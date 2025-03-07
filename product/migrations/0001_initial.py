# Generated by Django 5.0.3 on 2024-04-28 18:17

import django.db.models.deletion
import django.db.models.manager
import django_jalali.db.models
import lib.base_model
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('title', models.CharField(max_length=48, unique=True, verbose_name='brand title')),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('title', models.CharField(max_length=48, unique=True, verbose_name='category title')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='color name')),
                ('code', models.CharField(default='#fff', max_length=9, verbose_name='color code (hex)')),
            ],
            options={
                'verbose_name': 'color',
                'verbose_name_plural': 'colors',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('name', models.CharField(max_length=48, verbose_name='name')),
                ('phone_number', models.CharField(blank=True, max_length=24, null=True, verbose_name='phone number')),
            ],
            options={
                'verbose_name': 'seller',
                'verbose_name_plural': 'sellers',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='size')),
            ],
            options={
                'verbose_name': 'size',
                'verbose_name_plural': 'sizes',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='product title')),
                ('first_price', models.PositiveIntegerField(default=0, verbose_name='first price')),
                ('discount', models.PositiveIntegerField(default=0, verbose_name='discount')),
                ('visit_count', models.PositiveIntegerField(default=0, verbose_name='visit count')),
                ('buy_count', models.PositiveIntegerField(default=0, verbose_name='buy count')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brands', to='product.brand')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.seller', verbose_name='seller')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('title', models.CharField(max_length=48, verbose_name='attribute title')),
                ('value', models.CharField(max_length=48, verbose_name='value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='product.product')),
            ],
            options={
                'verbose_name': 'attribute',
                'verbose_name_plural': 'attributes',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('image', lib.base_model.CustomImageField(null=True, upload_to='products/', verbose_name='image')),
                ('size', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=6, null=True, verbose_name='size (MB)')),
                ('is_main', models.BooleanField(default=False, verbose_name='is main image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
            options={
                'verbose_name': 'product image',
                'verbose_name_plural': 'product images',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('quantity', models.PositiveSmallIntegerField(default=0, verbose_name='quantity')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventories', to='product.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to='product.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventories', to='product.size')),
            ],
            options={
                'verbose_name': 'inventory',
                'verbose_name_plural': 'inventories',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
