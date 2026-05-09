# Organizations and Workspaces

The marketplace supports multi-tenant workspaces through the **Organizations** and **Memberships** models.

## Models

### Organization
Represents a workspace or company.
- `name`: Human-readable name.
- `slug`: URL-friendly identifier.
- `is_active`: Toggle for workspace access.

### Membership
Connects users to organizations with specific roles.
- `user`: Reference to the User.
- `organization`: Reference to the Organization.
- `role`: One of `owner`, `admin`, or `member`.

## Roles and Permissions

- **Owner**: Full control over the organization, including billing and member management.
- **Admin**: Can manage projects and customization requests within the organization.
- **Member**: Can view resources and participate in assigned projects.

## Architecture

The system is designed to support future migration from user-owned resources to organization-owned resources.
Existing models (`TemplatePurchase`, `CustomizationRequest`, `ClientProject`, `DeploymentRequest`) now include an optional `organization` field.

When an organization is associated with a resource, access logic should prefer membership-based checks over direct user ownership.
