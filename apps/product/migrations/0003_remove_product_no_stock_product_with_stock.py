# Generated by Django 4.1.7 on 2023-03-22 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_with_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='no_stock',
        ),
        migrations.AddField(
            model_name='product',
            name='with_stock',
            field=models.BooleanField(default=False, verbose_name='with_stock'),
        ),
    ]
