# Generated by Django 4.2 on 2023-05-19 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_alter_fooditem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='category_default',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='fooditems_default', to='menu.categorydefault'),
        ),
    ]
