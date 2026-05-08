# Production Checklist

Steps to ensure the platform is ready for production deployment.

## Environment & Security

- [ ] Set `DEBUG=False`.
- [ ] Generate a secure `SECRET_KEY`.
- [ ] Configure `ALLOWED_HOSTS`.
- [ ] Enable HTTPS/SSL.
- [ ] Set up Sentry for error tracking.

## Database & Services

- [ ] Use a managed Postgres instance.
- [ ] Configure persistent Redis for Celery and Caching.
- [ ] Set up automated database backups.

## Payments & Licensing

- [ ] Switch billing to Live Mode.
- [ ] Verify webhook endpoints.
- [ ] Audit license generation logic.
