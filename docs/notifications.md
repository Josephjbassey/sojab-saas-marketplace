# Notification System

This document outlines the foundation of the notification system in the SaaS Marketplace platform.

## Overview

The notification system provides a centralized way to alert users about important events related to their account, organizations, and activity within the marketplace.

## Data Model

The core of the system is the `Notification` model:

- **Recipient**: The user who receives the notification.
- **Organization**: Optional link to an organization for context.
- **Type**:
  - `in_app`: Displayed within the user's dashboard.
  - `email`: Intended for external delivery (logic to be implemented in a future phase).
- **Title & Message**: The content of the alert.
- **Action URL**: Optional link for the user to follow.
- **Read Status**: Tracked via `read_at` timestamp.
- **Metadata**: JSON field for additional contextual data (e.g., related object IDs).

## Service Layer

Centralized logic is provided in `apps/notifications/services.py`:

- `create_notification`: Low-level creation of notification records.
- `notify_user`: Simple helper to alert a specific user.
- `notify_organization_admins`: Helper to alert all owners and admins of a given organization.
- `get_unread_count`: Utility to fetch the count of unread in-app notifications.

## Integrations

Currently, notifications are triggered during:

1. **Customization Requests**: User is notified when they submit a request.
2. **Purchases**: User is notified when a purchase is successfully completed or confirmed.

## Future Roadmap

- **WebSockets / Real-time**: Real-time push notifications using Django Channels.
- **Email Integration**: Sending `email` type notifications via a provider (e.g., Resend).
- **User Preferences**: Allowing users to opt-in/out of specific notification types.
- **Dashboard UI**: A dedicated notification center in the marketplace dashboard.
- **Batching**: Support for batched notifications to avoid noise.
