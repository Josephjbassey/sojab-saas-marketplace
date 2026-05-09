import os
import re
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.template.exceptions import TemplateDoesNotExist, TemplateSyntaxError

logger = logging.getLogger(__name__)

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
    Validates template_name for safety.
    """
    # Path traversal validation
    if not re.match(r'^[A-Za-z0-9_.-]+$', template_name) or template_name != os.path.basename(template_name):
        raise ValueError(f"Invalid template name: {template_name}")

    if context is None:
        context = {}

    try:
        html_content = render_to_string(f"emails/{template_name}.html", context)
    except (TemplateDoesNotExist, TemplateSyntaxError) as e:
        logger.error(
            f"Template error rendering {template_name} for {recipient_list}: {str(e)}",
            extra={'template_name': template_name, 'recipient_list': recipient_list}
        )
        raise RuntimeError(f"Could not render email template {template_name}") from e
    except Exception as e:
        logger.exception(
            f"Unexpected error rendering {template_name} for {recipient_list}",
            extra={'template_name': template_name, 'recipient_list': recipient_list}
        )
        raise

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
