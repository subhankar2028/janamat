# Generated by Django 2.2 on 2020-07-29 08:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jmat', '0005_auto_20200729_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dob',
        ),
        migrations.AlterField(
            model_name='comment',
            name='edit_Session_Expiry',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 29, 9, 21, 14, 201798, tzinfo=utc), editable=False),
        ),
    ]
