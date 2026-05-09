import pytest
from django.conf import settings

def test_security_settings_defaults():
    """Verify hardening settings have sensible defaults for development."""
    assert settings.X_FRAME_OPTIONS == 'DENY'
    assert settings.SECURE_REFERRER_POLICY == 'same-origin'
    assert settings.DATA_UPLOAD_MAX_MEMORY_SIZE == 2621440

def test_security_checks_configured():
    """Verify production security checks are configured in settings.py."""
    with open('config/settings.py', 'r') as f:
        content = f.read()
        assert 'ALLOWED_HOSTS cannot be wildcard in production' in content
        assert 'Set a non-default SECRET_KEY in environment when DEBUG=False' in content
