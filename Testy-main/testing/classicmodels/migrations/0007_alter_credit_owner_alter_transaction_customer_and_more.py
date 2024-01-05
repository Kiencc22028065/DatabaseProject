# Generated by Django 4.2.5 on 2023-10-23 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0006_remove_shop_shopname_shop_shop_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classicmodels.customer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='customer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classicmodels.customer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classicmodels.order'),
        ),
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('reviewID', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, max_length=100, null=True)),
                ('rating', models.CharField(blank=True, max_length=10, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classicmodels.product')),
            ],
        ),
    ]
