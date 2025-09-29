from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
import requests
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime

app = FastAPI(title="Student Microservice - DevOps Ready")

# Statisches Frontend mounten (wichtig: Pfad im Container)
app.mount("/frontend", StaticFiles(directory="/app/frontend"), name="frontend")

@app.get("/")
def serve_root():
    return FileResponse("/app/frontend/index.html")

# Prometheus metrics
REQUEST_COUNT = Counter("app_requests_total", "Total HTTP requests")
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency seconds")

class Item(BaseModel):
    id: int
    name: str
    value: float

class ConvertRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

STORE = {}

@app.get("/health")
def health():
    REQUEST_COUNT.inc()
    return {"status": "ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        item = STORE.get(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

@app.post("/items")
def create_item(item: Item):
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        if item.id in STORE:
            raise HTTPException(status_code=400, detail="Item exists")
        STORE[item.id] = item.dict()
        return {"created": True, "item": STORE[item.id]}

@app.post("/compute")
def compute(payload: dict):
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        x = payload.get('x', 0)
        y = payload.get('y', 0)
        return {"x": x, "y": y, "sum": x + y, "product": x * y}

# --------------------------
# Currency converter endpoints
# --------------------------

FALLBACK_RATES = {
    # simple symmetric sample table (not exhaustive)
    "USD": {"EUR": 0.92, "GBP": 0.78, "JPY": 150.0},
    "EUR": {"USD": 1.09, "GBP": 0.85, "JPY": 163.0},
    "GBP": {"USD": 1.28, "EUR": 1.17, "JPY": 192.0},
    "JPY": {"USD": 0.0067, "EUR": 0.0061}
}

def compute_with_fallback(frm: str, to: str, amount: float):
    frm = frm.upper()
    to = to.upper()
    if frm == to:
        return 1.0, amount
    # direct fallback
    rate = None
    if frm in FALLBACK_RATES and to in FALLBACK_RATES[frm]:
        rate = FALLBACK_RATES[frm][to]
    # inverse if available
    elif to in FALLBACK_RATES and frm in FALLBACK_RATES[to]:
        rate = 1.0 / FALLBACK_RATES[to][frm]
    else:
        # try via USD as hub
        if frm != "USD" and to != "USD":
            if frm in FALLBACK_RATES and "USD" in FALLBACK_RATES[frm] and "USD" in FALLBACK_RATES and to in FALLBACK_RATES["USD"]:
                rate = FALLBACK_RATES[frm]["USD"] * FALLBACK_RATES["USD"][to]
    if rate is None:
        raise HTTPException(status_code=503, detail="No rate available (fallback)")
    return rate, amount * rate

@app.get("/convert")
def convert_get(from_currency: str = "USD", to_currency: str = "EUR", amount: float = 1.0):
    """
    GET /convert?from_currency=USD&to_currency=EUR&amount=100
    """
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        from_currency = (from_currency or "USD").upper()
        to_currency = (to_currency or "EUR").upper()
        try:
            # primary: try public free API
            resp = requests.get(
                "https://api.exchangerate.host/convert",
                params={"from": from_currency, "to": to_currency, "amount": amount},
                timeout=5,
            )
            data = resp.json()
            # expected fields: result and info.rate
            if data and "result" in data:
                rate = data.get("info", {}).get("rate")
                return {
                    "from": from_currency,
                    "to": to_currency,
                    "amount": amount,
                    "rate": rate,
                    "result": data.get("result"),
                    "source": "live",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
        except Exception:
            # ignore and go to fallback
            pass

        # fallback
        try:
            rate, result = compute_with_fallback(from_currency, to_currency, amount)
            return {
                "from": from_currency,
                "to": to_currency,
                "amount": amount,
                "rate": rate,
                "result": result,
                "source": "fallback",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        except HTTPException as e:
            raise e

@app.post("/convert")
def convert_post(payload: ConvertRequest):
    return convert_get(from_currency=payload.from_currency, to_currency=payload.to_currency, amount=payload.amount)

# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    resp = generate_latest()
    return PlainTextResponse(content=resp, media_type=CONTENT_TYPE_LATEST)
