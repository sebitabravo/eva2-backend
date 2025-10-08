#!/bin/bash
set -e

echo "================================================"
echo "  Django Reservas API - Iniciando servicios"
echo "================================================"

# Esperar a que la base de datos esté lista
echo "Esperando a que PostgreSQL esté disponible..."
while ! nc -z $DATABASE_HOST 5432; do
  sleep 0.1
done
echo "✓ PostgreSQL está listo"

# Ejecutar migraciones
echo "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput
echo "✓ Migraciones completadas"

# Crear superusuario si no existe
echo "Verificando superusuario..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✓ Superusuario {username} creado exitosamente')
else:
    print(f'✓ Superusuario {username} ya existe')
EOF

# Poblar base de datos si AUTO_POPULATE_DB está habilitado
if [ "$AUTO_POPULATE_DB" = "True" ]; then
    echo "Auto-población de BD habilitada. Verificando datos..."
    python manage.py populate_db
fi

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
echo "✓ Archivos estáticos recolectados"

echo "================================================"
echo "  ✓ Inicialización completada"
echo "  Iniciando Gunicorn..."
echo "================================================"

# Ejecutar Gunicorn (optimizado para recursos limitados)
exec gunicorn drf.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-1} \
    --threads ${GUNICORN_THREADS:-4} \
    --worker-class sync \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --max-requests ${GUNICORN_MAX_REQUESTS:-500} \
    --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-50} \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --preload
