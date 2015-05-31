from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('djangocms_picture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='is_responsive',
            field=models.BooleanField(help_text='Add Twitter Bootstrap `img-responsive` css class.', verbose_name='responsive', blank=True, null=True),
            preserve_default=True,
        ),
    ]
