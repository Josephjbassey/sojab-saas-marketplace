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
