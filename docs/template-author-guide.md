# Template Author Guide

This guide is for developers creating new SaaS templates for the marketplace.

## Requirements

Templates must adhere to the following standards:
- **Standalone:** Must be runnable independently of the marketplace.
- **Standardized Manifest:** Must include a `template.json` file following our [Schema](../schemas/template.schema.json).
- **Documentation:** Must include internal documentation for the end-user.
- **Stack:** Standardized on Django, Postgres, Redis, and Tailwind CSS.

## Versioning & Changelog

- Use Semantic Versioning (SemVer) for templates.
- Maintain a `CHANGELOG.md` within the template directory.
- Updates to templates should be non-breaking for existing installations where possible.

## Licensing

- Authors must specify the `license_type` in the manifest.
- All third-party dependencies must be declared and compliant with the template's license.

## Third-Party Template Licensing Disclaimer

Any submitted template that includes third-party code, themes, UI kits, images, fonts, or other assets must include a clear licensing disclaimer in its own documentation. Authors are solely responsible for ensuring redistribution rights and license compliance for all bundled assets.
