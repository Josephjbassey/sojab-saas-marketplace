import pytest
from .models import AuditLog
from .services import log_action

@pytest.mark.django_db
class TestAuditLog:
    def test_log_action_basic(self, user):
        log = log_action(user, AuditLog.ACTION_LOGIN, message="User logged in")
        assert log.actor == user
        assert log.action == AuditLog.ACTION_LOGIN
        assert log.message == "User logged in"

    def test_log_action_with_resource(self, user, saas_template):
        log = log_action(user, AuditLog.ACTION_CREATE, resource=saas_template)
        assert log.resource_type == "SaaSTemplate"
        assert log.resource_id == str(saas_template.pk)

    def test_log_action_with_request(self, user, rf):
        request = rf.get('/')
        request.META['REMOTE_ADDR'] = '1.2.3.4'
        request.META['HTTP_USER_AGENT'] = 'TestAgent'

        log = log_action(user, AuditLog.ACTION_UPDATE, request=request)
        assert log.ip_address == '1.2.3.4'
        assert log.user_agent == 'TestAgent'
