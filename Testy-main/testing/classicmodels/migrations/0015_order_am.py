# Generated by Django 4.2.5 on 2023-11-04 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0014_order_paymentreceive'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='am',
            field=models.IntegerField(default=0),
        ),
    ]
