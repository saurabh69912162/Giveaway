# Generated by Django 2.2.2 on 2019-06-30 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0008_giveaway_rule_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_giveaway',
            name='status',
            field=models.CharField(default='Closed', max_length=255),
        ),
    ]
