# Generated by Django 2.2.3 on 2019-07-16 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0022_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='url',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
