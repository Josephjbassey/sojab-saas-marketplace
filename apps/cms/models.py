from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock

class HomePage(Page):
    hero_title = models.CharField(max_length=255, help_text="Main heading on the homepage")
    hero_subtitle = models.CharField(max_length=255, blank=True, help_text="Subheading below hero title")
    
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('features', blocks.ListBlock(blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('description', blocks.TextBlock()),
            ('icon', blocks.CharBlock(required=False, help_text="Lucide icon name")),
        ]))),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('body'),
    ]

    max_count = 1

class StandardPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class FAQPage(Page):
    body = StreamField([
        ('faq_item', blocks.StructBlock([
            ('question', blocks.CharBlock()),
            ('answer', blocks.RichTextBlock()),
        ])),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
