# Generated by Django 4.0.6 on 2022-11-16 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_request_accept_alter_connection_connected'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='decline',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
