# Generated by Django 4.2.7 on 2024-02-13 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0013_alter_participante_codigo_qr'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participante',
            unique_together=set(),
        ),
        migrations.AlterIndexTogether(
            name='participante',
            index_together=set(),
        ),
    ]
