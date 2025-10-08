# Django Reserva API - Sistema de Gestión de Reservas

[![Django](https://img.shields.io/badge/Django-5.1.3-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

API REST profesional para gestión de reservas de restaurantes. Incluye autenticación JWT, rate limiting, estadísticas avanzadas, validaciones robustas y configuración lista para producción.

## Características Principales

- **API Pública de Lectura**: GET sin autenticación (100 req/hora) | **Escritura Protegida**: Admin only (20 req/hora)
- **Multi-Usuario**: Cada usuario gestiona sus propios recursos | **Estadísticas Avanzadas**: Análisis y métricas de negocio
- **Validación Robusta**: Método `clean()` en modelos | **JWT Auth**: Access + Refresh tokens
- **Rate Limiting**: Protección anti-DDoS diferenciado | **Swagger/OpenAPI**: Documentación interactiva
- **Docker Ready**: PostgreSQL + Gunicorn | **Monitoreo**: Script de análisis de recursos

## Stack Tecnológico

**Backend**: Django 5.1.3 + DRF 3.15.2 | **DB**: PostgreSQL 16 | **Auth**: JWT | **Server**: Gunicorn | **Docs**: drf-spectacular

## Quick Start

### Desarrollo Local

```bash
git clone https://github.com/sebitabravo/eva2-backend.git && cd eva2-backend
python3 -m venv djangoenv && source djangoenv/bin/activate
pip install -r requirements.txt && cd djangoapi
python manage.py migrate && python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Producción con Docker

```bash
cp .env.example .env  # Editar: SECRET_KEY, DB_PASSWORD, ALLOWED_HOSTS
docker-compose up -d --build
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Autenticación

```bash
POST /api/token/          # Obtener JWT | POST /api/token/refresh/  # Refresh
```

### CRUD Principal

| Endpoint | GET (Público) | POST/PUT/DELETE (Admin) | Límite |
|----------|---------------|-------------------------|--------|
| `/api/v1/clientes/` | Listar | Crear/Editar/Eliminar | 100/20/hora |
| `/api/v1/mesas/` | Listar | Crear/Editar/Eliminar | 100/20/hora |
| `/api/v1/reservas/` | Listar | Crear/Editar/Eliminar | 100/20/hora |

### Estadísticas (Autenticado - 10 req/hora)

```bash
GET /api/v1/reservas/estadisticas/       # Métricas generales del sistema
GET /api/v1/clientes/{id}/estadisticas/  # Historial de reservas por cliente
GET /api/v1/mesas/{id}/estadisticas/     # Ocupación y popularidad de mesa
```

**Métricas**: Total de reservas, distribución por estado, tendencias temporales, top 5 mesas/clientes/horarios, tasas de cancelación, promedios.

### Documentación

```yaml
http://localhost:8000/api/docs/    # Swagger UI | http://localhost:8000/api/schema/  # OpenAPI
```

## Configuración (.env)

```bash
# Core
SECRET_KEY=genera-con-get-random-secret-key
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,localhost

# HTTPS Configuration - IMPORTANTE para proxies como Dokploy
ENABLE_HTTPS=False  # Mantener False si usas proxy inverso (Dokploy, Nginx, etc.)
                    # El proxy maneja HTTPS, no Django directamente

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
DATABASE_PORT=5432

# JWT (minutos)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Rate Limiting
THROTTLE_ANON_RATE=100/hour      # Lectura pública
THROTTLE_USER_RATE=1000/hour     # Usuario autenticado
THROTTLE_READ_RATE=100/hour      # GET
THROTTLE_WRITE_RATE=20/hour      # POST/PUT/DELETE
THROTTLE_STATS_RATE=10/hour      # Estadísticas (costoso)
THROTTLE_BURST_RATE=30/min       # Anti-ráfagas

# CORS & CSRF
CORS_ALLOWED_ORIGINS=https://tu-frontend.com
CSRF_TRUSTED_ORIGINS=https://api-reserva.sbravo.app

# Gunicorn
GUNICORN_WORKERS=2
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=120
```

## Validaciones

**Clientes**: Email único/válido, teléfono chileno (+56912345678), nombre 2+ chars
**Mesas**: Número único/positivo, capacidad 1-20, validación `clean()`
**Reservas**: Fecha no pasada (max 90 días), horario 12:00-23:00 cada 30min, disponibilidad de mesa, estados (pendiente/confirmada/cancelada/completada), validación `clean()`

## Comandos Útiles

```bash
# Monitoreo
./monitor-resources.sh              # Estado | watch: continuo (5s) | alerts: alertas

# Docker
docker-compose logs -f web                                              # Logs
docker-compose exec web python manage.py migrate                       # Migrar
docker-compose exec db pg_dump -U postgres reservas_db > backup.sql   # Backup

# Generar SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Seguridad

- JWT con refresh tokens | Rate limiting diferenciado | CORS configurado | HTTPS redirect
- Secure cookies + XSS/CSRF protection | Secrets via .env | DEBUG=False en prod | Multi-usuario con ownership

## Recursos (512MB RAM / 1 CPU)

```yaml
web:  256MB RAM, 0.5 CPU, Gunicorn (1 worker + 4 threads)
db:   256MB RAM, 0.5 CPU, PostgreSQL (max_connections=20, shared_buffers=64MB)
```

## Estructura

```yaml
eva2-backend/
├── djangoapi/api/          # models.py, views.py, serializers.py, permissions.py, throttling.py, tests/
├── djangoapi/drf/          # settings.py, urls.py
├── Dockerfile              # Multi-stage build
├── docker-compose.yml      # PostgreSQL + Django
├── gunicorn.conf.py        # Producción
├── monitor-resources.sh    # Monitoreo
└── requirements.txt
```

## Documentación Adicional

- [DOKPLOY.md](DOKPLOY.md) - **Guía para Dokploy** (solución de problemas de despliegue)
- [NUEVAS_FUNCIONALIDADES.md](NUEVAS_FUNCIONALIDADES.md) - Estadísticas, clean(), monitoreo
- [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) - Deployment completo
- [RATE_LIMITING.md](RATE_LIMITING.md) - Throttling
- [COMPARACION_EVA1_VS_EVA2.md](COMPARACION_EVA1_VS_EVA2.md) - Evolución
- [DOCKER_TEST_RESULTS.md](DOCKER_TEST_RESULTS.md) - Tests

## Autor

Sebastian Bravo - [GitHub](https://github.com/sebitabravo)
