import os
from django.core.files.base import ContentFile
from .models import ManagedFile

def save_managed_file(file_obj, purpose=ManagedFile.PURPOSE_OTHER, owner=None, organization=None, content_type=None):
    """
    Saves a file object to the ManagedFile model.
    """
    managed_file = ManagedFile(
        owner=owner,
        organization=organization,
        purpose=purpose,
        content_type=content_type or getattr(file_obj, 'content_type', ''),
        original_filename=getattr(file_obj, 'name', 'unknown'),
        size=file_obj.size
    )
    managed_file.file.save(managed_file.original_filename, file_obj, save=False)
    managed_file.save()
    return managed_file

def get_file_url(managed_file_id):
    """
    Returns the URL of a managed file by its ID.
    """
    try:
        managed_file = ManagedFile.objects.get(id=managed_file_id)
        return managed_file.file.url
    except ManagedFile.DoesNotExist:
        return None

def delete_managed_file(managed_file_id):
    """
    Deletes a managed file record and its associated file from storage.
    """
    try:
        managed_file = ManagedFile.objects.get(id=managed_file_id)
        if managed_file.file:
            if os.path.isfile(managed_file.file.path):
                os.remove(managed_file.file.path)
        managed_file.delete()
        return True
    except ManagedFile.DoesNotExist:
        return False
