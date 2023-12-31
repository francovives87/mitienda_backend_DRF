# Generated by Django 4.1.7 on 2023-04-17 15:37

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_alter_userpersonaldata_dni'),
        ('product', '0006_remove_product_only_attribute_alter_images_image_and_more'),
        ('tienda', '0025_alter_storestatistics_options'),
        ('order', '0002_alter_anonymouspersonaldata_apellido_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('notas', models.CharField(blank=True, max_length=255, null=True, verbose_name='Notas')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('estado', models.CharField(default='en espera', max_length=20, verbose_name='estado')),
                ('metodo_pago', models.CharField(default='efectivo', max_length=20, verbose_name='Metodo de pago')),
                ('quantity_products', models.PositiveIntegerField(verbose_name='cantidad de productos')),
                ('visto', models.BooleanField(default=False, verbose_name='visto')),
                ('mercado_pago_approved', models.BooleanField(default=False, verbose_name='mercado_pago_approved')),
                ('pago', models.CharField(default='pendiente', max_length=11, verbose_name='pago')),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Ordenes',
            },
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='apellido',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='apellido'),
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='direccion',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='direccion'),
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='telefono'),
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('quantity', models.PositiveIntegerField(verbose_name='cantidad')),
                ('price_sale', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precion_venta')),
                ('price_off', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precion_en_oferta')),
                ('variacion_id', models.IntegerField(blank=True, null=True, verbose_name='Variacion_id')),
                ('options', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='opciones'), blank=True, null=True, size=None)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Orden', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Producto', to='product.product')),
            ],
            options={
                'verbose_name': 'Orden Detalle',
                'verbose_name_plural': 'Ordenes Detalles',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='anonymous_user_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.anonymouspersonaldata', verbose_name='anonymous_user_data'),
        ),
        migrations.AddField(
            model_name='order',
            name='envio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.envios', verbose_name='Envio'),
        ),
        migrations.AddField(
            model_name='order',
            name='personal_user_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userpersonaldata', verbose_name='Datos Personales'),
        ),
        migrations.AddField(
            model_name='order',
            name='tienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.tienda', verbose_name='Tienda'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
