# Generated by Django 2.2.2 on 2019-07-06 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0020_auto_20190706_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='giveaway_rule',
            name='status',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
