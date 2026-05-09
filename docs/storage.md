# Storage Strategy

This document outlines the file storage strategy for the SaaS Marketplace.

## Current Implementation: Local Storage

For development and early MVP stages, the project uses local file system storage.

- **Storage Backend**: `django.core.files.storage.FileSystemStorage`
- **Media Root**: `media/` directory in the project root.
- **Media URL**: `/media/`
- **Model**: `ManagedFile` in `apps.files` handles file metadata and organization/user associations.

## Production Roadmap: Cloudflare R2 / S3

The architecture is designed to easily transition to S3-compatible storage like Cloudflare R2.

### Target: Cloudflare R2

Cloudflare R2 is preferred for its zero egress fees and S3-compatible API.

### Migration Plan

1. **Install dependencies**:
   ```bash
   pip install django-storages[boto3]
   ```

2. **Update `settings.py`**:
   Configure `STORAGES` to use `storages.backends.s3boto3.S3Boto3Storage`.

3. **Required Environment Variables**:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_STORAGE_BUCKET_NAME`
   - `AWS_S3_ENDPOINT_URL` (e.g., `https://<account_id>.r2.cloudflarestorage.com`)
   - `AWS_S3_CUSTOM_DOMAIN` (optional, for CDN)

## ManagedFile Usage

Always use the `apps.files.services` helpers to interact with files to ensure consistency and future-proofing.

- `save_managed_file(file_obj, purpose, owner, organization)`: Saves a file.
- `get_file_url(managed_file_id)`: Retrieves the public/signed URL.
- `delete_managed_file(managed_file_id)`: Deletes metadata and physical file.

### File Purposes

- `template_screenshot`: Screenshots of SaaS templates.
- `client_brand_asset`: Logos and assets uploaded by organizations.
- `delivery_zip`: Final source code bundles for delivery.
- `invoice`: Generated billing documents.
- `document`: General project documentation.
- `other`: Default fallback.
