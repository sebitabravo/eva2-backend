# Django Reserva API

Este proyecto es una API de reservas desarrollada con Django y Django REST Framework. La aplicación permite gestionar **clientes**, **mesas** y **reservas** mediante una API y una interfaz CRUD HTML.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Rutas Disponibles](#rutas-disponibles)

## Requisitos

- Python 3.12
- Django 5.1.3
- Django REST Framework 3.15.2
- SQLite (o cualquier base de datos compatible configurada en `settings.py`)

## Instalación

1. Clona el repositorio en tu máquina local:
```bash
git clone https://github.com/sebitabravo/eva2-backend.git
cd eva2-backend
```
2. Crear y activar un entorno virtual para el proyecto:
```bash
source djangoenv/bin/activate
```

3. Instalar las dependencias necesarias
```bash
pip install -r requirements.txt
```

4. Iniciar el servidor de desarrollo de Django, ejecuta:
```bash
python3 manage.py runserver 0.0.0.0:8000
```
- El servidor estará disponible en http://localhost:8000 o en tu IP de red local.

## Uso
### Interfaz CRUD
Puedes acceder a la interfaz de usuario HTML para gestionar clientes, mesas y reservas. Accede a las siguientes URLs en tu navegador:
- **Clientes**: [http://localhost:8000/clientes/](http://localhost:8000/clientes/)
- **Mesas**: [http://localhost:8000/mesas/](http://localhost:8000/mesas/)
- **Reservas**: [http://localhost:8000/reservas/](http://localhost:8000/reservas/)


### API REST
Para realizar solicitudes a la API REST, puedes usar una herramienta como Postman o cURL.
- **Clientes**:
  - **Listar y Crear**: `GET/POST` [http://localhost:8000/api/clientes/](http://localhost:8000/api/clientes/)
  - **Detalle, Actualizar, Eliminar**: `GET/PUT/DELETE` [http://localhost:8000/api/clientes/<id>/](http://localhost:8000/api/clientes/<id>/)

- **Mesas**:
  - **Listar y Crear**: `GET/POST` [http://localhost:8000/api/mesas/](http://localhost:8000/api/mesas/)
  - **Detalle, Actualizar, Eliminar**: `GET/PUT/DELETE` [http://localhost:8000/api/mesas/<id>/](http://localhost:8000/api/mesas/<id>/)

- **Reservas**:
  - **Listar y Crear**: `GET/POST` [http://localhost:8000/api/reservas/](http://localhost:8000/api/reservas/)
  - **Detalle, Actualizar, Eliminar**: `GET/PUT/DELETE` [http://localhost:8000/api/reservas/<id>/](http://localhost:8000/api/reservas/<id>/)

## Rutas Disponibles
- **clientes/**: Listar, crear, actualizar y eliminar clientes.
- **mesas/**: Listar, crear, actualizar y eliminar mesas.
- **reservas/**: Listar, crear, actualizar y eliminar reservas.
- **api/clientes/**: Endpoints de la API REST para gestionar clientes.
- **api/mesas/**: Endpoints de la API REST para gestionar mesas.
- **api/reservas/**: Endpoints de la API REST para gestionar reservas.

## Contribución
Si deseas contribuir, por favor realiza un fork del repositorio y crea un pull request con tus cambios. Cualquier sugerencia es bienvenida.
