# Audit Logging Foundation

Phase 5 implements a central audit logging system to track important events across the marketplace.

## Architecture

The system consists of:
- **AuditLog Model**: Stores event details, actor, organization, resource, and request context (IP, User Agent).
- **Service Function**: `log_action` provides a simple interface to record events.
- **Admin Interface**: A read-only view in the Django admin to monitor logs.

## AuditLog Model Fields

- `actor`: The user who performed the action (nullable for system events).
- `organization`: The organization associated with the event (nullable).
- `action`: The type of action (e.g., `register`, `payment_completed`).
- `resource_type`: The name of the model being acted upon.
- `resource_id`: The primary key of the resource.
- `message`: A human-readable description.
- `metadata`: JSON field for additional event-specific data.
- `ip_address`: Captured from the request.
- `user_agent`: Captured from the request.
- `created_at`: Timestamp of the event.

## Usage

Use the `log_action` service to record events in views or other services.

```python
from apps.audit.services import log_action

log_action(
    actor=request.user,
    action='payment_completed',
    resource=purchase,
    message=f"Payment completed for {package.name}",
    request=request,
    metadata={"purchase_id": str(purchase.id)}
)
```

## Action Choices

- `create`, `update`, `delete`
- `login`, `logout`, `register`
- `password_change`
- `permission_granted`, `permission_revoked`
- `payment_initiated`, `payment_completed`, `payment_failed`
- `customization_request_created`
- `deployment_request_created`
- `file_uploaded`, `file_deleted`
