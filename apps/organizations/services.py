from django.db import transaction, IntegrityError
from django.utils.text import slugify
from .models import Organization, Membership

def create_default_organization(user):
    """
    Creates a personal organization for a user and assigns them as owner.
    Uses an atomic transaction and retry logic to handle slug collisions safely.
    """
    base_name = f"{user.get_full_name() or user.username}'s Workspace"
    base_slug = slugify(base_name)

    max_retries = 10
    for i in range(max_retries):
        slug = base_slug if i == 0 else f"{base_slug}-{i}"

        try:
            with transaction.atomic():
                organization = Organization.objects.create(
                    name=base_name,
                    slug=slug
                )
                Membership.objects.create(
                    user=user,
                    organization=organization,
                    role='owner'
                )
                return organization
        except IntegrityError:
            # Continue to next iteration if slug collision occurred
            if i == max_retries - 1:
                raise
            continue
