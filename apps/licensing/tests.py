import pytest
from django.utils import timezone
from .models import TemplateVersion, TemplateLicense
from .services import generate_license_key, issue_license_for_purchase, validate_license_key, revoke_license

@pytest.mark.django_db
class TestLicensingModels:
    def test_create_version(self, saas_template):
        version = TemplateVersion.objects.create(
            template=saas_template,
            version="1.0.0",
            release_date=timezone.now().date(),
            is_latest=True
        )
        assert str(version) == f"{saas_template.name} v1.0.0"
        assert version.is_latest is True

    def test_latest_version_behavior(self, saas_template):
        v1 = TemplateVersion.objects.create(
            template=saas_template,
            version="1.0.0",
            release_date=timezone.now().date(),
            is_latest=True
        )
        v2 = TemplateVersion.objects.create(
            template=saas_template,
            version="1.1.0",
            release_date=timezone.now().date(),
            is_latest=True
        )
        v1.refresh_from_db()
        assert v1.is_latest is False
        assert v2.is_latest is True

@pytest.mark.django_db
class TestLicensingServices:
    def test_generate_license_key(self):
        key = generate_license_key()
        assert key.startswith("SaaS-")
        assert len(key.split("-")) == 4

    def test_issue_license_for_purchase(self, purchase):
        license = issue_license_for_purchase(purchase)
        assert license.purchase == purchase
        assert license.template == purchase.template
        assert license.user == purchase.user
        assert license.status == TemplateLicense.STATUS_ACTIVE

    def test_validate_license_key(self, purchase):
        license = issue_license_for_purchase(purchase)

        # Valid key
        valid_license, error = validate_license_key(license.license_key, license.template)
        assert valid_license == license
        assert error is None

        # Invalid key
        none_license, error = validate_license_key("invalid-key")
        assert none_license is None
        assert "not found" in error

    def test_revoke_license(self, purchase):
        license = issue_license_for_purchase(purchase)
        revoke_license(license, reason="Refunded")
        assert license.status == TemplateLicense.STATUS_REVOKED
        assert license.metadata['revocation_reason'] == "Refunded"

    def test_organization_linked_license(self, purchase, organization):
        purchase.organization = organization
        purchase.save()

        license = issue_license_for_purchase(purchase)
        assert license.organization == organization
