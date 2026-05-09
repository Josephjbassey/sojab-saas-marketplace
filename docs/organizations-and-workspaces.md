# Organizations and Workspaces

The marketplace supports multi-tenant workspaces through the **Organizations** and **Memberships** models. This enables business clients to manage projects, purchases, and requests as teams.

## Models

### Organization
Represents a workspace or company.
- `name`: Human-readable name.
- `slug`: URL-friendly identifier.
- `owner`: The primary user responsible for the organization.
- `is_active`: Toggle for workspace access.

### Membership
Connects users to organizations with specific roles.
- `user`: Reference to the User.
- `organization`: Reference to the Organization.
- `role`: One of `owner`, `admin`, `member`, or `guest`.

## Roles and Permissions

- **Owner**: Full control over the organization, including billing and member management.
- **Admin**: Can manage projects and customization requests within the organization.
- **Member**: Can view resources and participate in assigned projects.
- **Guest**: Limited view access to specific shared resources.

## Services and Helpers

The system provides several service functions in `apps/organizations/services.py` to manage organizations:

- `create_default_organization_for_user(user)`: Automatically creates a personal workspace for a new user.
- `add_member_to_organization(organization, user, role)`: Handles adding or updating memberships.
- `get_user_organizations(user)`: Retrieves all active organizations the user belongs to.
- `user_has_role(user, organization, roles)`: Helper to check permissions.

## Architecture

The system is designed to support a transition from user-owned resources to organization-owned resources.
Existing models (`TemplatePurchase`, `CustomizationRequest`, `ClientProject`, `DeploymentRequest`) include an optional `organization` field.

When an organization is associated with a resource, access logic should prioritize membership-based checks over direct user ownership.

## Role-Based Access Control (RBAC)

Phase 2 introduces lightweight RBAC helpers in `apps/organizations/permissions.py`. These functions provide a centralized way to check user permissions against organizations and their associated resources (like projects).

### Core Helpers

- `is_organization_owner(user, organization)`: Checks if the user has the 'Owner' role.
- `is_organization_admin(user, organization)`: Checks if the user has the 'Admin' role.
- `is_organization_member(user, organization)`: Checks if the user is any member of the organization.
- `can_view_organization(user, organization)`: Permission to view organization details (all members).
- `can_manage_organization(user, organization)`: Permission to change settings (Owners & Admins).
- `can_manage_members(user, organization)`: Permission to invite/remove members (Owners & Admins).
- `can_manage_billing(user, organization)`: Permission to manage payments (Owners & Admins).

### Resource Helpers

- `can_view_project(user, project)`: Returns True if the user owns the project or belongs to the organization that owns it.
- `can_manage_project(user, project)`: Returns True if the user owns the project or has management rights (Owner/Admin) in the project's organization.

### Implementation Note

This system uses a "Role-to-Action" mapping within the helper functions. While it is not yet a full-blown permission engine (where actions are granular database objects), it provides a robust and easy-to-use foundation for most SaaS requirements.
