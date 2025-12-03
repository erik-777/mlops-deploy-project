

# Guía de Configuración de EC2 para Desarrollo

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Configuración de la Instancia](#configuración-de-la-instancia)

   * [Crear Instancia EC2](#crear-instancia-ec2)
   * [Configuración de Grupos de Seguridad](#configuración-de-grupos-de-seguridad)
4. [Configuración del Acceso SSH](#configuración-del-acceso-ssh)
5. [Instalar Dependencias](#instalar-dependencias)

   * [Dependencias del Sistema](#dependencias-del-sistema)
   * [Configuración del Entorno Python](#configuración-del-entorno-python)
6. [Configurar Docker y Docker Compose](#configurar-docker-y-docker-compose)
7. [Desplegar la Aplicación](#desplegar-la-aplicación)
8. [Configuración Post-Instalación](#configuración-post-instalación)
9. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Esta guía te llevará a través de los pasos necesarios para configurar tu instancia EC2 para fines de desarrollo. Cubre la creación de la instancia EC2, la configuración de las claves SSH, la instalación de dependencias del sistema y Python, y el despliegue de la aplicación.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

* Una cuenta de AWS.
* AWS CLI configurado localmente (`aws configure`).
* Clave SSH para acceso seguro a las instancias EC2.
* Docker y Docker Compose instalados en tu máquina local (opcional para pruebas locales).
* El rol IAM necesario para el acceso de EC2 (si aplica).

---

## Configuración de la Instancia

### Crear Instancia EC2

1. **Iniciar sesión en la Consola de AWS**: Abre el panel de EC2.

2. **Lanzar Instancia**: Haz clic en "Launch Instance" para crear una nueva instancia EC2.

   * **Seleccionar AMI**: Elige una AMI de Ubuntu 20.04 LTS.
   * **Tipo de Instancia**: Selecciona el tipo de instancia adecuado (por ejemplo, `t2.micro` para pruebas).
   * **Configurar Instancia**: Configura los parámetros de la instancia como red, rol IAM y monitoreo.
   * **Añadir Almacenamiento**: Asegúrate de tener suficiente espacio para tus archivos de proyecto y las imágenes de Docker.
   * **Configurar Grupo de Seguridad**: Abre los siguientes puertos:

     * SSH (Puerto 22) para acceso remoto.
     * HTTP (Puerto 80) para servicios web.
     * Puerto personalizado (por ejemplo, 8000 para tu API).

3. **Revisar y Lanzar**: Una vez configurada, lanza la instancia.

---

### Configuración de Grupos de Seguridad

Asegúrate de que tu instancia EC2 tenga configurados los grupos de seguridad correctos:

1. **Acceso SSH**: Asegúrate de que el puerto 22 esté abierto para la IP que usarás para acceder a la instancia.
2. **Acceso HTTP**: Abre el puerto 80 (o el puerto que use tu aplicación) para permitir tráfico HTTP entrante.
3. **Otros Puertos**: Abre cualquier otro puerto necesario para tu aplicación (por ejemplo, para contenedores Docker).

---

## Configuración del Acceso SSH

1. **Descargar la Clave SSH**: Al crear tu instancia EC2, asegúrate de generar y descargar la clave SSH (por ejemplo, `mi-ec2-clave.pem`).
2. **Establecer Permisos para la Clave SSH**:

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

Instala las bibliotecas y herramientas necesarias para el sistema:

```bash
sudo apt update
sudo apt install -y build-essential curl git
```

### Configuración del Entorno Python

1. **Instalar Python 3**:

   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Crear un Entorno Virtual en Python**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar las Dependencias de Python**:
   Suponiendo que tienes un archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configurar Docker y Docker Compose

1. **Instalar Docker**:

   ```bash
   sudo apt install docker.io
   ```

2. **Iniciar Docker**:

   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Verificar la Instalación de Docker**:

   ```bash
   docker --version
   ```

4. **Instalar Docker Compose**:

   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

5. **Verificar la Instalación de Docker Compose**:

   ```bash
   docker-compose --version
   ```

---

## Desplegar la Aplicación

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

## Configuración Post-Instalación

Después de configurar la instancia EC2, asegúrate de:

* Configurar el registro y monitoreo para tu aplicación.
* Configurar tu instancia para escalabilidad automática si es necesario.
* Asegurar tu instancia EC2 deshabilitando el acceso root y usando autenticación basada en claves.

---

## Solución de Problemas

* **Problemas con Docker**: Si tu contenedor no está corriendo, revisa los logs:

  ```bash
  docker logs <id-contenedor>
  ```
* **Problemas de Acceso**: Si no puedes acceder a la instancia, verifica la configuración del grupo de seguridad y si la IP pública es accesible.

