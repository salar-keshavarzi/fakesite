# Generated by Django 5.0.3 on 2024-04-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_transaction_is_paid_transaction_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='ip',
            field=models.CharField(blank=True, editable=False, max_length=48, null=True, verbose_name='ip'),
        ),
    ]
