# Generated by Django 4.1.7 on 2023-04-03 22:24

import apps.tienda.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0018_alter_tiendaimages_logo_alter_tiendaimages_portada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiendaimages',
            name='logo',
            field=models.ImageField(blank=True, default='defaults/mitienda_logo_3_2_512.png', null=True, upload_to=functools.partial(apps.tienda.models.get_upload_path, *(), **{'field_name': 'logo'}), verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='tiendaimages',
            name='portada',
            field=models.ImageField(blank=True, default='defaults/portada1.jpg', null=True, upload_to=functools.partial(apps.tienda.models.get_upload_path, *(), **{'field_name': 'portada'}), verbose_name='portada'),
        ),
    ]
