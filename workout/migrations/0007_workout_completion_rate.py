# Generated by Django 3.1.7 on 2023-08-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0006_auto_20230816_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='completion_rate',
            field=models.IntegerField(default=100),
        ),
    ]
