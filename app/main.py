from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from .model_service import model_service
from .settings import settings


class PredictRequest(BaseModel):
    # Lista de 28*28 valores normalizados [0, 1]
    data: list


app = FastAPI(title=f"MNIST ONNX API - {settings.environment}")


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}


@app.post("/predict")
def predict(req: PredictRequest):
    """
    Recibe una imagen 28x28 aplastada en un vector de 784 elementos y
    devuelve el dígito predicho (0–9).
    """
    arr = np.array(req.data, dtype=np.float32).reshape(1, 1, 28, 28)
    output = model_service.predict(arr)  # shape [1, 10]
    pred_digit = int(output.argmax())

    # Registrar en S3
    model_service.log_prediction(str(pred_digit))

    return {"prediction": pred_digit}
