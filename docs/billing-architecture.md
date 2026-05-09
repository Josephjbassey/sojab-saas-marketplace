# Billing Architecture

The platform uses an abstraction layer for billing to support multiple payment providers. This allows us to maintain a consistent interface while swapping out the underlying gateway (e.g., Stripe, Paystack).

## Provider Interface

All payment providers must implement the `BasePaymentProvider` interface defined in `apps/billing/services.py`:

- `create_payment(purchase, amount)`: Initiates the payment process.
- `confirm_payment(purchase)`: Finalizes a pending payment.
- `refund_purchase(purchase)`: Handles refund requests.

## Models

### PaymentTransaction
Logs every attempt at a payment, including the provider used, external transaction ID, and final status. This provides an audit trail separate from the high-level `TemplatePurchase` state.

### WebhookEvent
A landing table for raw gateway notifications. In Phase 3, this is a placeholder to ensure the architecture is ready for asynchronous payment confirmations.

## Current Provider

- **Dummy (Active):** Simulates successful and failed transactions without external API calls. Enabled via `DUMMY_PAYMENTS_ENABLED` in settings.

## Roadmap

- **Phase 4:** Add real `PaystackProvider` with webhook support.
- **Phase 5:** Add `StripeProvider`.
- **Phase 6:** Implement Subscription-specific logic (plans, intervals).

## Webhook Integration Strategy

Future providers will push events to a unified endpoint (`/billing/webhooks/<provider>/`). The logic will:
1. Validate the signature.
2. Store the raw payload in `WebhookEvent`.
3. Dispatch a background task to update the relevant `TemplatePurchase` and `PaymentTransaction`.

## Paystack Integration (Phase 12)

The marketplace now supports Paystack for real payments.

### Setup
1. Register for a Paystack account at [paystack.com](https://paystack.com).
2. Obtain your **Secret Key** and **Public Key** from the dashboard.
3. Configure the following environment variables:
   - `PAYSTACK_PUBLIC_KEY`: Your public key.
   - `PAYSTACK_SECRET_KEY`: Your secret key.
   - `PAYSTACK_CALLBACK_URL`: Set this to `https://yourdomain.com/billing/paystack/callback/`.
   - `ACTIVE_PAYMENT_PROVIDER`: Set to `paystack` to enable.

### Webhooks
Paystack webhooks are used to ensure payments are recorded even if the user closes the browser before redirection.
- Endpoint: `/billing/paystack/webhook/`
- Security: All requests are verified using the `HTTP_X_PAYSTACK_SIGNATURE` header.

### Test vs Live Mode
- Use `pk_test_...` and `sk_test_...` keys for development.
- Switch to live keys for production.
- Ensure your `PAYSTACK_CALLBACK_URL` matches the environment (localhost for dev, real domain for prod).
