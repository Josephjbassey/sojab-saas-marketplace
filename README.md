# Django SaaS Template Marketplace

A production-ready SaaS template marketplace MVP.

## Features
- Dynamic CMS managed via Wagtail.
- Core business logic in Django.
- HTMX and Tailwind CSS v4 frontend.
- Purchase flow with stubbed payments for the MVP.
- Client dashboard and manual deployment tracking.

## Documentation
- [Organizations and Workspaces](docs/organizations.md)

For detailed information on the architecture, development, and roadmap, please refer to the following documentation:

- [Getting Started](docs/getting-started.md)
- [Local Development Guide](docs/local-development.md)
- [Project Structure](docs/project-structure.md)
- [Template Customization](docs/template-customization.md)
- [Template Author Guide](docs/template-author-guide.md)
- [CMS Guide](docs/cms-guide.md)
- [Billing Architecture](docs/billing-architecture.md)
- [Delivery Workflow](docs/delivery-workflow.md)
- [Project Generator Roadmap](docs/generator-roadmap.md)
- [Production Checklist](docs/production-checklist.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Launch Roadmap](docs/launch-roadmap.md)

## App Responsibilities

This project is separated into distinct Django apps for maintainability:

- `accounts`: Handles Custom User model, login, signup, and basic profile views.
- `organizations`: (Reserved for future) for managing team/agency access if needed.
- `marketplace`: Public-facing views that are not directly CMS-based (e.g., search wrapper, some routing logic if not handled strictly by Wagtail).
- `templates_catalog`: Manages `SaaSTemplate`, `TemplateCategory`, `TemplateFeature`, `TemplateScreenshot`, and `TemplatePackage`.
- `purchases`: Manages the transactions (`TemplatePurchase`) and integrates with billing.
- `licensing`: Handles the issuance of valid license keys for the purchased templates.
- `billing`: Gateway for Stripe/Paystack. Currently configured with a stubbed dummy processor via `DUMMY_PAYMENTS_ENABLED`.
- `deployments`: Manages `DeploymentRequest` and `ClientProject` (tracking the manual delivery status and attaching code/URLs).
- `cms`: Wagtail configuration, global settings, standard page models, and block definitions.
- `support`: Holds internal requests like `CustomizationRequest`.
- `common`: The base layout, shared templates, template tags, and general utilities (HTMX integration).

## Quick Start

1. Copy the `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Build and start containers:
   ```bash
   docker compose up --build -d
   ```
3. Run migrations and create a superuser:
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```
4. Access:
   - Frontend: `http://localhost:8000`
   - Admin: `http://localhost:8000/admin`
   - CMS: `http://localhost:8000/cms`

## Testing
Run the test suite:
```bash
docker compose exec web pytest
```
