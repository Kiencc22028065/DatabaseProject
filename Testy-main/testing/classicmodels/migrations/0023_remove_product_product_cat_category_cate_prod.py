# Generated by Django 4.2.5 on 2023-11-06 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0022_product_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_cat',
        ),
        migrations.AddField(
            model_name='category',
            name='cate_prod',
            field=models.ManyToManyField(to='classicmodels.product'),
        ),
    ]
