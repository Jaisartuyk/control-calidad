# Generated by Django 4.2.6 on 2023-10-25 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_diario', '0010_alter_reportediario_camarones_grandes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportediario',
            name='correctivos',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='reportediario',
            name='observaciones',
            field=models.TextField(blank=True),
        ),
    ]
