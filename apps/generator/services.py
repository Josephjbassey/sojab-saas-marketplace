from .models import GeneratedProject, ProjectConfiguration

def create_generated_project_from_purchase(purchase, project_name=None):
    """
    Initializes a GeneratedProject record from a successful purchase.
    """
    if not project_name:
        project_name = f"{purchase.template.name} - {purchase.user.username}"

    project = GeneratedProject.objects.create(
        purchase=purchase,
        template=purchase.template,
        user=purchase.user,
        organization=purchase.organization,
        project_name=project_name,
        status=GeneratedProject.STATUS_DRAFT
    )

    # Initialize basic configuration
    prepare_project_configuration(project)

    return project

def prepare_project_configuration(generated_project, **kwargs):
    """
    Creates or updates the ProjectConfiguration for a generated project.
    """
    config, created = ProjectConfiguration.objects.get_or_create(
        generated_project=generated_project
    )

    if kwargs:
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        config.save()

    return config

def mark_project_delivered(generated_project, deployment_url=None, github_url=None):
    """
    Marks a project as delivered and optionally sets URLs.
    """
    generated_project.status = GeneratedProject.STATUS_DELIVERED
    if deployment_url:
        generated_project.deployment_url = deployment_url
    if github_url:
        generated_project.github_repo_url = github_url
    generated_project.save(update_fields=['status', 'deployment_url', 'github_repo_url', 'updated_at'])
    return generated_project
