# Generated by Django 4.2.5 on 2023-11-06 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0025_order_shippingaddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='shippingAddress',
            new_name='shippingStatus',
        ),
    ]
