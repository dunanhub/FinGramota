# FinGramota

- Frontend: http://37.140.243.205/
- API base: http://37.140.243.205/api/
- Swagger: http://37.140.243.205/api/docs/
- OpenAPI schema: http://37.140.243.205/api/schema/
- Backend health: http://37.140.243.205/api/health/

API prefixes:

- Authentication: `/api/auth/`
- Users: `/api/users/`
- Verification: `/api/verification/`
- Marketplace: `/api/marketplace/`

Локальный запуск бэкенда:

`docker compose -f .\docker-fingramota\docker-compose.yml -f .\docker-fingramota\docker-compose.override.yml up -d --build backend`

Применить миграции базы данных на сервере:

`docker compose -f docker-fingramota/docker-compose.yml exec backend python manage.py migrate --noinput`

Установить зависимости локального загрузчика VBR:

`npm --prefix .\backend\tools\vbr_capture install`

Получить актуальные страницы VBR через обычный Chrome:

`npm --prefix .\backend\tools\vbr_capture run capture`

Импортировать полученные продукты в PostgreSQL:

`docker compose -f .\docker-fingramota\docker-compose.yml -f .\docker-fingramota\docker-compose.override.yml exec backend python manage.py sync_marketplace_products`

После первого успешного запуска загрузчик можно запускать в headless-режиме:

`npm --prefix .\backend\tools\vbr_capture run capture -- --headless`