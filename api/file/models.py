import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
from model_utils.models import TimeStampedModel
from upload_validator import FileTypeValidator


file_storage = FileSystemStorage(location=settings.FILE_STORAGE_ROOT)


class File(TimeStampedModel, models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        help_text=_("Unique identifier (UUID)."),
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    content = models.FileField(
        verbose_name=_("File Content"),
        storage=file_storage,
        null=False,
        unique=True,
        blank=False,
        validators=[FileTypeValidator(
            allowed_types=['text/plain'], allowed_extensions=['.txt']
        )]
    )

    def __str__(self):
        return self.content.path
