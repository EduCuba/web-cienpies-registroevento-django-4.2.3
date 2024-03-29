# Generated by Django 4.2.7 on 2024-02-12 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve', '0006_evento_nuevo_tipo_participante'),
        ('par', '0007_participante_participante_csv'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='codigo_qr',
            field=models.CharField(max_length=100, null=True, verbose_name='codigo qr'),
        ),
        migrations.AlterUniqueTogether(
            name='participante',
            unique_together={('evento', 'codigo_qr')},
        ),
        migrations.AddIndex(
            model_name='participante',
            index=models.Index(fields=['evento', 'codigo_qr'], name='evento_qr_idx'),
        ),
    ]
