import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.audit.models import AuditLog
from apps.audit.services import log_action

User = get_user_model()

@pytest.mark.django_db
class TestAuditService:
    def test_log_action_basic(self, db):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        log = log_action(actor=user, action='login', message='User logged in')

        assert AuditLog.objects.count() == 1
        assert log.actor == user
        assert log.action == 'login'
        assert log.message == 'User logged in'

    def test_log_action_metadata(self, db):
        metadata = {'key': 'value', 'nested': {'a': 1}}
        log = log_action(action='create', metadata=metadata)

        assert log.metadata == metadata

    def test_log_action_resource(self, db):
        user = User.objects.create_user(username='testuser2', email='test2@example.com', password='password')
        log = log_action(action='update', resource=user)

        assert log.resource_type == 'User'
        assert log.resource_id == str(user.id)

    def test_log_action_request_data(self, db):
        factory = RequestFactory()
        request = factory.get('/', HTTP_USER_AGENT='test-agent', REMOTE_ADDR='1.2.3.4')

        log = log_action(action='login', request=request)

        assert log.ip_address == '1.2.3.4'
        assert log.user_agent == 'test-agent'

    def test_log_action_nullable_actor(self, db):
        log = log_action(action='payment_completed', message='System event')

        assert log.actor is None
        assert log.action == 'payment_completed'
