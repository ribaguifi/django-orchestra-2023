# Generated by Django 2.2.28 on 2023-07-24 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import orchestra.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orchestration', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The app will be installed in %(home)s/webapps/%(app_name)s', max_length=128, validators=[orchestra.core.validators.validate_name], verbose_name='name')),
                ('type', models.CharField(choices=[('moodle-php', 'Moodle'), ('php', 'PHP'), ('python', 'Python'), ('static', 'Static'), ('symbolic-link', 'Symbolic link'), ('webalizer', 'Webalizer'), ('wordpress-php', 'WordPress')], max_length=32, verbose_name='type')),
                ('data', jsonfield.fields.JSONField(blank=True, default={}, help_text='Extra information dependent of each service.', verbose_name='data')),
                ('comments', models.TextField(blank=True, default='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webapps', to=settings.AUTH_USER_MODEL, verbose_name='Account')),
                ('target_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webapps', to='orchestration.Server', verbose_name='Target Server')),
            ],
            options={
                'verbose_name': 'Web App',
                'verbose_name_plural': 'Web Apps',
                'unique_together': {('name', 'account')},
            },
        ),
        migrations.CreateModel(
            name='WebAppOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(None, '-------'), ('FileSystem', [('public-root', 'Public root')]), ('Process', [('timeout', 'Process timeout'), ('processes', 'Number of processes')]), ('PHP', [('enable_functions', 'Enable functions'), ('disable_functions', 'Disable functions'), ('allow_url_include', 'Allow URL include'), ('allow_url_fopen', 'Allow URL fopen'), ('auto_append_file', 'Auto append file'), ('auto_prepend_file', 'Auto prepend file'), ('date.timezone', 'date.timezone'), ('default_socket_timeout', 'Default socket timeout'), ('display_errors', 'Display errors'), ('extension', 'Extension'), ('include_path', 'Include path'), ('open_basedir', 'Open basedir'), ('magic_quotes_gpc', 'Magic quotes GPC'), ('magic_quotes_runtime', 'Magic quotes runtime'), ('magic_quotes_sybase', 'Magic quotes sybase'), ('max_input_time', 'Max input time'), ('max_input_vars', 'Max input vars'), ('memory_limit', 'Memory limit'), ('mysql.connect_timeout', 'Mysql connect timeout'), ('output_buffering', 'Output buffering'), ('register_globals', 'Register globals'), ('post_max_size', 'Post max size'), ('sendmail_path', 'Sendmail path'), ('session.bug_compat_warn', 'Session bug compat warning'), ('session.auto_start', 'Session auto start'), ('safe_mode', 'Safe mode'), ('suhosin.post.max_vars', 'Suhosin POST max vars'), ('suhosin.get.max_vars', 'Suhosin GET max vars'), ('suhosin.request.max_vars', 'Suhosin request max vars'), ('suhosin.session.encrypt', 'Suhosin session encrypt'), ('suhosin.simulation', 'Suhosin simulation'), ('suhosin.executor.include.whitelist', 'Suhosin executor include whitelist'), ('upload_max_filesize', 'Upload max filesize'), ('upload_tmp_dir', 'Upload tmp dir'), ('zend_extension', 'Zend extension')])], max_length=128, verbose_name='name')),
                ('value', models.CharField(max_length=256, verbose_name='value')),
                ('webapp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='webapps.WebApp', verbose_name='Web application')),
            ],
            options={
                'verbose_name': 'option',
                'verbose_name_plural': 'options',
                'unique_together': {('webapp', 'name')},
            },
        ),
    ]