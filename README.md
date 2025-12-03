# Despliegue automático de modelo ONNX (MNIST) con AWS y GitHub Actions

Este repositorio implementa un sistema de **despliegue automático** para un modelo de clasificación de dígitos manuscritos en formato **ONNX**, usando:

- AWS S3 (modelo, datos de prueba, logs de predicciones)
- AWS ECR (registro de imágenes Docker)
- AWS EC2 (dos instancias: `dev` y `prod`)
- GitHub Actions (pipeline CI/CD)
- FastAPI (API de predicción)
- ONNX Runtime (inferencias)

## Objetivo

Permitir que **nuevos modelos ONNX** puedan ser desplegados de forma automática a dos entornos (`dev` y `prod`), asegurando:

1. Descarga del modelo y datos de prueba desde un bucket externo.
2. Ejecución de pruebas unitarias antes del despliegue:
   - El modelo responde a entradas definidas.
   - La métrica (accuracy) está por encima de un umbral.
3. Construcción de un contenedor Docker con la aplicación.
4. Despliegue automático del contenedor en EC2.
5. Registro de todas las predicciones en archivos TXT en S3 para monitoreo.

## Arquitectura

![Diagrama de Arquitectura](/mlops-deploy-project/infra/Diagrama%20de%20Componentes.png "Diagrama de Arquitectura")

- **S3**  
  - `models/mnist-12.onnx` → modelo ONNX  
  - `test_data/mnist_test.npz` → datos de prueba  
  - `logs/predicciones_dev.txt` → log de predicciones dev  
  - `logs/predicciones_prod.txt` → log de predicciones prod  

- **EC2**  
  - Instancia `dev`: expone `http://<EC2_DEV_IP>/predict`  
  - Instancia `prod`: expone `http://<EC2_PROD_IP>/predict`  

- **GitHub Actions**  
  - Rama `dev` → despliegue a instancia `dev`  
  - Rama `prod` → despliegue a instancia `prod`  

## Estructura del repositorio

```text
app/
  main.py              # API FastAPI (endpoints /health y /predict)
  model_service.py     # Carga del modelo ONNX y logging a S3
  settings.py          # Configuración por variables de entorno
  requirements.txt
  tests/
    test_model_runs.py # El modelo responde a entradas definidas
    test_metric.py     # La métrica de accuracy ≥ umbral

scripts/
  download_model.py    # Descarga modelo desde S3 en CI
  download_test_data.py# Descarga datos de prueba desde S3 en CI

docker/
  Dockerfile           # Construcción de la imagen del contenedor

.github/
  workflows/
    deploy.yml         # Pipeline CI/CD (test + build + deploy)

infra/
  ec2-dev-setup.md     # Notas de configuración de EC2 dev (documental)
  ec2-prod-setup.md    # Notas de configuración de EC2 prod (documental)
  iam-policy.json      # Política IAM de ejemplo para S3/ECR

utils/
  diagram-architecture.png  # Diagrama de arquitectura
