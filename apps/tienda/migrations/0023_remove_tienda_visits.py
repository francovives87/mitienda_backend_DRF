# Generated by Django 4.1.7 on 2023-04-15 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0022_envios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tienda',
            name='visits',
        ),
    ]
