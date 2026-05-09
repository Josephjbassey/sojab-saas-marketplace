# Organizations and Workspaces

This document explains the Organization and Membership system implemented in the marketplace to support business and team clients.

## Overview

The marketplace supports multi-tenancy through **Organizations** (also referred to as Workspaces). This allows users to group their purchases, projects, and requests under a shared entity, facilitating team collaboration.

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

## Roles and Permissions

- **Owner**: Full control over the organization, including billing and membership management. Usually the creator of the organization.
- **Admin**: Can manage projects and requests within the organization, and invite new members.
- **Member**: Can view and interact with shared projects but cannot manage the organization itself.

## Integration

Key models in the marketplace have been updated to support optional organization ownership:
- **Template Purchases**: Can be owned by an organization for shared licensing.
- **Client Projects**: Can be managed at the organization level.
- **Customization Requests**: Can be submitted on behalf of an organization.
- **Deployment Requests**: Can be linked to an organization for team visibility.

## Roadmap

Future updates will include:
1. **Team Dashboard**: A view for members to see all shared assets.
2. **Invitation System**: Allow owners and admins to invite users via email.
3. **Role-Based Access Control (RBAC)**: Fine-grained permissions for specific actions within the marketplace.
4. **Shared Billing**: Consolidate payments at the organization level.
