# Generated by Django 4.0.6 on 2023-03-01 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0008_clientsocketdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientsocketdata',
            name='last_read_id_in_server',
            field=models.IntegerField(default=0),
        ),
    ]