# Generated by Django 4.2.5 on 2024-05-14 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0046_alter_favoriteitem_table_alter_favoritelist_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='inFavList',
        ),
    ]
