# Production Checklist

Steps to ensure the platform is ready for production deployment.

## Environment & Security

- [ ] Set `DEBUG=False`.
- [ ] Generate a secure `SECRET_KEY`.
- [ ] Configure `ALLOWED_HOSTS` (Do not use wildcard `*`).
- [ ] Enable HTTPS/SSL (`SECURE_SSL_REDIRECT=True`).
- [ ] Enable HSTS (`SECURE_HSTS_SECONDS=31536000` or similar).
- [ ] Configure `CSRF_TRUSTED_ORIGINS`.
- [ ] Set up Sentry for error tracking.
- [ ] **Rate Limiting**: Install and configure `django-ratelimit` or `django-axes` to protect auth endpoints (login, register).
- [ ] **Webhook Security**: Ensure all webhook adapters (Paystack, Stripe) implement HMAC signature verification using the provider's secret.

## Database & Services

- [ ] Use a managed Postgres instance.
- [ ] Configure persistent Redis for Celery and Caching.
- [ ] Set up automated database backups.

## Payments & Licensing

- [ ] Switch billing to Live Mode (Real API Keys).
- [ ] Verify webhook endpoints are reachable by providers.
- [ ] Audit license generation logic for high-volume scenarios.

## Monitoring & Health

- [ ] Configure load balancer or orchestrator to use health endpoints:
  - `/health/live/`: Liveness probe (app running).
  - `/health/ready/`: Readiness probe (DB/Redis connectivity).
  - `/health/`: Detailed status.
