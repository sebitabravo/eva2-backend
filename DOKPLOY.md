# Configuración para Dokploy

## Problema común: Puerto incorrecto de PostgreSQL

Si ves el error `connection to server at "db" port 5433 failed`, es porque algo está sobrescribiendo la configuración del puerto.

### Diagnóstico

El sistema ahora incluye validación automática. Al iniciar el contenedor, verás en los logs:

```
Variables de entorno de base de datos:
  DATABASE_HOST: db
  DATABASE_PORT: 5432
  DATABASE_NAME: reservas_db
  DATABASE_USER: reservas_user
  DATABASE_URL: postgresql://***:***@db:5432/***

Verificando configuración de Django...
Django usará:
  ENGINE: django.db.backends.postgresql
  HOST: db
  PORT: 5432
  NAME: reservas_db
  USER: reservas_user
```

Si ves un puerto diferente a 5432 en "Django usará", significa que:
1. Dokploy está inyectando variables adicionales
2. Hay una variable de entorno en la plataforma que no está en tu .env

### Solución en Dokploy

#### Opción 1: Usar archivo .env (Recomendado)
1. Ve a tu proyecto en Dokploy
2. En la configuración, asegúrate de que esté usando el archivo `.env` del repositorio
3. **NO agregues variables de base de datos manualmente** si Dokploy las detecta automáticamente

#### Opción 2: Configurar manualmente
Si Dokploy no lee el .env correctamente:

1. Ve a tu proyecto en Dokploy
2. En la sección de **Variables de Entorno**, configura EXACTAMENTE estas variables:

```bash
DATABASE_URL=postgresql://reservas_user:TU_PASSWORD@db:5432/reservas_db
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=reservas_db
DATABASE_USER=reservas_user
DATABASE_PASSWORD=TU_PASSWORD
```

3. **CRÍTICO**: Si Dokploy muestra variables adicionales como `POSTGRES_PORT_5433_TCP_PORT` o similares, **elimínalas**
4. Después de configurar las variables, reconstruye y redeploya

### Fix aplicado en el código

El archivo `settings.py` ahora fuerza el puerto desde `DATABASE_PORT`:

```python
# Forzar el puerto a 5432 si está usando PostgreSQL
if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
    DATABASES['default']['PORT'] = config('DATABASE_PORT', default='5432')
```

Esto asegura que incluso si `DATABASE_URL` tiene un puerto incorrecto, se sobrescribirá con el valor correcto de `DATABASE_PORT`.

## Variables de entorno requeridas

Revisa el archivo `.env.example` para ver todas las variables necesarias.

### Variables críticas:
- `DATABASE_URL` - URL completa de conexión (formato: `postgresql://user:pass@host:port/dbname`)
- `SECRET_KEY` - Clave secreta de Django (genera una nueva para producción)
- `ALLOWED_HOSTS` - Dominios permitidos (separados por comas)
- `CSRF_TRUSTED_ORIGINS` - Orígenes confiables para CSRF (con https://)

### Comandos útiles

Ver logs del contenedor:
```bash
docker logs reservas_api -f
```

Ver logs de PostgreSQL:
```bash
docker logs reservas_db -f
```

Ejecutar migraciones manualmente:
```bash
docker exec -it reservas_api python manage.py migrate
```

Acceder a la shell de Django:
```bash
docker exec -it reservas_api python manage.py shell
```
