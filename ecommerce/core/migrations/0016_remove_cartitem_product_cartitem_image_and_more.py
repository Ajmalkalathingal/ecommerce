# Generated by Django 4.2.5 on 2023-10-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_cartitem_image_remove_cartitem_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='image',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
