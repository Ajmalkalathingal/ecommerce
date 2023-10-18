# Generated by Django 4.2.5 on 2023-10-12 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_remove_cartitem_user_cartitem_cart_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart_order',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='CartOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=100)),
                ('product_status', models.CharField(max_length=100)),
                ('item', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=100)),
                ('qty', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=99999999)),
                ('total', models.DecimalField(decimal_places=2, max_digits=999999)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cartorder')),
            ],
        ),
    ]
