# Generated by Django 2.2.2 on 2019-07-01 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0009_new_giveaway_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_giveaway',
            name='caption1',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='new_giveaway',
            name='caption2',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='new_giveaway',
            name='caption3',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
