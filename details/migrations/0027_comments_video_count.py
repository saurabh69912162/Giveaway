# Generated by Django 2.2.3 on 2019-07-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0026_auto_20190716_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='video_count',
            field=models.IntegerField(default=1),
        ),
    ]
