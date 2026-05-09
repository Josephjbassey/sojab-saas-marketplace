import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Organization, Membership
from .services import (
    create_default_organization_for_user,
    add_member_to_organization,
    get_user_organizations,
    user_has_role
)

User = get_user_model()

@pytest.mark.django_db
class TestOrganizationModels:
    def test_organization_creation(self):
        user = User.objects.create_user(username="owner", email="owner@example.com")
        org = Organization.objects.create(name="Test Org", owner=user)
        assert org.name == "Test Org"
        assert org.slug == "test-org"
        assert org.owner == user
        assert org.is_active is True

    def test_slug_uniqueness(self):
        user = User.objects.create_user(username="owner2", email="owner2@example.com")
        Organization.objects.create(name="Unique Org", slug="unique", owner=user)
        with pytest.raises(IntegrityError):
            Organization.objects.create(name="Another Org", slug="unique", owner=user)

    def test_membership_roles(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        owner = User.objects.create_user(username="owner3", email="owner3@example.com")
        org = Organization.objects.create(name="Test Org", owner=owner)

        # Test roles
        roles = [Membership.ROLE_OWNER, Membership.ROLE_ADMIN, Membership.ROLE_MEMBER, Membership.ROLE_GUEST]
        for role in roles:
            membership = Membership.objects.create(user=user, organization=org, role=role)
            if role == Membership.ROLE_OWNER:
                assert membership.is_owner
            elif role == Membership.ROLE_ADMIN:
                assert membership.is_admin
            elif role == Membership.ROLE_MEMBER:
                assert membership.is_member
            elif role == Membership.ROLE_GUEST:
                assert membership.is_guest
            membership.delete()

    def test_unique_membership(self):
        user = User.objects.create_user(username="testuser2", email="test2@example.com")
        owner = User.objects.create_user(username="owner4", email="owner4@example.com")
        org = Organization.objects.create(name="Test Org 2", owner=owner)
        Membership.objects.create(user=user, organization=org)

        with pytest.raises(IntegrityError):
            Membership.objects.create(user=user, organization=org)

@pytest.mark.django_db
class TestOrganizationServices:
    def test_create_default_organization(self):
        user = User.objects.create_user(username="newuser", email="new@example.com", first_name="John", last_name="Doe")
        org = create_default_organization_for_user(user)

        assert org.owner == user
        assert "John Doe's Workspace" in org.name
        assert Membership.objects.filter(user=user, organization=org, role=Membership.ROLE_OWNER).exists()

    def test_create_default_organization_slug_collision(self):
        user1 = User.objects.create_user(username="u1", email="u1@example.com", first_name="Same", last_name="Name")
        user2 = User.objects.create_user(username="u2", email="u2@example.com", first_name="Same", last_name="Name")

        org1 = create_default_organization_for_user(user1)
        org2 = create_default_organization_for_user(user2)

        assert org1.slug != org2.slug
        assert org2.slug.startswith(org1.slug)

    def test_add_member_to_organization(self):
        owner = User.objects.create_user(username="owner", email="owner@example.com")
        member = User.objects.create_user(username="member", email="member@example.com")
        org = Organization.objects.create(name="Team", owner=owner)

        add_member_to_organization(org, member, Membership.ROLE_ADMIN)
        assert Membership.objects.filter(user=member, organization=org, role=Membership.ROLE_ADMIN).exists()

        # Update role
        add_member_to_organization(org, member, Membership.ROLE_MEMBER)
        assert Membership.objects.get(user=member, organization=org).role == Membership.ROLE_MEMBER

    def test_get_user_organizations(self):
        user = User.objects.create_user(username="user", email="user@example.com")
        owner = User.objects.create_user(username="owner", email="owner@example.com")
        org1 = Organization.objects.create(name="Org 1", owner=owner)
        org2 = Organization.objects.create(name="Org 2", owner=owner)
        org3 = Organization.objects.create(name="Org 3", owner=owner)

        Membership.objects.create(user=user, organization=org1)
        Membership.objects.create(user=user, organization=org2)

        user_orgs = get_user_organizations(user)
        assert user_orgs.count() == 2
        assert org1 in user_orgs
        assert org2 in user_orgs
        assert org3 not in user_orgs

    def test_user_has_role(self):
        user = User.objects.create_user(username="user", email="user@example.com")
        owner = User.objects.create_user(username="owner", email="owner@example.com")
        org = Organization.objects.create(name="Org", owner=owner)
        Membership.objects.create(user=user, organization=org, role=Membership.ROLE_ADMIN)

        assert user_has_role(user, org, Membership.ROLE_ADMIN)
        assert user_has_role(user, org, [Membership.ROLE_ADMIN, Membership.ROLE_OWNER])
        assert not user_has_role(user, org, Membership.ROLE_MEMBER)
