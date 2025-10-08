#!/bin/bash
set -e

echo "================================================"
echo "  Django Reservas API - Iniciando servicios"
echo "================================================"

# Validar configuración de base de datos desde variables de entorno
echo "Variables de entorno de base de datos:"
echo "  DATABASE_HOST: ${DATABASE_HOST:-no configurado}"
echo "  DATABASE_PORT: ${DATABASE_PORT:-no configurado}"
echo "  DATABASE_NAME: ${DATABASE_NAME:-no configurado}"
echo "  DATABASE_USER: ${DATABASE_USER:-no configurado}"
if [ -n "$DATABASE_URL" ]; then
    # Extraer y mostrar solo el host y puerto del DATABASE_URL (sin contraseña)
    DB_INFO=$(echo "$DATABASE_URL" | sed -E 's/.*@([^:]+):([0-9]+).*/\1:\2/')
    echo "  DATABASE_URL: postgresql://***:***@${DB_INFO}/***"
fi

# Validar configuración que Django usará
echo ""
echo "Verificando configuración de Django..."
python << 'PYEOF'
import os
import sys
sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')

try:
    from django.conf import settings
    db_config = settings.DATABASES['default']
    print(f"Django usará:")
    print(f"  ENGINE: {db_config.get('ENGINE', 'no configurado')}")
    print(f"  HOST: {db_config.get('HOST', 'no configurado')}")
    print(f"  PORT: {db_config.get('PORT', 'no configurado')}")
    print(f"  NAME: {db_config.get('NAME', 'no configurado')}")
    print(f"  USER: {db_config.get('USER', 'no configurado')}")
    
    # Advertir si el puerto no es el esperado
    if db_config.get('PORT') and str(db_config.get('PORT')) != '5432':
        print(f"\n⚠️  ADVERTENCIA: El puerto {db_config.get('PORT')} no es el estándar 5432")
        print(f"   Esto puede causar errores de conexión si PostgreSQL está en 5432")
except Exception as e:
    print(f"Error al leer configuración de Django: {e}")
    sys.exit(1)
PYEOF

echo ""
# Esperar a que la base de datos esté lista
echo "Esperando a que PostgreSQL esté disponible..."
DB_PORT=${DATABASE_PORT:-5432}
echo "Intentando conectar a $DATABASE_HOST:$DB_PORT"
RETRY_COUNT=0
MAX_RETRIES=30
while ! nc -z $DATABASE_HOST $DB_PORT; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "❌ Error: No se pudo conectar a PostgreSQL después de $MAX_RETRIES intentos"
    echo "   Verifica que el contenedor de base de datos esté corriendo en el puerto $DB_PORT"
    exit 1
  fi
  sleep 1
done
echo "✓ PostgreSQL está listo en $DATABASE_HOST:$DB_PORT"

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
