import pytest
from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.clients.models import Client
from apps.leads.models import Lead
from apps.common.models import Note
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal

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
