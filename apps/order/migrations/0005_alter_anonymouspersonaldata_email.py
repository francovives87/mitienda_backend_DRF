# Generated by Django 4.1.7 on 2023-05-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_anonymouspersonaldata_apellido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymouspersonaldata',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='email'),
        ),
    ]
