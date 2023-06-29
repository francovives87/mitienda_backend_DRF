# Generated by Django 4.1.7 on 2023-03-23 02:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0011_alter_tienda_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('product_categories', models.IntegerField(verbose_name='product_categories')),
                ('product_products', models.IntegerField(verbose_name='product_products')),
                ('blog_categories', models.IntegerField(verbose_name='blog_categories')),
                ('blog_entries', models.IntegerField(verbose_name='blog_entries')),
                ('images_x_products', models.IntegerField(verbose_name='imagenes_x_producto')),
                ('images_x_services', models.IntegerField(verbose_name='imagenes_x_servicio')),
                ('images_x_entries', models.IntegerField(verbose_name='imagenes_x_entrada')),
                ('images_sliders', models.IntegerField(verbose_name='imagenes_sliders')),
                ('services_categories', models.IntegerField(verbose_name='servicios_categorias')),
                ('services', models.IntegerField(verbose_name='servicios')),
                ('orders', models.IntegerField(verbose_name='ordenes')),
                ('bookings', models.IntegerField(verbose_name='reservas')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
            },
        ),
        migrations.AddField(
            model_name='tienda',
            name='plan',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='tienda_plan', to='tienda.plan', verbose_name='Plan'),
            preserve_default=False,
        ),
    ]