import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.templates_catalog.models import SaaSTemplate, TemplateCategory, TemplatePackage, TemplateFeature

def register():
    # 1. Category
    category, _ = TemplateCategory.objects.get_or_create(
        slug='crm-agency-ops',
        defaults={
            'name': 'CRM / Agency Operations',
            'description': 'Tools for managing clients, leads, and internal agency workflows.',
            'icon_class': 'fas fa-users-cog'
        }
    )

    # 2. Template
    template, created = SaaSTemplate.objects.get_or_create(
        slug='agency-crm-saas-template',
        defaults={
            'category': category,
            'name': 'Agency CRM SaaS Template',
            'short_description': 'A ready-made Django SaaS foundation for agencies and freelancers.',
            'description': """
A robust CRM boilerplate for digital agencies, featuring lead management, client portals, and automated reporting.
Built with Django, PostgreSQL, Tailwind, HTMX, and CMS-ready architecture.

Key features include lead tracking, client management, project workspaces, and invoicing.
            """,
            'is_active': True,
            'is_featured': True,
        }
    )

    if created:
        # 3. Features
        features = [
            ('Lead Tracking', 'Manage your pipeline from initial contact to conversion.', 'fas fa-filter'),
            ('Client Portals', 'Give your clients a dedicated space to view projects and invoices.', 'fas fa-portal-enter'),
            ('Project Workspaces', 'Collaborative spaces for team and client communication.', 'fas fa-tasks'),
            ('Automated Invoicing', 'Generate and send professional invoices in seconds.', 'fas fa-file-invoice-dollar'),
            ('Wagtail CMS', 'Built-in marketing pages and internal documentation.', 'fas fa-edit'),
        ]
        for name, desc, icon in features:
            TemplateFeature.objects.get_or_create(
                template=template,
                name=name,
                defaults={'description': desc, 'icon_class': icon}
            )

        # 4. Packages
        packages = [
            ('Starter License', 'commercial', 299.00, 'Full codebase access, setup documentation, and local deployment guide.'),
            ('Customization Package', 'commercial', 999.00, 'Starter license plus custom branding, page edits, and workflow adjustments.'),
            ('Full SaaS Launch', 'agency', 2499.00, 'Complete setup, customization, deployment to your cloud, and 2 hours of training.'),
        ]
        for name, l_type, price, desc in packages:
            TemplatePackage.objects.get_or_create(
                template=template,
                name=name,
                defaults={
                    'license_type': l_type,
                    'price': price,
                    'description': desc
                }
            )
        print("Agency CRM registered successfully.")
    else:
        print("Agency CRM already registered.")

if __name__ == '__main__':
    register()
