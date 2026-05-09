import pytest
from .models import GeneratedProject, ProjectConfiguration
from .services import create_generated_project_from_purchase, mark_project_delivered, prepare_project_configuration

@pytest.mark.django_db
class TestGeneratorModels:
    def test_create_generated_project(self, purchase):
        project = GeneratedProject.objects.create(
            purchase=purchase,
            template=purchase.template,
            user=purchase.user,
            project_name="Test Project"
        )
        assert project.project_name == "Test Project"
        assert project.status == GeneratedProject.STATUS_DRAFT
        assert project.slug == "test-project"

    def test_project_configuration(self, purchase):
        project = GeneratedProject.objects.create(
            purchase=purchase,
            template=purchase.template,
            user=purchase.user,
            project_name="Config Project"
        )
        config = ProjectConfiguration.objects.create(
            generated_project=project,
            brand_name="My Brand",
            primary_color="#ff0000"
        )
        assert config.brand_name == "My Brand"
        assert project.configuration == config

@pytest.mark.django_db
class TestGeneratorServices:
    def test_create_from_purchase(self, purchase):
        project = create_generated_project_from_purchase(purchase)
        assert project.purchase == purchase
        assert project.user == purchase.user
        assert project.template == purchase.template
        assert ProjectConfiguration.objects.filter(generated_project=project).exists()

    def test_mark_delivered(self, purchase):
        project = create_generated_project_from_purchase(purchase)
        mark_project_delivered(project, deployment_url="https://myapp.vercel.app")
        assert project.status == GeneratedProject.STATUS_DELIVERED
        assert project.deployment_url == "https://myapp.vercel.app"

    def test_prepare_configuration(self, purchase):
        project = create_generated_project_from_purchase(purchase)
        # Verify fresh fetch of config
        config = prepare_project_configuration(project, brand_name="Updated Name", cms_enabled=False)
        assert config.brand_name == "Updated Name"
        assert config.cms_enabled is False

        # Verify it persisted
        project.refresh_from_db()
        assert project.configuration.brand_name == "Updated Name"
