# Organizations and Workspaces

This document explains the Organization and Membership system implemented in the marketplace to support business and team clients.

## Overview

The marketplace supports multi-tenancy through **Organizations** (also referred to as Workspaces). This allows users to group their purchases, projects, and requests under a shared entity.

## Data Model

### Organization
Represents a business or team entity.
- `name`: The display name of the organization.
- `slug`: A unique URL-friendly identifier.
- `is_active`: Boolean flag to enable or disable the organization.

### Membership
Connects Users to Organizations with specific roles.
- `user`: The marketplace user.
- `organization`: The organization the user belongs to.
- `role`: One of `owner`, `admin`, or `member`.

## Roles and Intent

Current roles are defined to facilitate future permission checks. **Note: RBAC (Role-Based Access Control) enforcement is planned for a future update and is not yet active in the core marketplace logic.**

- **Owner**: Intended for full control over the organization, including billing and membership management.
- **Admin**: Intended for managing projects and requests within the organization.
- **Member**: Intended for viewing and interacting with shared projects.

## Integration

Key models in the marketplace support optional organization ownership:
- **Template Purchases**: Can be associated with an organization.
- **Client Projects**: Can be associated with an organization.
- **Customization Requests**: Can be associated with an organization.
- **Deployment Requests**: Can be associated with an organization.

Existing logic remains user-centric; organization-based access and shared visibility will be introduced in subsequent PRs.

## Roadmap

The following features are planned to build upon this foundation:
1. **Team Dashboard**: A view for members to see all shared assets.
2. **RBAC Enforcement**: Fine-grained permissions based on the `Membership.role`.
3. **Invitation System**: Allow owners and admins to invite users via email.
4. **Shared Billing**: Consolidate payments at the organization level.
