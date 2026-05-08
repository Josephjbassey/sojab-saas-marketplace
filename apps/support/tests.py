from django.test import TestCase
from django.urls import reverse


class TemplateToSaaSCustomizationPageTests(TestCase):
    def test_page_renders(self):
        response = self.client.get(reverse('support:template_to_saas_customization'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Turn any premium SaaS template into a working product.')
        self.assertContains(response, 'Clients must purchase or own the correct license')
