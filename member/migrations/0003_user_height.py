# Generated by Django 3.1.7 on 2023-08-09 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20230716_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='height',
            field=models.IntegerField(default=70, max_length=4),
        ),
    ]
