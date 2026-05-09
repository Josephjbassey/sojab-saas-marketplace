from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_email(subject, recipient_list, text_content, html_content=None, from_email=None):
    """
    Low-level helper to send a single email.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    if html_content:
        msg.attach_alternative(html_content, "text/html")

    return msg.send()

def send_template_email(subject, recipient_list, template_name, context=None, from_email=None):
    """
    Helper to send an email using Django templates.
    """
    if context is None:
        context = {}

    html_content = render_to_string(f"emails/{template_name}.html", context)
    text_content = strip_tags(html_content)

    return send_email(subject, recipient_list, text_content, html_content, from_email)

def build_email_context(user, **kwargs):
    """
    Helper to build a standard context for emails.
    """
    context = {
        'user': user,
        'site_name': getattr(settings, 'WAGTAIL_SITE_NAME', 'SaaS Marketplace'),
    }
    context.update(kwargs)
    return context
