from django.db import models

from bases.models import ClaseModelo2,Usuario
#from par.models import Tipo_Participante

# Create your models here.


class Modalidad_Evento(ClaseModelo2):
  descripcion_modalidad_evento = models.CharField(
      max_length=30,
      help_text='Modalidad de Evento',
      blank=False,
      unique=True
  )
  
  ''' 
  def delete(self, *args, **kwargs):
        if Evento.objects.filter(modalidad_evento_id= self.pk).exists():
            raise Exception('Modalidad esta siendo utilizada en Evento(s)') 
           # or you can throw your custom exception here.
        super(Modalidad_Evento, self).delete(*args, **kwargs)
  '''
  def __str__(self):
    return '{}'.format(self.descripcion_modalidad_evento)

  class Meta:
      verbose_name_plural ='Modalidad_de_eventos'
      
      
      
class Evento(ClaseModelo2):
    modalidad_evento = models.ForeignKey(Modalidad_Evento, on_delete=models.PROTECT)
    nombre_evento = models.CharField(
        max_length=100,
        help_text='Evento',
        blank=False,
        unique=True
    )
    nuevo_tipo_participante= models.IntegerField(default=0)  
    asigna_qr_registro = models.BooleanField(('Se asigna QR al registrarse'),default=False)
    imprime_etiqueta_registro = models.BooleanField(('Se imprime etiqueta al registrarse'),default=False) 
    #nuevo_tipo_participante=models.ForeignKey(Tipo_Participante, on_delete=models.PROTECT)
    
    
    def __str__(self):
        return '{}:{}:{}'.format(self.id,self.nombre_evento,self.nuevo_tipo_participante)
    
    #sobreescribimos el metodo save para grabar con mayusculas
    #def save(self):
    #    self.descripcion = self.descripcion.upper()
    #    super(SubCategoria, self).save()
        
    class Meta:
        verbose_name_plural = "Eventos"
        ordering = ['nombre_evento']
        #creamos un inique compuesto para evitar duplicidad de subcategoria
        ###unique_together = ('categoria','descripcion')
        
      

class Usuario_Evento(ClaseModelo2):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento =  models.ForeignKey(Evento, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}:{}'.format(self.usuario,self.evento)
    
    class Meta:
        verbose_name_plural = "Usuario Eventos"


#class Meta:
#       indexes = [
#            models.Index(fields=['first_name',]),
#            models.Index(fields=['last_name',]),
#            models.Index(fields=['-date_of_birth',]),
#]

#class Meta:
#       indexes = [
#           models.Index(fields=['last_name', 'first_name',]),
#           models.Index(fields=['-date_of_birth',]),
#]

 #class Meta:
  #      unique_together= (('content', 'ip'),)