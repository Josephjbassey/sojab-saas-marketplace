import os
import django
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.templates_catalog.models import TemplateCategory, SaaSTemplate, TemplatePackage, TemplateFeature
from apps.accounts.models import User


def seed_data():
    print("Seeding database...")
    
    # 1. Ensure Superuser
    if not User.objects.filter(email='admin@example.com').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
        print("- Created superuser admin@example.com")

    # 2. Categories
    categories_data = ['SaaS Boilerplates', 'Ecommerce', 'Marketing', 'Dashboards']
    categories = []
    for cat_name in categories_data:
        cat, created = TemplateCategory.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name)}
        )
        categories.append(cat)
        if created:
            print(f"- Created category: {cat_name}")

    # 3. Dummy Templates
    templates_data = [
        {
            'name': 'Titan SaaS Boilerplate',
            'category': categories[0],
            'description': 'A robust Next.js and Django boilerplate with multi-tenancy, payments, and auth ready to go.',
            'is_featured': True
        },
        {
            'name': 'Luxe Ecommerce Store',
            'category': categories[1],
            'description': 'Premium ecommerce template for luxury brands with high-performance animations and Stripe integration.',
            'is_featured': True
        },
        {
            'name': 'SaaS Metrics Dashboard',
            'category': categories[3],
            'description': 'Clean and efficient dashboard template for monitoring SaaS KPIs and user engagement.',
            'is_featured': False
        }
    ]

    for tdata in templates_data:
        template, created = SaaSTemplate.objects.get_or_create(
            name=tdata['name'],
            category=tdata['category'],
            defaults={
                'slug': slugify(tdata['name']),
                'description': tdata['description'],
                'is_featured': tdata['is_featured'],
                'is_active': True
            }
        )
        if created:
            print(f"- Created template: {template.name}")
            
            # Packages for each template
            TemplatePackage.objects.create(
                template=template,
                name='Personal License',
                license_type='personal',
                price=99.00,
            )
            TemplatePackage.objects.create(
                template=template,
                name='Commercial License',
                license_type='commercial',
                price=299.00,
            )
            
            # Features
            features = ['Responsive Design', 'Auth Ready', 'Documentation Included', '6 Months Support']
            for f in features:
                TemplateFeature.objects.create(template=template, name=f)

    print("Seeding complete!")

if __name__ == '__main__':
    seed_data()
