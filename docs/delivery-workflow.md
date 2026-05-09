# Delivery Workflow

The process of delivering a SaaS template from the marketplace to the customer.

## Current Manual Workflow

1. **Purchase Confirmation:** Verified via `purchases` app.
2. **License Issuance:** `licensing` app generates keys.
3. **Repository Access:** Support team grants access to a private GitHub repository or provides a zip archive.
4. **Setup Support:** Manual tracking via `deployments.models.DeploymentRequest`.

## Customization Boundaries

- **Standard:** The template as-is.
- **Managed:** Includes basic setup and branding by our team.
- **Custom:** Bespoke features added via `support.models.CustomizationRequest`.

## Update Policy

Purchasers are entitled to updates within the same major version of the template for a period specified in their license.

## Entitlement and License Issuance

As part of the delivery workflow, the system performs the following steps:
1. Validates the `TemplatePurchase`.
2. Calls `issue_license_for_purchase()` to generate a secure license key.
3. Associates the license with the user and their organization (if applicable).
4. Includes the license key in the delivery artifacts or project configuration.
