from django.utils.text import slugify
from .models import Organization, Membership

def create_default_organization(user):
    """
    Creates a personal organization for a user and assigns them as owner.
    """
    name = f"{user.get_full_name() or user.username}'s Workspace"
    slug = slugify(name)

    # Ensure slug uniqueness if necessary, though simple slugify is usually fine for personal workspaces
    base_slug = slug
    counter = 1
    while Organization.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    organization = Organization.objects.create(
        name=name,
        slug=slug
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role='owner'
    )

    return organization
