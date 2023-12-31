# Generated by Django 4.1.7 on 2023-05-16 22:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userpersonaldata_dni'),
        ('tienda', '0030_storesettings_order_email_storesettings_order_wp'),
    ]

    operations = [
        migrations.CreateModel(
            name='TiendaVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.tienda', verbose_name='tienda')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.visitor', verbose_name='visitor')),
            ],
            options={
                'verbose_name': 'TiendaVisitor',
                'verbose_name_plural': 'TiendaVisitor',
            },
        ),
    ]
