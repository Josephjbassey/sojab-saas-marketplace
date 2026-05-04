from django.db import models
from django.utils.text import slugify
from apps.common.models import BaseModel

class TemplateCategory(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True, help_text="CSS class for the icon (e.g., 'fas fa-rocket')")

    class Meta:
        verbose_name_plural = "Template Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class SaaSTemplate(BaseModel):
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    thumbnail = models.ImageField(upload_to='templates/thumbnails/', blank=True, null=True)
    demo_url = models.URLField(blank=True)
    github_repo_url = models.URLField(blank=True, help_text="Private or public repository URL")
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class TemplatePackage(BaseModel):
    LICENSE_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('commercial', 'Commercial'),
        ('agency', 'Agency'),
    ]

    template = models.ForeignKey(SaaSTemplate, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=100, help_text="e.g. Personal, Commercial, Agency")
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPE_CHOICES, default='personal')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.template.name} - {self.name} (${self.price})"

class TemplateFeature(BaseModel):
    template = models.ForeignKey(SaaSTemplate, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.template.name} - {self.name}"

class TemplateScreenshot(BaseModel):
    template = models.ForeignKey(SaaSTemplate, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='templates/screenshots/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Screenshot for {self.template.name}"
