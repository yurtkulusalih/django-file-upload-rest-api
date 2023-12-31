# Generated by Django 4.1.7 on 2023-03-10 10:35

import django.core.files.storage
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID).', primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/api/media/uploads'), unique=True, upload_to='', verbose_name='File Content')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
