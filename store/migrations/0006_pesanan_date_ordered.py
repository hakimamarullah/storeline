# Generated by Django 3.2.4 on 2021-06-29 11:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210629_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesanan',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 6, 29, 11, 42, 30, 274867, tzinfo=utc)),
            preserve_default=False,
        ),
    ]