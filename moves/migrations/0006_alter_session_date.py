# Generated by Django 4.0.6 on 2022-07-26 05:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moves', '0005_alter_session_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 7, 26, 5, 51, 3, 92545)),
        ),
    ]
