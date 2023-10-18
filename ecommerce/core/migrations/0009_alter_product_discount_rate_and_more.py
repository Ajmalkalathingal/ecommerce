# Generated by Django 4.2.5 on 2023-10-01 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_product_discount_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_rate',
            field=models.DecimalField(decimal_places=2, max_digits=999999999),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=999999999),
        ),
    ]