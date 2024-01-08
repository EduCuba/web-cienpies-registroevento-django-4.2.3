from django.db import models

from bases.models import ClaseModelo2,Usuario
# Create your models here.


class Modalidad_Evento(ClaseModelo2):
  descripcion_modalidad_evento = models.CharField(
      max_length=30,
      help_text='Modalidad de Evento',
      blank=False,
      unique=True
  )
  
  def __str__(self):
    return '{}'.format(self.descripcion_modalidad_evento)

  class Meta:
      verbose_name_plural ='Modalidad_de_eventos'
      
      
      
class Evento(ClaseModelo2):
    modalidad_evento = models.ForeignKey(Modalidad_Evento, on_delete=models.CASCADE)
    nombre_evento = models.CharField(
        max_length=100,
        help_text='Evento',
        blank=False,
        unique=True
    )
    
    def __str__(self):
        return '{}'.format(self.nombre_evento)
    
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