# Generated by Django 4.2.16 on 2024-12-28 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
