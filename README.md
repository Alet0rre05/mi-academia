# Mi Academia

CRUD de Cursos y Alumnos con Django 5.2 (MVT) y PostgreSQL.

## Puesta en marcha

```bash
# 1. Entorno virtual y dependencias
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Base de datos (PostgreSQL debe estar corriendo)
createdb mi_academia            # o crearla desde pgAdmin

# 3. Variables de entorno (ver .env.example)
export DB_NAME=mi_academia DB_USER=postgres DB_PASSWORD=tu_clave DB_HOST=localhost DB_PORT=5432
# Windows PowerShell: $env:DB_NAME="mi_academia"  (y así con las demás)

# 4. Migraciones y servidor
python manage.py makemigrations academia
python manage.py migrate
python manage.py createsuperuser   # opcional, para /admin/
python manage.py runserver
```

Abrí http://127.0.0.1:8000/
