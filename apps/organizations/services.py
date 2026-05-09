from django.db import IntegrityError, transaction
from django.utils.text import slugify
from .models import Organization, Membership


def create_default_organization_for_user(user):
    """
    Creates a default personal organization for a new user.
    """
    name = f"{user.get_full_name() or user.username}'s Workspace"
    base_slug = slugify(name)
    counter = 0

    while True:
        slug = base_slug if counter == 0 else f"{base_slug}-{counter}"
        try:
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
        except IntegrityError:
            if not Organization.objects.filter(slug=slug).exists():
                raise
            counter += 1


def add_member_to_organization(organization, user, role=Membership.ROLE_MEMBER):
    """
    Adds a user to an organization with a specific role.
    """
    with transaction.atomic():
        membership, created = Membership.objects.get_or_create(
            user=user,
            organization=organization,
            defaults={'role': role}
        )
        if not created and membership.role != role:
            membership.role = role
            membership.save(update_fields=['role'])

        if role == Membership.ROLE_OWNER and organization.owner_id != user.id:
            organization.owner = user
            organization.save(update_fields=['owner'])

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
