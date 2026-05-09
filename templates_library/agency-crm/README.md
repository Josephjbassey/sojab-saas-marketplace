# Agency CRM SaaS Boilerplate

A professional Agency CRM built with Django, Wagtail, and HTMX.

## Features
- **Standalone Django SaaS**: Fully self-contained project structure.
- **Client Management**: Track leads, contacts, and customer history.
- **Lead Pipeline**: Kanban-style visual pipeline for tracking opportunities.
- **Project Tracking**: Manage tasks, deadlines, and deliverables.
- **Workspace Support**: Multi-tenancy ready for agency teams.
- **Modern Stack**: Tailwind CSS v4, HTMX, Alpine.js, and Wagtail CMS.
- **Production Ready**: Optimized for Docker, PostgreSQL, and Redis.

## Getting Started

### 1. Initialize
```bash
make init
```
*Note: This will use the provided docker-compose.example.yml*

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Seed Data
```bash
python seed_crm_data.py
```

### 4. Start Development
```bash
make dev
```

## Documentation
See the `docs/` folder for detailed guides on project structure, customization, and deployment.
