# Generated by Django 4.0.6 on 2022-11-10 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_connections'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Connections',
            new_name='Connection',
        ),
    ]
