FROM python:3.11-slim

WORKDIR /app

# Dependencias de sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la app
COPY app/ /app/

# El modelo se copiará en build_and_deploy (CI) en la raíz,
# luego lo añadimos a la imagen:
COPY model.onnx /app/model.onnx

EXPOSE 8000

ENV ENVIRONMENT=dev

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
