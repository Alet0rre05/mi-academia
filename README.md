# 📚 Mi Academia - Guía Definitiva de Instalación y Despliegue Local (De Cero a 100)

Este proyecto es una aplicación web desarrollada con **Django 5.2** y **PostgreSQL**. 

Esta guía está diseñada para llevar a cualquier desarrollador desde una computadora sin configurar hasta tener el proyecto corriendo perfectamente en local, incluyendo todas las soluciones a problemas comunes (variables de entorno, autenticación de bases de datos y configuraciones de Windows).

---

## 🛠️ Fase 1: Descarga e Instalación de Herramientas Base

Si es tu primera vez configurando el entorno, necesitás instalar estos programas:

### 1. Python (3.10 o superior)
1. Descargá el instalador desde [python.org](https://www.python.org/downloads/).
2. **⚠️ PASO CRÍTICO:** Al abrir el instalador, marcá la casilla que dice **"Add Python to PATH"** (Agregar Python al PATH) antes de darle a "Install Now". Si no hacés esto, la terminal no reconocerá los comandos de Python.

### 2. PostgreSQL (Versión 16 o superior)
1. Descargá el instalador de Windows desde [postgresql.org](https://www.postgresql.org/download/windows/).
2. Durante la instalación, dejá el puerto por defecto (`5432`).
3. Te pedirá crear una contraseña para el superusuario `postgres`. **Anotala bien** (ej. `admin1234`), la vas a usar más adelante.

---

## ⚙️ Fase 2: Configuración de Rutas (PATH) en Windows

Para que la terminal de PowerShell reconozca comandos como `psql`, hay que agregarlo a las Variables de Entorno de Windows:

1. Presioná la tecla `Windows` y buscá **"Editar las variables de entorno del sistema"**.
2. Hacé clic en el botón **"Variables de entorno..."** (abajo a la derecha).
3. En la sección "Variables del sistema" (abajo), buscá la variable llamada **`Path`**, seleccionala y dale a **"Editar..."**.
4. Hacé clic en **"Nuevo"** y agregá la ruta donde se instalaron los binarios de PostgreSQL. Generalmente es:
   `C:\Program Files\PostgreSQL\16\bin`
   *(Asegurate de que el número coincida con tu versión instalada).*
5. Dale a Aceptar a todo y **reiniciá tu computadora** (o cerrá y volvé a abrir todas las terminales de PowerShell).

---

## 🗄️ Fase 3: Configuración de PostgreSQL

Vamos a crear la base de datos y el usuario para el proyecto.

1. Abrí **PowerShell** y conectate a PostgreSQL forzando la conexión por IPv4 (para evitar errores de Windows):
   ```powershell
   psql -U postgres -h 127.0.0.1
   ```
2. Ingresá la contraseña que elegiste al instalar PostgreSQL.
3. Una vez en la consola interactiva (`postgres=#`), ejecutá línea por línea:
   ```sql
   CREATE USER mi_academia_user WITH PASSWORD 'mi_clave_123';
   CREATE DATABASE mi_academia_db OWNER mi_academia_user;
   GRANT ALL PRIVILEGES ON DATABASE mi_academia_db TO mi_academia_user;
   \q
   ```

---

## 🚀 Fase 4: Preparación del Proyecto Local

### 1. Posicionarse en la carpeta
Abrí PowerShell y navegá a la carpeta donde clonaste o descargaste el proyecto:
```powershell
cd C:\Users\ejemplo\Ruta\Al\Proyecto\mi-academia
```

### 2. Crear y configurar `.env`
En la raíz del proyecto, creá un archivo llamado **`.env`**.
> **⚠️ CUIDADO EN WINDOWS:** Asegurate de que se llame **`.env`** y NO `.env.txt`. Si ves que Windows le agrega `.txt`, ejecutá esto en PowerShell para arreglarlo:
> `Rename-Item -Path ".\.env.txt" -NewName ".env"`

Pegá este contenido en el `.env`:
```env
SECRET_KEY=clave_secreta_desarrollo_local_123
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=mi_academia_db
DB_USER=mi_academia_user
DB_PASSWORD=mi_clave_123
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 3. Entorno Virtual y Dependencias
Ejecutá estos comandos en PowerShell:

```powershell
# 1. Habilitar ejecución de scripts (solo si da error PSSecurityException)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
.\.venv\Scripts\Activate.ps1
# (Debe aparecer '(.venv)' al inicio de la línea de la terminal)

# 4. Instalar dependencias del proyecto y de variables de entorno
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install python-dotenv
```

### 4. Actualizar `config/settings.py` (Importante)
Asegurate de que el archivo `settings.py` esté configurado para leer el `.env`. Agregá esto al inicio del archivo:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'default-insecure-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'mi_academia_db'),
        'USER': os.getenv('DB_USER', 'mi_academia_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'mi_clave_123'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

---

## 🏗️ Fase 5: Base de Datos Django y Ejecución

Con el entorno `(.venv)` activo, ejecutá:

```powershell
# 1. Preparar las migraciones de la base de datos
python manage.py makemigrations
python manage.py makemigrations academia

# 2. Crear las tablas físicas en PostgreSQL (Soluciona el ProgrammingError)
python manage.py migrate

# 3. Crear el usuario administrador
python manage.py createsuperuser

# 4. Levantar el servidor
python manage.py runserver
```

### Navegación
Abrí tu navegador e ingresá **escribiendo limpiamente** las URLs (evitá copiar corchetes o caracteres raros):
* **Inicio:** `http://127.0.0.1:8000/`
* **Admin:** `http://127.0.0.1:8000/admin/`

---

## 🚨 Troubleshooting Extendido (Errores Comunes)

Si te trabás, buscá tu error acá:

### 1. `psql: error: falló la conexión... la autentificación password falló para el usuario postgres`
Esto ocurre en Windows porque intenta conectar por IPv6 (`::1`).
**Solución:** Siempre conectate forzando IPv4 agregando `-h 127.0.0.1` al comando: `psql -U postgres -h 127.0.0.1`.

### 2. Olvidé la contraseña de PostgreSQL o no me deja entrar de ninguna forma (`FATAL: password authentication failed`)
**Solución de rescate (Modificar `pg_hba.conf`):**
1. Abrí el Bloc de notas como Administrador.
2. Abrí el archivo `C:\Program Files\PostgreSQL\16\data\pg_hba.conf`.
3. Al final del archivo, cambiá los métodos `scram-sha-256` por `trust` en las líneas de IPv4 e IPv6.
4. Presioná `Win + R`, escribí `services.msc`, buscá "postgresql-x64-16" y reinicialo.
5. Entrá a PowerShell y ejecutá `psql -U postgres -h 127.0.0.1` (entrarás sin clave).
6. Cambiá la clave: `ALTER USER postgres WITH PASSWORD 'admin1234';` y salí (`\q`).
7. Volvé a editar `pg_hba.conf`, devolvé los `trust` a `scram-sha-256`, guardá y reiniciá el servicio de nuevo.

### 3. `KeyError: 'DB_NAME'` o Django no arranca
**Causa:** Django no encuentra el `.env` o la librería `python-dotenv` no está instalada.
**Solución:** 
- Revisá que tu archivo no se llame `.env.txt`.
- Asegurate de haber instalado `pip install python-dotenv`.
- Revisá que `load_dotenv()` esté puesto al principio de `settings.py`.

### 4. `ProgrammingError: no existe la relación «academia_curso»`
**Causa:** La base de datos existe, pero las tablas de Django no se crearon.
**Solución:** Detené el servidor y ejecutá:
`python manage.py makemigrations academia`
`python manage.py migrate`

### 5. Página no encontrada (Error 404) al abrir el navegador
**Causa:** Estás pegando caracteres extraños en el navegador (ej: `/%5D(http://127.0.0.1:8000/`).
**Solución:** Escribí manualmente `http://127.0.0.1:8000/` en la barra de direcciones.

---

## 🔒 Git y Control de Versiones

Antes de subir código a GitHub, creá un archivo `.gitignore` en la raíz del proyecto para evitar subir archivos sensibles o pesados:

```text
.venv/
.env
__pycache__/
*.pyc
db.sqlite3
```
