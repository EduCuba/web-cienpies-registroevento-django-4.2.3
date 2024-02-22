# Generated by Django 4.2.7 on 2024-02-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0024_alter_participante_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participante',
            options={'verbose_name_plural': 'Participantes'},
        ),
        migrations.AddIndex(
            model_name='participante',
            index=models.Index(fields=['evento', 'codigo_qr'], name='par_partici_evento__15baf8_idx'),
        ),
        migrations.AddConstraint(
            model_name='participante',
            constraint=models.UniqueConstraint(condition=models.Q(('codigo_qr', None), _negated=True), fields=('evento', 'codigo_qr'), name='evento_qr_unico'),
        ),
    ]
