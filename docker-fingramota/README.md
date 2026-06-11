# FinGramota Docker

## Development

The default Compose command automatically loads `docker-compose.override.yml`,
mounts the source code, and starts Django and Nuxt with hot reload:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

## Production-like

Use only the base Compose file to run Gunicorn and the built Nuxt server:

```powershell
docker compose -f docker-compose.yml up --build
```

Replace the example passwords and `DJANGO_SECRET_KEY` in `.env` before using
the production-like configuration outside local development.

## Services

- Nuxt: http://localhost:3000
- Django health endpoint: http://localhost:8000/api/health/
- Django admin: http://localhost:8000/admin/
- PostgreSQL: `localhost:5432`
- pgAdmin: http://localhost:5050

To register PostgreSQL in pgAdmin, use:

- Host: `postgres`
- Port: `5432`
- Database: the value of `POSTGRES_DB`
- Username: the value of `POSTGRES_USER`
- Password: the value of `POSTGRES_PASSWORD`

Stop the stack without deleting database data:

```powershell
docker compose down
```

Delete containers and persistent data:

```powershell
docker compose down --volumes
```
