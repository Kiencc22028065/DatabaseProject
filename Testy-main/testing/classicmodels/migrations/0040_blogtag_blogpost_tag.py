# Generated by Django 4.2.6 on 2023-11-23 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classicmodels', '0039_alter_product_infavlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('tagID', models.AutoField(primary_key=True, serialize=False)),
                ('tagName', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'Blog_Tag',
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classicmodels.blogtag'),
        ),
    ]
