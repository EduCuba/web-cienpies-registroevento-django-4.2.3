# Generated by Django 4.2.7 on 2024-02-13 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0019_remove_participante_evento_qr_unico_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='codigo_qr',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='codigo qr'),
        ),
    ]
