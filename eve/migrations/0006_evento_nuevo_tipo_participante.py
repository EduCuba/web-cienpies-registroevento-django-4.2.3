# Generated by Django 4.2.7 on 2024-02-07 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eve', '0005_alter_evento_modalidad_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='nuevo_tipo_participante',
            field=models.IntegerField(default=0),
        ),
    ]
