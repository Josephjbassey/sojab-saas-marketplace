# Customization Guide

## Branding
Update `WAGTAIL_SITE_NAME` in `.env` and replace logo assets in `static/brand/`.

## Pipelines
Modify the `STAGES` constant in `apps/pipelines/models.py` to customize your sales workflow.

## UI Styling
This project uses Tailwind CSS v4. Rebuild styles using the provided build script after modifying templates.
