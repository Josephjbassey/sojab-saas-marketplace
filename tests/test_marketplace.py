import pytest
from django.urls import reverse
from apps.templates_catalog.models import SaaSTemplate, TemplateCategory, TemplatePackage
from apps.purchases.models import TemplatePurchase
from apps.support.models import CustomizationRequest


@pytest.mark.django_db
class TestCatalogFlow:
    def test_catalog_listing(self, client):
        url = reverse('templates_catalog:template_list')
        response = client.get(url)
        assert response.status_code == 200

    def test_template_detail(self, client, saas_template):
        url = reverse('templates_catalog:template_detail', kwargs={'slug': saas_template.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert saas_template.name in response.content.decode()

    def test_template_detail_invalid_slug_returns_404(self, client):
        url = reverse('templates_catalog:template_detail', kwargs={'slug': 'nonexistent-template'})
        response = client.get(url)
        assert response.status_code == 404

    def test_htmx_filter_returns_partial(self, client, saas_template):
        url = reverse('templates_catalog:template_list')
        response = client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200
        # HTMX responses use the partial template
        assert 'template_grid_items' in response.template_name[0] or 'template_grid_items.html' in str(response.templates)


@pytest.mark.django_db
class TestAuthFlow:
    def test_login_page_loads(self, client):
        url = reverse('accounts:login')
        response = client.get(url)
        assert response.status_code == 200

    def test_register_page_loads(self, client):
        url = reverse('accounts:register')
        response = client.get(url)
        assert response.status_code == 200

    def test_register_creates_user_with_auto_username(self, client):
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = client.post(url, data)
        assert response.status_code == 302  # Redirect after success
        from apps.accounts.models import User
        user = User.objects.get(email='newuser@example.com')
        assert user.username == 'newuser'

    def test_dashboard_requires_login(self, client):
        url = reverse('marketplace:dashboard')
        response = client.get(url)
        assert response.status_code == 302
        assert '/auth/login/' in response.url


@pytest.mark.django_db
class TestPurchaseFlow:
    def test_checkout_requires_login(self, client, template_package):
        url = reverse('purchases:checkout', kwargs={'package_id': template_package.id})
        response = client.get(url)
        assert response.status_code == 302

    def test_checkout_page_loads(self, authenticated_client, template_package):
        url = reverse('purchases:checkout', kwargs={'package_id': template_package.id})
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert template_package.template.name in response.content.decode()

    def test_checkout_creates_purchase(self, authenticated_client, template_package, user):
        url = reverse('purchases:checkout', kwargs={'package_id': template_package.id})
        response = authenticated_client.post(url)
        assert response.status_code == 302  # Redirect to success
        assert TemplatePurchase.objects.filter(user=user, package=template_package).exists()
        purchase = TemplatePurchase.objects.get(user=user, package=template_package)
        assert purchase.status == 'paid'
        assert purchase.transaction_id.startswith('dummy_')

    def test_duplicate_purchase_redirects(self, authenticated_client, purchase, template_package):
        url = reverse('purchases:checkout', kwargs={'package_id': template_package.id})
        response = authenticated_client.get(url)
        assert response.status_code == 302  # Redirect because already purchased

    def test_purchase_success_page(self, authenticated_client, purchase):
        url = reverse('purchases:success', kwargs={'purchase_id': purchase.id})
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert purchase.template.name in response.content.decode()


@pytest.mark.django_db
class TestCustomizationRequest:
    def test_customization_request_login_required(self, client, saas_template):
        url = reverse('support:customization_request', kwargs={'template_slug': saas_template.slug})
        response = client.get(url)
        assert response.status_code == 302

    def test_customization_request_submission(self, authenticated_client, saas_template):
        url = reverse('support:customization_request', kwargs={'template_slug': saas_template.slug})
        data = {
            'template': saas_template.id,
            'subject': 'Test Customization',
            'description': 'I need custom fields added.',
            'budget_expectation': 500.00,
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == 200
        assert CustomizationRequest.objects.count() == 1


@pytest.mark.django_db
class TestDashboard:
    def test_dashboard_shows_purchases(self, authenticated_client, purchase):
        url = reverse('marketplace:dashboard')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert purchase.template.name in response.content.decode()

    def test_dashboard_shows_projects(self, authenticated_client, client_project):
        url = reverse('marketplace:dashboard')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert client_project.name in response.content.decode()
