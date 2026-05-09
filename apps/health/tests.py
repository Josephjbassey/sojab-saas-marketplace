import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
class TestHealthEndpoints:
    def setup_method(self):
        self.client = Client()

    def test_health_live(self):
        url = reverse('health:live')
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert data['app'] == 'running'
        assert 'timestamp' in data

    def test_health_ready(self):
        url = reverse('health:ready')
        response = self.client.get(url)
        # Should be 200 since DB works in test env
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert data['database'] == 'ok'
        assert 'redis' in data

    def test_health_status(self):
        url = reverse('health:status')
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert data['app'] == 'running'
        assert 'uptime' in data
        assert 'version' in data
