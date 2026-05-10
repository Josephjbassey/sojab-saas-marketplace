from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class CrmBasePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        abstract = True

class CrmHomePage(CrmBasePage):
    template = "cms/home_page.html"
    max_count = 1

class CrmStandardPage(CrmBasePage):
    template = "cms/standard_page.html"
