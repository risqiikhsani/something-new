# Generated by Django 4.0.6 on 2023-02-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0006_notification_object_data_notification_subject_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='object_text_preview',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='subject_text_preview',
            field=models.TextField(blank=True, null=True),
        ),
    ]
