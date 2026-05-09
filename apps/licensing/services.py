import uuid
import secrets
from django.utils import timezone
from .models import TemplateLicense

def generate_license_key():
    """
    Generates a secure random license key.
    Format: SaaS-XXXX-XXXX-XXXX
    """
    parts = [secrets.token_hex(4).upper() for _ in range(3)]
    return f"SaaS-{' '.join(parts).replace(' ', '-')}"

def issue_license_for_purchase(purchase):
    """
    Issues a template license for a completed purchase.
    """
    license_type = purchase.package.license_type or TemplateLicense.TYPE_PERSONAL
    allowed_end_products = 10 if license_type == TemplateLicense.TYPE_AGENCY else 1

    license = TemplateLicense.objects.create(
        license_key=generate_license_key(),
        template=purchase.template,
        purchase=purchase,
        user=purchase.user,
        organization=purchase.organization,
        license_type=license_type,
        allowed_end_products=allowed_end_products,
        status=TemplateLicense.STATUS_ACTIVE
    )
    return license

def validate_license_key(license_key, template=None):
    """
    Validates a license key and returns the license object if valid.
    """
    try:
        license = TemplateLicense.objects.get(license_key=license_key)

        # Basic checks
        if not license.is_active:
            return None, "License is not active."

        if template and license.template != template:
            return None, "License is for a different template."

        if license.expires_at and license.expires_at < timezone.now():
            license.status = TemplateLicense.STATUS_EXPIRED
            license.save(update_fields=['status', 'updated_at'])
            return None, "License has expired."

        return license, None
    except TemplateLicense.DoesNotExist:
        return None, "License key not found."

def revoke_license(license, reason=""):
    """
    Revokes a license and records the reason in metadata.
    """
    license.status = TemplateLicense.STATUS_REVOKED
    license.metadata['revocation_reason'] = reason
    license.metadata['revoked_at'] = timezone.now().isoformat()
    license.save(update_fields=['status', 'metadata', 'updated_at'])
    return license
