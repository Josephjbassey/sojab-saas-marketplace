import pytest
from django.urls import reverse
from apps.templates_catalog.models import SaaSTemplate, TemplateCategory, TemplatePackage
from apps.support.models import CustomizationRequest

@pytest.mark.django_db
class TestMarketplaceFlow:
    def test_catalog_listing(self, client):
        url = reverse('templates_catalog:template_list')
        response = client.get(url)
        assert response.status_code == 200

    def test_template_detail(self, client, db_setup):
        template = SaaSTemplate.objects.first()
        url = reverse('templates_catalog:template_detail', kwargs={'slug': template.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert template.name in response.content.decode()

    def test_customization_request_login_required(self, client, db_setup):
        template = SaaSTemplate.objects.first()
        url = reverse('support:customization_request', kwargs={'template_slug': template.slug})
        response = client.get(url)
        assert response.status_code == 302 # Redirect to login

    def test_customization_request_submission(self, admin_client, db_setup):
        template = SaaSTemplate.objects.first()
        url = reverse('support:customization_request', kwargs={'template_slug': template.slug})
        data = {
            'subject': 'Test Customization',
            'description': 'I need some custom fields added to the user profile.',
            'budget_expectation': 500.00
        }
        response = admin_client.post(url, data)
        assert response.status_code == 200 # Success template
        assert CustomizationRequest.objects.count() == 1

@pytest.fixture
def db_setup(db):
    # This fixture can be expanded to create minimal test data if not using seed_data.py for tests
    # But for MVP verification, we expect seed_data to be run or handled in conftest
    pass
