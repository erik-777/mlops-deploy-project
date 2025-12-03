import os
import boto3

BUCKET_NAME = os.environ["BUCKET_NAME"]
MODEL_KEY = os.environ["MODEL_KEY"]  # ej: models/mnist-12.onnx
LOCAL_PATH = "model.onnx"

s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))

if __name__ == "__main__":
    s3.download_file(BUCKET_NAME, MODEL_KEY, LOCAL_PATH)
    print(f"Modelo descargado en {LOCAL_PATH}")
