# Agency CRM SaaS Template

A professional, multi-tenant CRM foundation designed for digital agencies, freelancers, and service businesses. Built with **Django 6.x**, **Wagtail CMS**, **Tailwind CSS v4**, and **HTMX**.

## What this template does
This template provides a ready-to-use SaaS architecture for managing the lifecycle of agency operations:
- **Lead Pipeline**: Track potential deals from discovery to closing.
- **Client Management**: Maintain a central database of clients and their primary contacts.
- **Project Workspaces**: Manage delivery statuses for active projects.
- **Invoicing**: Track billing history and payment statuses.
- **Multi-tenancy**: Built-in isolation for organizations and their members.
- **Marketing CMS**: Integrated Wagtail CMS for high-performance marketing pages.

## Who it is for
- **Digital Agencies** looking for a customizable internal tool.
- **SaaS Founders** needing a boilerplate for a multi-tenant B2B application.
- **Freelancers** managing multiple clients and projects.

## Installation & Setup

### 1. Prerequisites
- Python 3.12+
- Docker & Docker Compose (for PostgreSQL/Redis)

### 2. Environment Setup
Copy the example environment file and install dependencies:
```bash
cp .env.example .env
pip install -r requirements.txt
```

### 3. Database & Services
Start the required services using Docker:
```bash
docker compose -f docker-compose.example.yml up -d
```

Run migrations to set up the database schema:
```bash
python manage.py migrate
# OR using Makefile:
make migrate
```

### 4. Seed Demo Data
Populate the database with demo organizations, clients, and leads:
```bash
python seed_crm_data.py
# OR using Makefile:
make seed
```
*Note: This command will output a randomly generated admin password.*

### 5. Create a Superuser
If you prefer to create your own admin account:
```bash
python manage.py createsuperuser
# OR using Makefile:
make superuser
```

## Running the Application
Start the development server:
```bash
python manage.py runserver
# OR using Makefile:
make dev
```
Access the dashboard at `http://localhost:8000/dashboard/` and the admin panel at `http://localhost:8000/django-admin/`.

## Testing
Verify the application integrity with pytest:
```bash
pytest tests.py
# OR using Makefile:
make test
```

## Makefile Commands
A Makefile is provided for common development tasks:
- `make init`: Full setup (env, dependencies, containers).
- `make dev`: Start the local server.
- `make test`: Run the test suite.
- `make migrate`: Apply database changes.
- `make seed`: Load demo CRM data.
- `make check`: Run Django system checks.

## Project Structure
- `apps/accounts`: User authentication and profiles.
- `apps/organizations`: Workspace isolation and membership.
- `apps/leads`: Sales pipeline tracking.
- `apps/clients`: Client management.
- `apps/projects`: Project delivery tracking.
- `apps/invoices`: Billing and financial records.
- `apps/cms`: Wagtail CMS integration.

## License
Commercial - See [template.json](template.json) for details.
