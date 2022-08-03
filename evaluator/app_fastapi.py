import uvicorn
from typing import Dict, Any
from fastapi import FastAPI

from eval_func import eval_func # local module

DEBUG = True
PORT = 5000

app = FastAPI()

@app.post("/eval")
def evaluate(body: Dict[Any, Any]):
    payload = body['payload']
    r = eval_func(payload)
    return r

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
