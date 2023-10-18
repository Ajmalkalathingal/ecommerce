# Generated by Django 4.2.5 on 2023-10-13 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_cartitem_product_cartitem_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product_id',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.product'),
        ),
    ]