# Generated by Django 4.2.5 on 2023-10-22 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0005_alter_shop_shopname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='shopName',
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
