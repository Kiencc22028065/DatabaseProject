# Generated by Django 4.2.5 on 2023-11-06 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0023_remove_product_product_cat_category_cate_prod'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantitySold',
            field=models.IntegerField(default=0),
        ),
    ]
