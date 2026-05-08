import pytest
from django.contrib.auth import get_user_model
from .models import Organization, Membership

User = get_user_model()

@pytest.mark.django_db
class TestOrganizationModels:
    def test_organization_creation(self):
        org = Organization.objects.create(name="Test Org")
        assert org.name == "Test Org"
        assert org.slug == "test-org"
        assert org.is_active is True

    def test_membership_roles(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        org = Organization.objects.create(name="Test Org")

        # Default role should be member
        membership = Membership.objects.create(user=user, organization=org)
        assert membership.role == Membership.ROLE_MEMBER

        # Change to owner
        membership.role = Membership.ROLE_OWNER
        membership.save()
        assert membership.role == Membership.ROLE_OWNER

    def test_unique_membership(self):
        user = User.objects.create_user(username="testuser2", email="test2@example.com", password="password")
        org = Organization.objects.create(name="Test Org 2")
        Membership.objects.create(user=user, organization=org)

        with pytest.raises(Exception): # Should raise IntegrityError
            Membership.objects.create(user=user, organization=org)

    def test_user_multiple_organizations(self):
        user = User.objects.create_user(username="testuser3", email="test3@example.com", password="password")
        org1 = Organization.objects.create(name="Org 1")
        org2 = Organization.objects.create(name="Org 2")

        Membership.objects.create(user=user, organization=org1, role=Membership.ROLE_OWNER)
        Membership.objects.create(user=user, organization=org2, role=Membership.ROLE_MEMBER)

        assert user.memberships.count() == 2
        assert user.memberships.filter(role=Membership.ROLE_OWNER).count() == 1
