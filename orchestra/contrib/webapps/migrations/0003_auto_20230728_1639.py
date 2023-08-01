# Generated by Django 2.2.28 on 2023-07-28 14:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orchestration', '__first__'),
        ('webapps', '0002_webapp_sftpuser'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='webapp',
            unique_together={('name', 'account', 'target_server')},
        ),
    ]
