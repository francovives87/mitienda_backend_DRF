# Generated by Django 4.1.7 on 2023-03-16 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_remove_tienda_category_tienda_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='domain',
            field=models.CharField(max_length=50, unique=True, verbose_name='dominio'),
        ),
    ]