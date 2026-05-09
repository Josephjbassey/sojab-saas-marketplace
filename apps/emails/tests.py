import pytest
from django.core import mail
from .services import send_email, send_template_email, build_email_context

@pytest.mark.django_db
class TestEmailServices:
    def test_send_email_basic(self):
        send_email("Subject", ["to@example.com"], "Text Body")
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Subject"
        assert mail.outbox[0].to == ["to@example.com"]

    def test_send_template_email(self, user):
        context = build_email_context(user)
        send_template_email(
            "Welcome",
            [user.email],
            "purchase_confirmation",
            context={'user': user, 'purchase': {'template': {'name': 'T1'}, 'package': {'name': 'P1'}, 'transaction_id': 'TX1', 'amount_paid': '10.00'}}
        )
        assert len(mail.outbox) == 1
        assert "T1" in mail.outbox[0].body

    def test_build_email_context(self, user):
        """Verify standard context and merging of custom values."""
        context = build_email_context(user, custom_key='custom_value')
        assert context['user'] == user
        assert 'site_name' in context
        assert context['custom_key'] == 'custom_value'

    def test_send_template_email_invalid_name(self, user):
        """Verify template name validation."""
        with pytest.raises(ValueError, match="Invalid template name"):
            send_template_email("Subject", [user.email], "../illegal")
