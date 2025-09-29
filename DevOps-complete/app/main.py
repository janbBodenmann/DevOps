
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Student Microservice - DevOps Ready")

REQUEST_COUNT = Counter("app_requests_total", "Total HTTP requests")
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency seconds")

class Item(BaseModel):
    id: int
    name: str
    value: float

# in-memory store
STORE = {}

@app.get("/health")
def health():
    REQUEST_COUNT.inc()
    return {"status":"ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        item = STORE.get(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

@app.get("/external")
def call_external():
    """Call an external microservice (example: httpbin.org/get). In an offline environment this may fail."""
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        try:
            r = requests.get("https://httpbin.org/get", timeout=5)
            return {"status":"ok","external_status": r.status_code, "external_args": r.json().get('args',{})}
        except Exception as e:
            # graceful fallback (important for CI/offline)
            return {"status":"ok","external_error": str(e)}

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
    """a small POST endpoint that does some computation and returns result"""
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        x = payload.get('x', 0)
        y = payload.get('y', 0)
        return {"x": x, "y": y, "sum": x + y, "product": x * y}

# Metrics endpoint for Prometheus to scrape
@app.get("/metrics")
def metrics():
    resp = generate_latest()
    return PlainTextResponse(content=resp, media_type=CONTENT_TYPE_LATEST)
