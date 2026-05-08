# Troubleshooting

Common issues and their resolutions.

## Environment Issues

- **Docker containers won't start:** Check `docker-compose logs`. Ensure ports 8001 (Web) and 5436 (DB) are free.
- **Database Connection Refused:** Ensure the `db` container is healthy before starting `web`.

## Celery Tasks

- **Tasks not executing:** Verify the `celery` container is running and connected to Redis.
- **Broker Connection Error:** Check `CELERY_BROKER_URL` in `.env`.

## Wagtail/CMS

- **Images not loading:** Ensure `MEDIA_ROOT` and `MEDIA_URL` are correctly configured.
- **Page Not Found:** Verify the Wagtail site settings in the admin dashboard.
