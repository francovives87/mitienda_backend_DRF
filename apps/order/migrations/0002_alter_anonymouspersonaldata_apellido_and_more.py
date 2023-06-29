# Generated by Django 4.1.7 on 2023-04-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='apellido',
            field=models.CharField(default='gomez', max_length=50, verbose_name='apellido'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='direccion',
            field=models.CharField(default='gaboto', max_length=80, verbose_name='direccion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='email',
            field=models.CharField(default='lorem@mail.com', max_length=100, verbose_name='email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='nombre',
            field=models.CharField(default='raul', max_length=50, verbose_name='Nombre'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='telefono',
            field=models.CharField(default='341558877', max_length=50, verbose_name='telefono'),
            preserve_default=False,
        ),
    ]