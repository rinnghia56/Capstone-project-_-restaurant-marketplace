# Generated by Django 4.2 on 2023-06-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0015_foodfavorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='notice',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
