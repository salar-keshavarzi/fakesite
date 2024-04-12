# Generated by Django 5.0.3 on 2024-04-04 09:50

import django.db.models.deletion
import django.db.models.manager
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
            ],
            options={
                'verbose_name': 'shipping price',
                'verbose_name_plural': 'shipping prices',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='StoryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('title', models.CharField(max_length=48, verbose_name='title')),
                ('image', models.ImageField(upload_to='storyCategory/', verbose_name='image')),
                ('size', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=6, null=True, verbose_name='size (MB)')),
            ],
            options={
                'verbose_name': 'story category',
                'verbose_name_plural': 'story categories',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('image', models.ImageField(upload_to='collections/', verbose_name='image')),
                ('size', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=6, null=True, verbose_name='size (MB)')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='product.category')),
            ],
            options={
                'verbose_name': 'collection',
                'verbose_name_plural': 'collections',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('image', models.ImageField(upload_to='collections/', verbose_name='image')),
                ('size', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=6, null=True, verbose_name='size (MB)')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sliders', to='product.product')),
            ],
            options={
                'verbose_name': 'slider',
                'verbose_name_plural': 'sliders',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_time', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='modified time')),
                ('image', models.ImageField(upload_to='stories/', verbose_name='image')),
                ('size', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=6, null=True, verbose_name='size (MB)')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stories', to='product.product')),
                ('story_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='manager.storycategory')),
            ],
            options={
                'verbose_name': 'story',
                'verbose_name_plural': 'stories',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
