from fastapi import FastAPI, Body
import requests

app = FastAPI()

conversions = []
favorites = []
last_conversion = None

EXCHANGE_API = "https://api.exchangerate.host/convert"

@app.post('/convert')
def convert(amount: float = Body(...), source: str = Body(...), target: str = Body(...)):
   
    response = requests.get(EXCHANGE_API, params={"from": source, "to": target, "amount": amount})
    data = response.json()
    result = data.get("result", None)

    global last_conversion
    last_conversion = {
        "amount": amount,
        "source": source,
        "target": target,
        "result": result
    }
    conversions.append(last_conversion)
    return last_conversion

@app.get('/last-conversion')
def get_last_conversion():
    return last_conversion

@app.post('/favorite')
def add_favorite(source: str = Body(...), target: str = Body(...)):
    favorite = {"source": source, "target": target}
    favorites.append(favorite)
    return favorite

@app.get('/favorites')
def get_favorites():
    return favorites