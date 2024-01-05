# Generated by Django 4.2.5 on 2023-10-26 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0012_alter_transaction_totalamount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classicmodels.customer'),
        ),
    ]