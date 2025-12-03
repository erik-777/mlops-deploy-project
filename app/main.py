from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from model_service import model_service
from settings import settings   


class PredictRequest(BaseModel):
    data: list  # Imagen normalizada 28x28


app = FastAPI(title=f"MNIST ONNX API - {settings.environment}")


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}

@app.get("/check")
def health():
    return {"status": "check", "env": settings.environment}


@app.post("/predict")
def predict(req: PredictRequest):
    # Convertir lista → numpy tensor shape [1,1,28,28]
    arr = np.array(req.data, dtype=np.float32).reshape(1, 1, 28, 28)

    output = model_service.predict(arr)
    pred_digit = int(output.argmax())

    # Guardar predicción en S3
    model_service.log_prediction(str(pred_digit))

    return {"prediction": pred_digit}
