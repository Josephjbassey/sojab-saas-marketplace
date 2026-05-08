# Billing Architecture

The platform uses an abstraction layer for billing to support multiple payment providers.

## Abstraction Layer

The `apps.billing` module defines a standard interface for:
- Creating checkout sessions.
- Handling webhooks.
- Managing subscriptions vs. one-time purchases.

## Supported Providers

- **Stub/Dummy (Current MVP):** Used for development and testing. This is the only currently active provider.

## Planned Providers (Future)

- **Stripe:** Planned for international payments.
- **Paystack:** Planned for regional markets.

## Transaction Flow

1. User selects a template package.
2. `purchases.views.checkout` initiates the billing session.
3. Upon success, a `TemplatePurchase` is recorded.
4. The `licensing` app generates a license key.
5. The `deployments` app creates a delivery task.
