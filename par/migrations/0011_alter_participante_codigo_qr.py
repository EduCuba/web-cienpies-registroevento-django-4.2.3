# Generated by Django 4.2.7 on 2024-02-13 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0010_alter_participante_codigo_qr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='codigo_qr',
            field=models.CharField(max_length=100, null=True, verbose_name='codigo qr'),
        ),
    ]
