# Generated by Django 4.0.6 on 2023-01-24 04:31

import app.models
from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_postmedia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmedia',
            name='media',
        ),
        migrations.AddField(
            model_name='postmedia',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=app.models.get_upload_path),
        ),
    ]
