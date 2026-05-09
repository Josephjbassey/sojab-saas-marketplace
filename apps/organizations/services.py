from django.db import transaction
from django.utils.text import slugify
from .models import Organization, Membership

def create_default_organization_for_user(user):
    """
    Creates a default personal organization for a new user.
    """
    name = f"{user.get_full_name() or user.username}'s Workspace"
    slug = slugify(name)

    # Handle slug collisions if necessary
    base_slug = slug
    counter = 1
    while Organization.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    with transaction.atomic():
        org = Organization.objects.create(
            name=name,
            slug=slug,
            owner=user
        )
        Membership.objects.create(
            user=user,
            organization=org,
            role=Membership.ROLE_OWNER
        )
    return org

def add_member_to_organization(organization, user, role=Membership.ROLE_MEMBER):
    """
    Adds a user to an organization with a specific role.
    """
    membership, created = Membership.objects.get_or_create(
        user=user,
        organization=organization,
        defaults={'role': role}
    )
    if not created and membership.role != role:
        membership.role = role
        membership.save()
    return membership

def get_user_organizations(user):
    """
    Returns all organizations a user belongs to.
    """
    return Organization.objects.filter(memberships__user=user, is_active=True)

def user_has_role(user, organization, roles):
    """
    Checks if a user has one of the specified roles in an organization.
    """
    if isinstance(roles, str):
        roles = [roles]
    return Membership.objects.filter(
        user=user,
        organization=organization,
        role__in=roles
    ).exists()
