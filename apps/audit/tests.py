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

    def test_log_action_ip_priority(self, user, rf):
        """Verify HTTP_X_FORWARDED_FOR is preferred over REMOTE_ADDR."""
        request = rf.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '5.6.7.8, 9.10.11.12'
        request.META['REMOTE_ADDR'] = '1.2.3.4'

        log = log_action(user, AuditLog.ACTION_UPDATE, request=request)
        assert log.ip_address == '5.6.7.8'

    def test_log_action_validation(self, user):
        """Verify action is required."""
        with pytest.raises(ValueError, match="Action is required"):
            log_action(user, "")

    def test_log_action_requires_actor(self):
        with pytest.raises(ValueError, match="Actor is required"):
            log_action(None, AuditLog.ACTION_UPDATE)
