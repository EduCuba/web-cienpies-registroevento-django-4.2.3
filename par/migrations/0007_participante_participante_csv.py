# Generated by Django 4.2.7 on 2023-12-23 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('par', '0006_participante_csv'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='participante_csv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='par.participante_csv'),
        ),
    ]
