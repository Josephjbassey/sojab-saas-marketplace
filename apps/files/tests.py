import os
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import ManagedFile
from .services import save_managed_file, delete_managed_file

User = get_user_model()

@pytest.mark.django_db
class TestManagedFile:
    def test_file_model_creation(self):
        file_content = b"test content"
        test_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        managed_file = ManagedFile.objects.create(
            file=test_file,
            purpose='document',
            original_filename="test.txt",
            size=len(file_content)
        )

        assert managed_file.original_filename == "test.txt"
        assert managed_file.purpose == "document"
        assert managed_file.size == len(file_content)
        assert "test" in managed_file.file.name
        assert managed_file.file.name.endswith(".txt")

    def test_save_managed_file_service(self):
        user = User.objects.create_user(username="testuser", email="test@example.com")
        file_content = b"service content"
        test_file = SimpleUploadedFile("service.txt", file_content)

        managed_file = save_managed_file(test_file, 'client_brand_asset', user=user)

        assert managed_file.owner == user
        assert managed_file.purpose == 'client_brand_asset'
        assert managed_file.size == len(file_content)

    def test_file_size_validation(self, settings):
        settings.MAX_UPLOAD_SIZE = 10  # 10 bytes limit
        file_content = b"content longer than 10 bytes"
        test_file = SimpleUploadedFile("too_big.txt", file_content)

        managed_file = ManagedFile(file=test_file)
        with pytest.raises(ValidationError):
            managed_file.full_clean()

    def test_delete_managed_file_service(self):
        file_content = b"delete me"
        test_file = SimpleUploadedFile("delete.txt", file_content)
        managed_file = save_managed_file(test_file, 'other')

        file_path = managed_file.file.path
        assert os.path.exists(file_path)

        delete_managed_file(managed_file)

        assert not ManagedFile.objects.filter(id=managed_file.id).exists()
        assert not os.path.exists(file_path)
