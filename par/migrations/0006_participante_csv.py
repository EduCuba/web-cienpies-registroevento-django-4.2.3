# Generated by Django 4.2.7 on 2023-12-22 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eve', '0004_usuario_evento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('par', '0005_remove_participante_par_partici_evento__c3492e_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participante_Csv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('archivo_csv', models.CharField(help_text='Archivo csv', max_length=260, verbose_name='Archivo')),
                ('cantidad', models.IntegerField()),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eve.evento')),
                ('uc', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('um', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Archivos',
            },
        ),
    ]