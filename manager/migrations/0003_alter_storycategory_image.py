# Generated by Django 5.0.3 on 2024-04-06 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_alter_storycategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storycategory',
            name='image',
            field=models.ImageField(upload_to='storyCategory/', verbose_name='image'),
        ),
    ]
