# Generated by Django 4.0.6 on 2022-11-16 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='accept',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='connection',
            name='connected',
            field=models.ManyToManyField(blank=True, to='user.connection'),
        ),
    ]