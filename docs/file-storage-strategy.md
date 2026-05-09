# File Storage Strategy

The platform uses a managed file abstraction to handle template assets, client brand materials, and delivery ZIPs.

## Current Implementation

We currently use the standard `django.core.files.storage.FileSystemStorage` for local development. Files are stored in the `media/` directory.

### ManagedFile Model

The `apps.files.ManagedFile` model tracks all uploaded assets with metadata:
- **Purpose**: Categorizes files (e.g., `template_screenshot`, `delivery_zip`).
- **Ownership**: Tracks which user or organization owns the asset.
- **Validation**: Enforces size limits (default 50MB) and tracks MIME types.

### Service Layer

Always use the service helpers in `apps/files/services.py` to manage files:
- `save_managed_file()`: Handles the record creation and file persistence.
- `get_file_url()`: Retrieves the access URL.
- `delete_managed_file()`: Ensures both the DB record and the physical file are removed.

## Roadmap: Cloudflare R2 / S3

For production, we will migrate to Cloudflare R2 (or any S3-compatible storage) using `django-storages`.

### Planned Changes
1. Install `django-storages[s3]`.
2. Configure `STORAGES` in `settings.py` to use `S3Storage`.
3. Update `get_file_url()` to support presigned URLs for private assets (like delivery ZIPs).
4. Implement lifecycle policies in R2 for temporary files.
