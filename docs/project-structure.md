# Project Structure

The repository is organized into a modular Django architecture to support a marketplace model.

## Layer 1: Marketplace Platform

Located in the `apps/` directory:
- `accounts`: Custom user management.
- `billing`: Abstracted payment processing.
- `cms`: Wagtail CMS for content management.
- `deployments`: Tracking delivery and setup requests.
- `licensing`: License key generation and validation.
- `marketplace`: Core platform views.
- `organizations`: Workspace and team management.
- `purchases`: Transaction and order history.
- `templates_catalog`: Metadata and listing of available SaaS templates.

## Layer 2: SaaS Template Boilerplates

Templates are stored (or referenced) in the `templates_library/` directory. Each template is a standalone Django project designed to be cloned and customized for the end-user.

Each template must include:
- `README.md`
- `.env.example`
- `Dockerfile` & `docker-compose.yml`
- `Makefile`
- `seed_data.py`
- A test suite.
