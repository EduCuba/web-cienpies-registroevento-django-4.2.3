# Generated by Django 4.2.7 on 2024-02-13 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0015_participante_evento_qr_unico'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='participante',
            index=models.Index(fields=['evento', 'codigo_qr'], name='par_partici_evento__15baf8_idx'),
        ),
    ]