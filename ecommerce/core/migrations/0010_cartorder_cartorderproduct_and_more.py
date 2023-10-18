# Generated by Django 4.2.5 on 2023-10-11 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_alter_product_discount_rate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9999999)),
                ('paid_status', models.BooleanField(default=False)),
                ('orderd_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('accepted', 'accepted'), ('process', 'process'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('cancel', 'cancel')], default='pending', max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
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
        migrations.RemoveField(
            model_name='orderplaced',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderplaced',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Orderplaced',
        ),
    ]