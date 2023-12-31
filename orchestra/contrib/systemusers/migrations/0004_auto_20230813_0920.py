# Generated by Django 2.2.28 on 2023-08-13 07:20

from django.db import migrations, models
import orchestra.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('systemusers', '0003_auto_20230724_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webappusers',
            name='username',
            field=models.CharField(help_text='Required. 32 characters or fewer. Letters, digits and ./-/_ only.', max_length=32, validators=[orchestra.core.validators.validate_username], verbose_name='username'),
        ),
    ]
