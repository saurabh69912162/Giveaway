# Generated by Django 2.2.3 on 2019-07-16 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0024_auto_20190716_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]