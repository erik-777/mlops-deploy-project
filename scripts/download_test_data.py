import os
import boto3

BUCKET_NAME = os.environ["BUCKET_NAME"]
TEST_DATA_KEY = os.environ["TEST_DATA_KEY"]  # ej: test_data/mnist_test.npz
LOCAL_PATH = "test_data.npz"

s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))

if __name__ == "__main__":
    s3.download_file(BUCKET_NAME, TEST_DATA_KEY, LOCAL_PATH)
    print(f"Datos de prueba descargados en {LOCAL_PATH}")
