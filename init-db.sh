#!/bin/bash
set -e

# Este script se ejecuta automáticamente cuando el contenedor de PostgreSQL se inicia por primera vez
# Crea el usuario y la base de datos si no existen

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Crear el usuario si no existe
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DATABASE_USER}') THEN
            CREATE USER ${DATABASE_USER} WITH PASSWORD '${DATABASE_PASSWORD}';
        END IF;
    END
    \$\$;

    -- Otorgar todos los privilegios en la base de datos
    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${DATABASE_USER};
    
    -- Conectar a la base de datos y otorgar privilegios en el schema public
    \c ${POSTGRES_DB}
    GRANT ALL PRIVILEGES ON SCHEMA public TO ${DATABASE_USER};
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${DATABASE_USER};
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${DATABASE_USER};
    
    -- Otorgar privilegios por defecto para objetos futuros
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${DATABASE_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${DATABASE_USER};
EOSQL

echo "Usuario ${DATABASE_USER} configurado correctamente con acceso a ${POSTGRES_DB}"
