# Generated by Django 4.0.6 on 2023-03-16 06:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_customuser_email_verified_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
