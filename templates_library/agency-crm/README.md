# Agency CRM SaaS Boilerplate

A robust, multi-tenant CRM foundation for digital agencies, built with Django 6.x, Wagtail CMS, Tailwind CSS v4, and HTMX.

## Features

- **Lead Management**: Track and search leads through the sales pipeline.
- **Client Portals**: Manage client profiles, projects, and invoices.
- **Project Tracking**: Monitor delivery status and project details.
- **Invoicing**: Simple billing history and payment status tracking.
- **Multi-tenancy**: Built-in Organization and Membership models for workspace isolation.
- **CMS Integration**: Wagtail-powered marketing and standard pages.
- **HTMX Interactions**: Dynamic search and status updates without full page reloads.
- **Clean UI**: Responsive design using Tailwind CSS v4.

## Quick Start

1. **Setup Environment**:
   ```bash
   cp .env.example .env
   ```

2. **Initialize Database**:
   ```bash
   python manage.py migrate
   ```

3. **Seed Demo Data**:
   ```bash
   python seed_crm_data.py
   ```
   *Note: This will print a generated admin password.*

4. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `apps/accounts`: Custom user model and authentication.
- `apps/organizations`: Multi-tenancy logic.
- `apps/clients`: Client management.
- `apps/leads`: Sales pipeline tracking.
- `apps/projects`: Delivery and project management.
- `apps/invoices`: Billing and invoices.
- `apps/cms`: Wagtail models and pages.
- `apps/common`: Shared layouts, components, and notes.

## Development

- **Tailwind CSS**: Uses the v4 browser-based compiler for rapid development.
- **HTMX**: Used for dynamic list filtering and status updates.
- **Tests**: Run `pytest tests.py` to verify core functionality.

## Deployment

Refer to [docs/deployment-guide.md](docs/deployment-guide.md) for instructions on deploying to Railway, Render, or Vercel.
