import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Organization, Membership
from .services import create_default_organization
from apps.purchases.models import TemplatePurchase
from apps.templates_catalog.models import SaaSTemplate, TemplatePackage, TemplateCategory
from apps.support.models import CustomizationRequest
from apps.deployments.models import ClientProject, DeploymentRequest

User = get_user_model()

@pytest.fixture
def setup_data(db):
    user = User.objects.create_user(username="testuser", email="test@example.com")
    org = Organization.objects.create(name="Acme Corp", slug="acme-corp")
    category = TemplateCategory.objects.create(name="SaaS", slug="saas")
    template = SaaSTemplate.objects.create(category=category, name="SaaS Pro", slug="saas-pro", description="A pro SaaS template")
    package = TemplatePackage.objects.create(template=template, name="Basic", price=99.00)
    return user, org, template, package

@pytest.mark.django_db
class TestOrganizationModels:
    def test_organization_creation(self):
        org = Organization.objects.create(name="Acme Corp", slug="acme-corp")
        assert org.name == "Acme Corp"
        assert org.slug == "acme-corp"
        assert org.is_active is True
        assert str(org) == "Acme Corp"

    def test_membership_creation_and_roles(self):
        user = User.objects.create_user(username="testuser", email="test@example.com")
        org = Organization.objects.create(name="Acme Corp", slug="acme-corp")

        membership = Membership.objects.create(user=user, organization=org, role='admin')
        assert membership.user == user
        assert membership.organization == org
        assert membership.role == 'admin'
        assert str(membership) == "test@example.com in Acme Corp (admin)"

    def test_unique_membership_constraint(self):
        user = User.objects.create_user(username="testuser", email="test@example.com")
        org = Organization.objects.create(name="Acme Corp", slug="acme-corp")
        Membership.objects.create(user=user, organization=org, role='member')

        with pytest.raises(IntegrityError):
            Membership.objects.create(user=user, organization=org, role='admin')

    def test_user_multiple_organizations(self):
        user = User.objects.create_user(username="testuser", email="test@example.com")
        org1 = Organization.objects.create(name="Org 1", slug="org-1")
        org2 = Organization.objects.create(name="Org 2", slug="org-2")

        Membership.objects.create(user=user, organization=org1, role='owner')
        Membership.objects.create(user=user, organization=org2, role='member')

        assert user.memberships.count() == 2

    def test_organization_multiple_members(self):
        org = Organization.objects.create(name="Acme Corp", slug="acme-corp")
        user1 = User.objects.create_user(username="user1", email="u1@example.com")
        user2 = User.objects.create_user(username="user2", email="u2@example.com")

        Membership.objects.create(user=user1, organization=org, role='owner')
        Membership.objects.create(user=user2, organization=org, role='member')

        assert org.memberships.count() == 2

@pytest.mark.django_db
class TestOrganizationServices:
    def test_create_default_organization(self):
        user = User.objects.create_user(username="testuser", first_name="John", last_name="Doe")
        org = create_default_organization(user)

        assert org.name == "John Doe's Workspace"
        assert org.slug == "john-does-workspace"

        membership = Membership.objects.get(user=user, organization=org)
        assert membership.role == 'owner'

    def test_create_default_organization_duplicate_slug_handling(self):
        user1 = User.objects.create_user(username="testuser1", first_name="John", last_name="Doe")
        user2 = User.objects.create_user(username="testuser2", first_name="John", last_name="Doe")

        org1 = create_default_organization(user1)
        org2 = create_default_organization(user2)

        assert org1.slug == "john-does-workspace"
        assert org2.slug == "john-does-workspace-1"

@pytest.mark.django_db
class TestOrganizationIntegration:
    def test_organization_associated_records(self, setup_data):
        user, org, template, package = setup_data

        purchase = TemplatePurchase.objects.create(
            user=user, organization=org, template=template, package=package, amount_paid=99.00, status='paid'
        )
        assert purchase.organization == org

        request = CustomizationRequest.objects.create(
            user=user, organization=org, template=template, subject="Test", description="Help"
        )
        assert request.organization == org

        project = ClientProject.objects.create(
            user=user, organization=org, template=template, purchase=purchase, name="Project"
        )
        assert project.organization == org

        deployment = DeploymentRequest.objects.create(
            project=project, user=user, organization=org, status='pending'
        )
        assert deployment.organization == org

    def test_user_only_records(self, setup_data):
        user, org, template, package = setup_data

        purchase = TemplatePurchase.objects.create(
            user=user, template=template, package=package, amount_paid=99.00, status='paid'
        )
        assert purchase.organization is None

        # Querying
        assert TemplatePurchase.objects.filter(user=user, organization__isnull=True).exists()
        assert not TemplatePurchase.objects.filter(organization=org).exists()
