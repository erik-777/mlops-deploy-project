
# Guía de Configuración EC2 para Producción

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Configuración de la Instancia EC2](#configuración-de-la-instancia-ec2)

   * [Crear Instancia EC2](#crear-instancia-ec2)
   * [Configuración de Grupos de Seguridad](#configuración-de-grupos-de-seguridad)
4. [Acceso SSH y Configuración de Seguridad](#acceso-ssh-y-configuración-de-seguridad)
5. [Instalar Dependencias](#instalar-dependencias)

   * [Dependencias del Sistema](#dependencias-del-sistema)
   * [Configuración del Entorno Python](#configuración-del-entorno-python)
6. [Configurar Docker y Docker Compose](#configurar-docker-y-docker-compose)
7. [Desplegar la Aplicación en Producción](#desplegar-la-aplicación-en-producción)
8. [Configuración Post-Despliegue](#configuración-post-despliegue)
9. [Monitoreo y Registro](#monitoreo-y-registro)
10. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Esta guía cubre todos los pasos necesarios para configurar tu instancia EC2 en un entorno de **producción**. Incluye desde la creación de la instancia hasta el despliegue de la aplicación, asegurando que todo esté optimizado para un entorno de producción seguro, escalable y eficiente.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

* Una cuenta de AWS y acceso a EC2.
* AWS CLI configurado localmente (`aws configure`).
* Claves SSH para el acceso seguro a la instancia EC2.
* Docker y Docker Compose instalados en tu máquina local (opcional para pruebas).
* Acceso IAM adecuado para gestionar instancias EC2 y otros servicios AWS necesarios.

---

## Configuración de la Instancia EC2

### Crear Instancia EC2

1. **Iniciar sesión en la Consola de AWS**: Accede a la consola de AWS y abre el panel de EC2.

2. **Lanzar Instancia**: Haz clic en "Launch Instance" para crear una nueva instancia EC2.

   * **Seleccionar AMI**: Elige Ubuntu 20.04 LTS (u otra versión compatible para producción).
   * **Tipo de Instancia**: Para producción, selecciona una instancia con suficiente capacidad, por ejemplo, `t3.medium` o superior según la carga estimada.
   * **Configurar Instancia**: Define configuraciones avanzadas, incluyendo la red y el rol IAM para la instancia.
   * **Almacenamiento**: Asegúrate de que la instancia tenga suficiente almacenamiento para tu aplicación y archivos.
   * **Configurar Grupos de Seguridad**: Asegúrate de abrir puertos como:

     * **SSH (Puerto 22)** para el acceso remoto.
     * **HTTP (Puerto 80)** y **HTTPS (Puerto 443)** para servicios web.
     * **Puerto personalizado** (e.g., 8000) si tu aplicación lo requiere.

3. **Revisar y Lanzar**: Revisa las configuraciones y lanza la instancia.

---

### Configuración de Grupos de Seguridad

Asegúrate de que tu instancia EC2 esté protegida y que solo los puertos necesarios estén abiertos:

1. **Acceso SSH**: Permite el acceso SSH en el puerto 22 solo desde tu IP de administración.
2. **Acceso HTTP y HTTPS**: Abre los puertos 80 y 443 para tráfico web.
3. **Otros Puertos**: Abre puertos adicionales según sea necesario para tu aplicación (por ejemplo, puerto 8000 para APIs).

---

## Acceso SSH y Configuración de Seguridad

1. **Descargar la Clave SSH**: Cuando crees la instancia, asegúrate de descargar la clave SSH (`mi-ec2-clave.pem`).
2. **Configurar los Permisos para la Clave SSH**:

   ```bash
   chmod 400 mi-ec2-clave.pem
   ```
3. **Acceder a la Instancia EC2**:

   ```bash
   ssh -i "mi-ec2-clave.pem" ubuntu@<ip-publica-ec2>
   ```

---

## Instalar Dependencias

### Dependencias del Sistema

Asegúrate de tener las herramientas y bibliotecas necesarias en el sistema para la aplicación:

```bash
sudo apt update
sudo apt install -y build-essential curl git
```

### Configuración del Entorno Python

1. **Instalar Python 3 y Pip**:

   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Crear un Entorno Virtual en Python**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar las Dependencias de Python**:
   Si tienes un archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configurar Docker y Docker Compose

1. **Instalar Docker**:

   ```bash
   sudo apt install docker.io
   ```

2. **Iniciar y habilitar Docker**:

   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Verificar la instalación de Docker**:

   ```bash
   docker --version
   ```

4. **Instalar Docker Compose**:

   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

5. **Verificar la instalación de Docker Compose**:

   ```bash
   docker-compose --version
   ```

---

## Desplegar la Aplicación en Producción

1. **Clonar tu Proyecto**:

   ```bash
   git clone <repositorio-url>
   cd <directorio-del-proyecto>
   ```

2. **Construir la Imagen Docker**:

   ```bash
   docker build -t mi-aplicacion .
   ```

3. **Ejecutar el Contenedor Docker**:

   ```bash
   docker run -d -p 80:8000 --name mi-aplicacion-contenedor mi-aplicacion
   ```

4. **Verificar que el Contenedor está Corriendo**:

   ```bash
   docker ps
   ```

---

## Configuración Post-Despliegue

Después de desplegar la aplicación, asegúrate de:

* Configurar un entorno de monitoreo para la aplicación.
* Configurar el autoescalado de la instancia si es necesario para manejar picos de tráfico.
* Asegurarte de que tu aplicación esté optimizada para producción.

---

## Monitoreo y Registro

1. **Configurar AWS CloudWatch** para monitorear logs y métricas.
2. **Usar herramientas de logging** como `Fluentd` o `Logstash` para enviar logs a un servidor de logs centralizado.
3. **Configurar alertas** para estar al tanto de posibles problemas en el sistema.

---

## Solución de Problemas

1. **Errores de Docker**: Si el contenedor no se inicia correctamente, revisa los logs:

   ```bash
   docker logs <id-contenedor>
   ```

2. **Problemas de Conexión SSH**: Si no puedes acceder, verifica la configuración de los grupos de seguridad y asegúrate de que la IP pública sea accesible.


