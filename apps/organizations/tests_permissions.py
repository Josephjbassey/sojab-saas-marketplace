import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .models import Organization, Membership
from .permissions import (
    is_organization_owner,
    is_organization_admin,
    is_organization_member,
    can_view_organization,
    can_manage_organization,
    can_manage_members,
    can_manage_billing,
    can_view_project,
    can_manage_project
)
from apps.templates_catalog.models import SaaSTemplate, TemplateCategory
from apps.purchases.models import TemplatePurchase
from apps.deployments.models import ClientProject

User = get_user_model()

@pytest.fixture
def org_and_users(db):
    owner_user = User.objects.create_user(username="owner", email="owner@example.com")
    admin_user = User.objects.create_user(username="admin", email="admin@example.com")
    member_user = User.objects.create_user(username="member", email="member@example.com")
    guest_user = User.objects.create_user(username="guest", email="guest@example.com")
    outsider = User.objects.create_user(username="outsider", email="outsider@example.com")

    org = Organization.objects.create(name="Test Org", owner=owner_user)

    Membership.objects.create(user=owner_user, organization=org, role=Membership.ROLE_OWNER)
    Membership.objects.create(user=admin_user, organization=org, role=Membership.ROLE_ADMIN)
    Membership.objects.create(user=member_user, organization=org, role=Membership.ROLE_MEMBER)
    Membership.objects.create(user=guest_user, organization=org, role=Membership.ROLE_GUEST)

    return {
        'org': org,
        'owner': owner_user,
        'admin': admin_user,
        'member': member_user,
        'guest': guest_user,
        'outsider': outsider,
        'anonymous': AnonymousUser()
    }

@pytest.fixture
def project(db, org_and_users):
    category = TemplateCategory.objects.create(name="SaaS")
    template = SaaSTemplate.objects.create(name="Starter", category=category)
    package = template.packages.create(name="Basic", price=99, license_type='personal')
    purchase = TemplatePurchase.objects.create(
        user=org_and_users['owner'],
        organization=org_and_users['org'],
        template=template,
        package=package,
        amount_paid=99,
        status='paid'
    )
    return ClientProject.objects.create(
        name="Team Project",
        user=org_and_users['owner'],
        organization=org_and_users['org'],
        template=template,
        purchase=purchase
    )

@pytest.mark.django_db
class TestRBACPermissions:
    def test_is_organization_owner(self, org_and_users):
        org = org_and_users['org']
        assert is_organization_owner(org_and_users['owner'], org) is True
        assert is_organization_owner(org_and_users['admin'], org) is False
        assert is_organization_owner(org_and_users['outsider'], org) is False
        assert is_organization_owner(org_and_users['anonymous'], org) is False

    def test_is_organization_admin(self, org_and_users):
        org = org_and_users['org']
        assert is_organization_admin(org_and_users['admin'], org) is True
        assert is_organization_admin(org_and_users['owner'], org) is False
        assert is_organization_admin(org_and_users['outsider'], org) is False

    def test_is_organization_member(self, org_and_users):
        org = org_and_users['org']
        assert is_organization_member(org_and_users['owner'], org) is True
        assert is_organization_member(org_and_users['guest'], org) is True
        assert is_organization_member(org_and_users['outsider'], org) is False

    def test_can_view_organization(self, org_and_users):
        org = org_and_users['org']
        assert can_view_organization(org_and_users['guest'], org) is True
        assert can_view_organization(org_and_users['outsider'], org) is False

    def test_can_manage_organization(self, org_and_users):
        org = org_and_users['org']
        assert can_manage_organization(org_and_users['owner'], org) is True
        assert can_manage_organization(org_and_users['admin'], org) is True
        assert can_manage_organization(org_and_users['member'], org) is False
        assert can_manage_organization(org_and_users['guest'], org) is False

    def test_can_manage_members(self, org_and_users):
        org = org_and_users['org']
        assert can_manage_members(org_and_users['admin'], org) is True
        assert can_manage_members(org_and_users['member'], org) is False

    def test_can_manage_billing(self, org_and_users):
        org = org_and_users['org']
        assert can_manage_billing(org_and_users['owner'], org) is True
        assert can_manage_billing(org_and_users['guest'], org) is False

    def test_can_view_project(self, org_and_users, project):
        assert can_view_project(org_and_users['owner'], project) is True
        assert can_view_project(org_and_users['guest'], project) is True
        assert can_view_project(org_and_users['outsider'], project) is False

    def test_can_manage_project(self, org_and_users, project):
        assert can_manage_project(org_and_users['owner'], project) is True
        assert can_manage_project(org_and_users['admin'], project) is True
        assert can_manage_project(org_and_users['member'], project) is False
        assert can_manage_project(org_and_users['outsider'], project) is False

    def test_can_view_standalone_project(self, org_and_users):
        category = TemplateCategory.objects.create(name="Standalone")
        template = SaaSTemplate.objects.create(name="Alone", category=category)
        package = template.packages.create(name="Basic", price=50, license_type='personal')
        purchase = TemplatePurchase.objects.create(
            user=org_and_users['outsider'],
            template=template,
            package=package,
            amount_paid=50,
            status='paid'
        )
        alone_project = ClientProject.objects.create(
            name="Private Project",
            user=org_and_users['outsider'],
            template=template,
            purchase=purchase
        )

        assert can_view_project(org_and_users['outsider'], alone_project) is True
        assert can_view_project(org_and_users['owner'], alone_project) is False
