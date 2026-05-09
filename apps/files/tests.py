import pytest
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization
from .models import ManagedFile, validate_file_size
from .services import save_managed_file, get_file_url, delete_managed_file

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', email='test@example.com', password='password')

@pytest.fixture
def organization(db, user):
    return Organization.objects.create(name='Test Org', owner=user)

@pytest.mark.django_db
class TestManagedFileModel:
    def test_create_managed_file(self, user, organization):
        file_content = b"hello world"
        uploaded_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        managed_file = ManagedFile.objects.create(
            owner=user,
            organization=organization,
            file=uploaded_file,
            purpose=ManagedFile.PURPOSE_DOCUMENT
        )

        assert managed_file.original_filename == "test.txt"
        assert managed_file.size == len(file_content)
        assert managed_file.purpose == ManagedFile.PURPOSE_DOCUMENT
        assert managed_file.content_type == "" # Not set automatically in .create() unless we override more

    def test_file_size_validation(self):
        class MockFile:
            def __init__(self, size):
                self.size = size

        # 50MB is okay
        validate_file_size(MockFile(50 * 1024 * 1024))

        # 51MB should fail
        with pytest.raises(ValidationError):
            validate_file_size(MockFile(51 * 1024 * 1024))

@pytest.mark.django_db
class TestManagedFileServices:
    def test_save_managed_file(self, user, organization):
        file_content = b"service test content"
        uploaded_file = SimpleUploadedFile("service_test.txt", file_content, content_type="text/plain")

        managed_file = save_managed_file(
            uploaded_file,
            purpose=ManagedFile.PURPOSE_CLIENT_BRAND_ASSET,
            owner=user,
            organization=organization
        )

        assert managed_file.original_filename == "service_test.txt"
        assert managed_file.size == len(file_content)
        assert managed_file.purpose == ManagedFile.PURPOSE_CLIENT_BRAND_ASSET
        assert managed_file.content_type == "text/plain"
        assert "service_test" in managed_file.file.name

    def test_get_file_url(self, user):
        file_content = b"url test"
        uploaded_file = SimpleUploadedFile("url_test.txt", file_content)
        managed_file = save_managed_file(uploaded_file, owner=user)

        url = get_file_url(managed_file.id)
        assert url is not None
        assert managed_file.file.url in url

    def test_delete_managed_file(self, user):
        file_content = b"delete test"
        uploaded_file = SimpleUploadedFile("delete_test.txt", file_content)
        managed_file = save_managed_file(uploaded_file, owner=user)
        managed_file_id = managed_file.id

        # In-memory storage might not have a path, but FileSystemStorage does.
        # We check the record deletion regardless.
        result = delete_managed_file(managed_file_id)
        assert result is True
        assert ManagedFile.objects.filter(id=managed_file_id).count() == 0
