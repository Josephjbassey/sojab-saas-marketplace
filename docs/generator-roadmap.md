# Project Generator Roadmap

The project generator facilitates the configuration and delivery of SaaS template instances to clients.

## Implementation Status: Phase 10 (Foundation)
- [x] **Core Models**: `GeneratedProject` for lifecycle tracking and `ProjectConfiguration` for settings.
- [x] **Admin Workflow**: Manual management of project statuses and delivery URLs/files in Django Admin.
- [x] **Service Stubs**: Basic helpers for creating projects and marking them delivered.

## Current Manual Workflow (Admin)
1. **Creation**: Admin creates a `GeneratedProject` from a successful `TemplatePurchase`.
2. **Configuration**: Admin (or later, the user) fills in `ProjectConfiguration` (brand name, colors, etc.).
3. **Processing**: Admin manually prepares the project (code generation, repo setup).
4. **Delivery**: Admin updates `github_repo_url`, `deployment_url`, or uploads a `zip_file`.
5. **Completion**: Admin sets status to `Delivered`.

## Future Automation Roadmap

### 1. Celery Automation (Next Phase)
- Move generation tasks to background workers.
- Add status updates (`Queued`, `Preparing`) via Celery task signals.

### 2. Actual Code Generation
- Implement a template engine to transform the base boilerplate based on `ProjectConfiguration`.
- Dynamic replacement of brand names, primary colors, and feature flags.

### 3. Automated Delivery
- **GitHub Provisioning**: Automated creation of private repositories via GitHub API.
- **Zip Export**: Dynamic creation and storage of project archives using `apps/files`.
- **One-Click Deploy**: Webhook-based integration with Vercel/Railway for instant provisioning.
