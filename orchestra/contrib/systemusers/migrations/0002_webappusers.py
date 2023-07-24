# Generated by Django 2.2.28 on 2023-07-22 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import orchestra.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orchestration', '__first__'),
        ('systemusers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebappUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Required. 32 characters or fewer. Letters, digits and ./-/_ only.', max_length=32, unique=True, validators=[orchestra.core.validators.validate_username], verbose_name='username')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('home', models.CharField(blank=True, help_text='Starting location when login with this no-shell user.', max_length=256, verbose_name='home')),
                ('shell', models.CharField(choices=[('/dev/null', 'No shell, FTP only'), ('/bin/rssh', 'No shell, SFTP/RSYNC only'), ('/usr/bin/git-shell', 'No shell, GIT only'), ('/bin/bash', '/bin/bash')], default='/dev/null', max_length=32, verbose_name='shell')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL, verbose_name='Account')),
                ('target_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orchestration.Server', verbose_name='Server')),
            ],
            options={
                'unique_together': {('username', 'target_server')},
            },
        ),
    ]