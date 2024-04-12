# Generated by Django 5.0.3 on 2024-04-04 09:50

import django.db.models.deletion
import django.db.models.manager
import django_jalali.db.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'basket',
                'verbose_name_plural': 'baskets',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='BasketLine',
            fields=[
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='quantity')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='basket.basket')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='product.inventory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='product.product')),
            ],
            options={
                'verbose_name': 'basket line',
                'verbose_name_plural': 'basket lines',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
