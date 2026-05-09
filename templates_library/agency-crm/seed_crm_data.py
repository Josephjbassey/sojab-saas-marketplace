import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.organizations.models import Organization, Membership
from apps.clients.models import Client
from apps.leads.models import Lead
from apps.projects.models import Project
from apps.invoices.models import Invoice
from decimal import Decimal
from datetime import date, timedelta

def seed():
    # Admin
    admin, _ = User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True)
    admin.set_password('password')
    admin.save()

    # Org
    org, _ = Organization.objects.get_or_create(name='Titan Agency', slug='titan-agency')
    Membership.objects.get_or_create(user=admin, organization=org, role='owner')

    # Client
    client, _ = Client.objects.get_or_create(
        organization=org,
        name='Acme Corp',
        email='contact@acme.com'
    )

    # Lead
    Lead.objects.get_or_create(
        organization=org,
        client=client,
        title='Website Redesign',
        value=Decimal('5000.00'),
        status='qualified'
    )

    # Project
    project, _ = Project.objects.get_or_create(
        organization=org,
        client=client,
        name='Q2 Marketing Campaign',
        status='active'
    )

    # Invoice
    Invoice.objects.get_or_create(
        organization=org,
        client=client,
        project=project,
        number='INV-2025-001',
        amount=Decimal('1200.00'),
        due_date=date.today() + timedelta(days=14),
        status='sent'
    )

    print("Agency CRM seed data applied successfully.")

if __name__ == '__main__':
    seed()
