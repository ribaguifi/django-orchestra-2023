# Generated by Django 2.2.28 on 2023-07-24 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systemusers', '0003_auto_20230724_1813'),
        ('webapps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webapp',
            name='sftpuser',
            field=models.ForeignKey(blank=True, help_text='This option is only required for the new webservers.', null=True, on_delete=django.db.models.deletion.CASCADE, to='systemusers.WebappUsers', verbose_name='SFTP user'),
        ),
    ]