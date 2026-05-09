from .models import ManagedFile

def save_managed_file(file, purpose, user=None, organization=None):
    """
    Service helper to create a ManagedFile record and save the file.
    """
    managed_file = ManagedFile(
        file=file,
        purpose=purpose,
        owner=user,
        organization=organization,
        original_filename=file.name,
        size=file.size,
        content_type=getattr(file, 'content_type', '')
    )
    managed_file.save()
    return managed_file

def get_file_url(managed_file):
    """
    Returns the absolute or relative URL for the file.
    In the future, this can be updated to return presigned URLs for R2/S3.
    """
    if not managed_file or not managed_file.file:
        return None
    return managed_file.file.url

def delete_managed_file(managed_file):
    """
    Deletes the ManagedFile record and the associated file from storage.
    """
    if managed_file.file:
        managed_file.file.delete(save=False)
    managed_file.delete()
