# Generated by Django 3.2.5 on 2021-07-02 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50, null=True)),
                ('lastName', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('kelurahan', models.CharField(max_length=50, null=True)),
                ('kecamatan', models.CharField(max_length=50, null=True)),
                ('kabkot', models.CharField(max_length=50, null=True)),
                ('provinsi', models.CharField(max_length=50, null=True)),
                ('kode_pos', models.CharField(max_length=15, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_default', models.BooleanField(default=False, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
            ],
            options={
                'db_table': 'customer_address',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('is_digital', models.BooleanField(blank=True, default=False, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customeraddress')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
            options={
                'verbose_name_plural': 'ShippingAddresses',
                'db_table': 'shipping_address',
            },
        ),
        migrations.CreateModel(
            name='Pesanan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PRO', 'On Process'), ('PND', 'Pending'), ('COM', 'Complete'), ('CNC', 'Canceled')], default='PND', max_length=15)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('shipping', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.shippingaddress')),
            ],
            options={
                'verbose_name_plural': 'pesanan',
                'db_table': 'pesanan',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'db_table': 'order_item',
            },
        ),
    ]
