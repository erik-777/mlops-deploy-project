import boto3
import onnxruntime as ort
import numpy as np
from botocore.exceptions import ClientError

from .settings import settings


class ModelService:
    def __init__(self):
        # El modelo se empaqueta en la imagen como "model.onnx"
        self.model_path = "model.onnx"
        self.session = None
        self.s3 = boto3.client("s3", region_name=settings.aws_region)

    def load_model(self):
        if self.session is None:
            self.session = ort.InferenceSession(self.model_path)

    def predict(self, input_array: np.ndarray) -> np.ndarray:
        """
        input_array: np.array con shape [1, 1, 28, 28]
        """
        if self.session is None:
            self.load_model()

        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: input_array})
        return outputs[0]

    def log_prediction(self, prediction: str):
        """
        Agrega una línea con la predicción al archivo TXT en S3.
        """
        bucket = settings.bucket_name
        key = settings.predictions_file_key

        # Leer contenido previo (si existe)
        try:
            obj = self.s3.get_object(Bucket=bucket, Key=key)
            content = obj["Body"].read().decode("utf-8")
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                content = ""
            else:
                raise

        # Agregar nueva línea
        new_content = content + prediction + "\n"

        # Subir archivo actualizado
        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=new_content.encode("utf-8"),
        )


model_service = ModelService()
