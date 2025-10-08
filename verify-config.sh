#!/bin/bash
# Script para verificar la configuración de base de datos antes de desplegar

echo "======================================"
echo "  Verificación de configuración"
echo "======================================"
echo ""

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    echo "❌ Error: No existe el archivo .env"
    echo "   Copia .env.example a .env y configura las variables"
    exit 1
fi

echo "✓ Archivo .env encontrado"
echo ""

# Verificar variables críticas
echo "Variables de base de datos en .env:"
grep "^DATABASE_URL=" .env | sed 's/\(.*:\/\/[^:]*:\)[^@]*\(@.*\)/\1***\2/'
grep "^DATABASE_HOST=" .env
grep "^DATABASE_PORT=" .env
grep "^DATABASE_NAME=" .env
grep "^DATABASE_USER=" .env
echo "DATABASE_PASSWORD=***"
echo ""

# Validar que DATABASE_URL tenga el puerto correcto
DB_URL=$(grep "^DATABASE_URL=" .env | cut -d'=' -f2-)
if echo "$DB_URL" | grep -q ":5433"; then
    echo "❌ ERROR: DATABASE_URL tiene el puerto 5433 (incorrecto)"
    echo "   Debe ser 5432 para PostgreSQL"
    exit 1
elif echo "$DB_URL" | grep -q ":5432"; then
    echo "✓ DATABASE_URL tiene el puerto correcto (5432)"
else
    echo "⚠️  ADVERTENCIA: No se pudo detectar el puerto en DATABASE_URL"
fi

# Validar DATABASE_PORT
DB_PORT=$(grep "^DATABASE_PORT=" .env | cut -d'=' -f2- | tr -d "'\"")
if [ "$DB_PORT" != "5432" ]; then
    echo "❌ ERROR: DATABASE_PORT='$DB_PORT' (incorrecto)"
    echo "   Debe ser 5432 para PostgreSQL"
    exit 1
else
    echo "✓ DATABASE_PORT es correcto (5432)"
fi

echo ""
echo "======================================"
echo "  ✓ Configuración válida"
echo "======================================"
echo ""
echo "Puedes desplegar con:"
echo "  docker-compose up -d --build"
echo ""
echo "O hacer push para desplegar en Dokploy"
