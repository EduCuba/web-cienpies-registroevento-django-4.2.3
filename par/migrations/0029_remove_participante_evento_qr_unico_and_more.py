# Generated by Django 4.2.7 on 2024-03-20 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0028_alter_participante_codigo_qr'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='participante',
            name='evento_qr_unico',
        ),
        migrations.RemoveIndex(
            model_name='participante',
            name='par_evento_qr_unico',
        ),
    ]