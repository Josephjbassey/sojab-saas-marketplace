import os
import django
import secrets
import sys

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
    admin_password = os.environ.get('ADMIN_PASSWORD')
    is_generated = False
    if not admin_password:
        admin_password = secrets.token_urlsafe(16)
        is_generated = True

    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True}
    )
    admin.set_password(admin_password)
    admin.save()

    if is_generated:
        print(f"Generated admin password: {admin_password}")
    else:
        print("Admin password set from environment.")

    # Org
    org, _ = Organization.objects.get_or_create(
        slug='titan-agency',
        defaults={'name': 'Titan Agency'}
    )

    # Membership
    Membership.objects.get_or_create(
        user=admin,
        organization=org,
        defaults={'role': 'owner'}
    )

    # Client
    client, _ = Client.objects.get_or_create(
        email='contact@acme.com',
        organization=org,
        defaults={'name': 'Acme Corp'}
    )

    # Lead
    Lead.objects.get_or_create(
        organization=org,
        title='Website Redesign',
        defaults={
            'client': client,
            'value': Decimal('5000.00'),
            'status': 'qualified'
        }
    )

    # Project
    project, _ = Project.objects.get_or_create(
        organization=org,
        name='Q2 Marketing Campaign',
        defaults={
            'client': client,
            'status': 'active'
        }
    )

    # Invoice
    Invoice.objects.get_or_create(
        number='INV-2025-001',
        organization=org,
        defaults={
            'client': client,
            'project': project,
            'amount': Decimal('1200.00'),
            'due_date': date.today() + timedelta(days=14),
            'status': 'sent'
        }
    )

    print("Agency CRM seed data applied successfully.")

if __name__ == '__main__':
    seed()
