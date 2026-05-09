import pytest
from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.clients.models import Client
from apps.leads.models import Lead
from apps.projects.models import Project
from apps.invoices.models import Invoice
from apps.common.models import Note
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

@pytest.mark.django_db
def test_crm_baseline():
    user = User.objects.create_user(username='tester', password='password')
    org = Organization.objects.create(name='Test Org', slug='test-org')

    client = Client.objects.create(
        organization=org,
        name='Test Client',
        email='test@client.com'
    )

    lead = Lead.objects.create(
        organization=org,
        client=client,
        title='Big Deal',
        value=Decimal('1000.00'),
        status='new'
    )

    # Test Note (Generic Relation)
    note = Note.objects.create(
        user=user,
        content="Met with client today.",
        content_type=ContentType.objects.get_for_model(client),
        object_id=client.id
    )

    assert client.name == 'Test Client'
    assert lead.value == Decimal('1000.00')
    assert lead.organization == org
    assert note.content_object == client

@pytest.mark.django_db
def test_cross_tenant_validation():
    org1 = Organization.objects.create(name='Org 1', slug='org-1')
    org2 = Organization.objects.create(name='Org 2', slug='org-2')

    client_org1 = Client.objects.create(organization=org1, name='C1', email='c1@o1.com')

    # Test Lead tenant mismatch
    with pytest.raises(ValidationError):
        Lead.objects.create(
            organization=org2,
            client=client_org1,
            title='Mismatched Lead'
        )

    # Test Project tenant mismatch
    with pytest.raises(ValidationError):
        Project.objects.create(
            organization=org2,
            client=client_org1,
            name='Mismatched Project'
        )

    project_org1 = Project.objects.create(organization=org1, client=client_org1, name='P1')

    # Test Invoice tenant mismatch (client)
    with pytest.raises(ValidationError):
        Invoice.objects.create(
            number='INV-001',
            organization=org2,
            client=client_org1,
            amount=Decimal('100.00'),
            due_date=date.today()
        )

    # Test Invoice tenant mismatch (project)
    with pytest.raises(ValidationError):
        Invoice.objects.create(
            number='INV-002',
            organization=org2,
            client=client_org1, # Mismatched but will fail on project first or both
            project=project_org1,
            amount=Decimal('100.00'),
            due_date=date.today()
        )
