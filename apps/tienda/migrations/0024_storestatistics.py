# Generated by Django 4.1.7 on 2023-04-15 18:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0023_remove_tienda_visits'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('visits', models.IntegerField(default=0, verbose_name='visitas')),
                ('wp_contacts', models.IntegerField(default=0, verbose_name='wp_contactos')),
                ('wp_products', models.IntegerField(default=0, verbose_name='wp_products')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_statistics', to='tienda.tienda', verbose_name='Tienda')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
