# Generated by Django 4.2.5 on 2023-10-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0010_alter_orderdetails_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]
