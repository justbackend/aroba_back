from django.core.files.storage import FileSystemStorage


class MediaStorage(FileSystemStorage):
    pass


class PublicStorage(FileSystemStorage):
    pass
