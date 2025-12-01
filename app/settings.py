import os


class Settings:
    # S3
    bucket_name: str = os.getenv("BUCKET_NAME", "")
    predictions_file_key: str = os.getenv("PREDICTIONS_FILE_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")

    # Entorno (dev o prod)
    environment: str = os.getenv("ENVIRONMENT", "dev")


settings = Settings()
