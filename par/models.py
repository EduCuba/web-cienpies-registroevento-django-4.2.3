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

from django.db.models import Deferrable, UniqueConstraint
from django.db.models import Q


class Tipo_Participante(ClaseModelo2):
    descripcion_tipo_participante=models.CharField(
        ('tipo participante'),
        max_length=30,
        unique=True,
        blank=False
    )
    
    tipo_identificacion_participante=models.CharField(
        max_length=30,
        blank=True,     
    )
    
                   
    background_tipo_participante=models.CharField(
        max_length=10,     
    )
    
   
    def __str__(self):
        return '{}:{}'.format(self.descripcion_tipo_participante,self.tipo_identificacion_participante)
    
    class Meta:
        verbose_name_plural = "Tipo de participantes"
        
        
    def delete(self, *args, **kwargs):
        print('modelo')
        print(self.descripcion_tipo_participante)
        if Participante.objects.filter(tipo_participante_id= self.pk).exists():
            raise Exception('Tipo de Participante se esta utilizando')  # or you can throw your custom exception here.
        super(Tipo_Participante, self).delete(*args, **kwargs)     
        

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
        
 
 
 
class Participante_Csv(ClaseModelo2):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT,null=False, blank=False)
    archivo_csv = models.CharField(('Archivo'),
    help_text='Archivo csv',
        max_length=260,
        null=False, blank=False)
    cantidad = models.IntegerField(null=False,blank=False)
    
    def __str__(self):
        return '{}:{}'.format(self.archivo_csv,
                                             self.cantidad,
                                            )
    
    
     
    
    class Meta:
        verbose_name_plural = "Archivos"
        
        
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
    participante_csv = models.ForeignKey(Participante_Csv, on_delete=models.PROTECT,null=True, blank=True)
    codigo_qr=models.CharField(('codigo qr'),max_length=100,null=True,default=None, blank=True)
    
    def __str__(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.apellido_participante,
                                             self.nombre_participante,
                                             self.empresa_participante,
                                             self.email_participante,
                                             self.asistio_evento,
                                             self.tipo_participante.descripcion_tipo_participante,
                                             self.tipo_participante.pk,
                                             self.modalidad_asistencia.descripcion_modalidad_asistencia,
                                             self.codigo_qr,
                                             self.pk)
    
   
   
    class Meta:
        verbose_name_plural = "Participantes"
        
        constraints = [
            models.UniqueConstraint(fields=['evento', 'codigo_qr'], 
                                    condition=(~models.Q(codigo_qr=None)),
                                    name='const_evento_qr_unico')
                    ] 
        indexes = [
           models.Index(fields=['evento', 'codigo_qr'], name="idx_par_evento_qr_unico") ]
    
    
  
       # indexes = [models.Index(fields=["evento", "codigo_qr"],name="evento_qr_idx")],
       # constraints = [
       #     models.UniqueConstraint(fields=['evento', 'codigo_qr'], 
       #                             condition=(models.Q(codigo_qr=None)),
       #                             name='evento_qr_unico')
       #             ] 

        #UniqueConstraint(fields=["evento,codigo_qr"], condition=(~(Q(codigo_qr=None))), name="unique_evento_qr")   
       
                          
#indexes = [
 #           models.Index(fields=["evento", "codigo_qr"],name="evento_qr_idx"),

# unique_together = ["evento", "codigo_qr"]
#        index_together=["evento", "codigo_qr"]
       
   
#class Meta:
#       indexes = [
#            models.Index(fields=['evento',]),
#            models.Index(fields=['last_name',]),
#            models.Index(fields=['-date_of_birth',]),
#]        



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
    
    

   