# Generated by Django 4.2 on 2023-06-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_order_total_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_shipping_fee',
            field=models.FloatField(default=0),
        ),
    ]
