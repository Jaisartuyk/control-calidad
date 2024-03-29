# Generated by Django 4.2.6 on 2023-10-19 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_diario', '0006_reportediario_nombre_analista_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportediario',
            name='clasificacion',
            field=models.CharField(choices=[('16-20', '16-20'), ('21-25', '21-25'), ('26-30', '26-30'), ('31-35', '31-35'), ('36-40', '36-40'), ('51-60', '51-60'), ('61-70', '61-70'), ('71-90', '71-90')], default='16-20', max_length=10),
        ),
        migrations.AddField(
            model_name='reportediario',
            name='lote',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]
