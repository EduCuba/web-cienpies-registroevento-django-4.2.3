from django.db import models
from django.db import migrations, models

from bases.models import ClaseModelo2
# Create your models here.


#Para los signals
#from django.db.models.signals import post_save, post_delete
#from django.dispatch import receiver
#from django.contrib.auth.views import login, logout

#from django.db.models import Sum
# Create your models here.
from eve.models import Evento

class Tipo_Participante(ClaseModelo2):
    descripcion_tipo_participante=models.CharField(
        ('tipo participante'),
        max_length=30,
        unique=True,
        blank=False
    )
    
    
    background_tipo_participante=models.CharField(
        max_length=10,     
    )
    
    def __str__(self):
        return '{}'.format(self.descripcion_tipo_participante)
    
    class Meta:
        verbose_name_plural = "Tipo de participantes"
        

class Modalidad_Asistencia(ClaseModelo2):
    descripcion_modalidad_asistencia=models.CharField(
        max_length=20,
        help_text='Modalidad de Asistencia',
        unique=True,
        blank=False
    )
    color_modalidad_asistencia=models.CharField(
        max_length=10,     
    )
    
    def __str__(self):
        return '{}'.format(self.descripcion_modalidad_asistencia)
    
    class Meta:
        verbose_name_plural = "Modalidad de asistencia"
        
        
        
class Participante(ClaseModelo2):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT,null=False, blank=False)
    tipo_participante = models.ForeignKey(Tipo_Participante, on_delete=models.PROTECT,null=False, blank=False)
    modalidad_asistencia = models.ForeignKey(Modalidad_Asistencia, on_delete=models.PROTECT,null=False, blank=False)
    nombre_participante=models.CharField(('nombre'),
        max_length=50,
        null=False, blank=False)
    apellido_participante=models.CharField(('apellido'),
        max_length=50,
        null=False, blank=False)
    asistio_evento = models.BooleanField(('Asistio'),default=False)
    confirmo_asistencia = models.BooleanField(('Confirmo asistencia'),default=True)
    email_participante = models.EmailField(('cuenta correo'), max_length=100, unique=False)
    telefono_participante=models.CharField(('teléfono'),
        max_length=50,
        null=False, blank=True)
    empresa_participante=models.CharField(('empresa'),
        max_length=150,
        null=False, blank=True)
    cargo_participante=models.CharField(('cargo'),
        max_length=150,
        null=False, blank=True)
    observaciones_participante=models.CharField(('observaciones'),
        max_length=250,
        null=False, blank=True)
    acompanante_de=models.CharField(('acompañante de'),
        max_length=100,
        null=False, blank=True)
    
    def __str__(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.apellido_participante,
                                             self.nombre_participante,
                                             self.empresa_participante,
                                             self.email_participante,
                                             self.asistio_evento,
                                             self.tipo_participante.descripcion_tipo_participante,
                                             self.tipo_participante.pk,
                                             self.modalidad_asistencia.descripcion_modalidad_asistencia,
                                             self.pk)
    
    
    class Meta:
        verbose_name_plural = "Participantes"



#class Actualiza_Participante(migrations.Migration):

 #   dependencies = [('0001_initial')]

    #operations = [
    #    migrations.DeleteModel('Tribble'),
    #     migrations.AlterField(
    #        model_name='Participante',
    #        name='email',
    #        field=models.EmailField(null=False, verbose_name='email_participante', blank=True, max_length=100, unique=False),
    #    ),        
    #]