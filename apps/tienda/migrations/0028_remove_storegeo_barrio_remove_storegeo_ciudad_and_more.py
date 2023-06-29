# Generated by Django 4.1.7 on 2023-04-22 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0027_alter_codigoqr_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storegeo',
            name='barrio',
        ),
        migrations.RemoveField(
            model_name='storegeo',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='storegeo',
            name='codigo_postal',
        ),
        migrations.RemoveField(
            model_name='storegeo',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='storegeo',
            name='pais',
        ),
        migrations.RemoveField(
            model_name='storegeo',
            name='subregion',
        ),
        migrations.AddField(
            model_name='storegeo',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='city_district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='house_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='municipality',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='postcode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='road',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='state_district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='storegeo',
            name='suburb',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='storegeo',
            name='region',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]