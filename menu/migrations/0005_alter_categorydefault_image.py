# Generated by Django 4.2 on 2023-05-19 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_categorydefault_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorydefault',
            name='image',
            field=models.ImageField(blank=True, upload_to='categoty_default'),
        ),
    ]
