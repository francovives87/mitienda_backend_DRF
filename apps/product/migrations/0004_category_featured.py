# Generated by Django 4.1.7 on 2023-03-27 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_no_stock_product_with_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='destacada'),
        ),
    ]
