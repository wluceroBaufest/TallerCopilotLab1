# Backend - JWT Authentication API

API REST desarrollada con **FastAPI** que implementa autenticación basada en **JSON Web Tokens (JWT)**.

## Características

- Endpoint de login que valida credenciales y retorna un JWT con expiración de 300 segundos.
- Endpoint de refresh que permite renovar un token válido.
- Gestión de dependencias con **Poetry**.
- Despliegue mediante **Docker**.

## Requisitos

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

## Instalación

```bash
cd backend
poetry install
```

## Ejecución

```bash
poetry run uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

## Endpoints

### POST /login

Autentica al usuario y devuelve un token JWT.

**Request body:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200):**

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

**Response (401):**

```json
{
  "detail": "Invalid username or password"
}
```

### POST /refresh

Renueva un token JWT válido.

**Request body:**

```json
{
  "token": "<jwt_token>"
}
```

**Response (200):**

```json
{
  "access_token": "<new_jwt_token>",
  "token_type": "bearer"
}
```

**Response (401):**

```json
{
  "detail": "Invalid or expired token"
}
```

## Tests

```bash
poetry run pytest
```

## Docker

### Construir la imagen

```bash
docker build -t jwt-backend .
```

### Ejecutar el contenedor

```bash
docker run -p 8000:8000 jwt-backend
```

La API estará disponible en `http://localhost:8000`.

## Documentación interactiva

FastAPI genera documentación automática disponible en:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
