# Generated by Django 4.2.7 on 2023-12-07 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0004_participante_par_partici_evento__c3492e_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='participante',
            name='par_partici_evento__c3492e_idx',
        ),
    ]