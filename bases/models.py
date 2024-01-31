from django.db import models

from django.utils import timezone
#from django.utils.http import urlquote
#  correct import (Django v4+)
#from django.utils.http import url_has_allowed_host_and_scheme

#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .managers import UsuarioManager

from urllib.parse import (
    ParseResult,
    SplitResult,
    _coerce_args,
    _splitnetloc,
    _splitparams,
    scheme_chars,
)
from urllib.parse import urlencode as original_urlencode
from urllib.parse import uses_params

from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey
# Create your models here.

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('cuenta correo'), max_length=100, unique=True)
    nombre = models.CharField(_('nombres'), max_length=50, blank=False)
    apellido = models.CharField(_('apellidos'), max_length=50, blank=False)
    is_staff = models.BooleanField(_('is_staff'), default=False, help_text=('Indica si puede iniciar sesión de admin'))
    is_active = models.BooleanField(_('active'), default=True, help_text=('esta activo'))
    fecha_registro = models.DateTimeField(_('fecha registro'), default=timezone.now, help_text=('Indica si puede iniciar sesión de admin'))
   
   # se setea para que el campo email sea el principal 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]
    
    objects = UsuarioManager()
    
    # en el meta se indica que el nombre las estiqueta se muestre lo configurado en la propiedad :
    # models.EmailField
    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        
    #def get_absolute_url(self):
    #    return "/users/%s" % urlquote(self.email)
    
    def get_absolute_url(self):
        return "/users/%s/" % self.email
        
    
    
    def get_full_name(self):
        full_name="%s %s" % (self.nombre,self.apellido)
        return full_name.strip()
    
    def get_short_name(self):
        return self.nombre
    
    #    def get_absolute_url(self):
    #    return "/users/%s" % urlquote(self.email)
        
   # @property
   # def get_is_staff(self):
        #"Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
   #     return self.is_staff
    
    
class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.PROTECT)
    um = models.IntegerField(blank=True,null=True)
    
    # class Meta indica a Django que no cree este modelo
    class Meta:
        abstract=True


class ClaseModelo2(models.Model):
    estado = models.BooleanField(default=True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    #uc = models.ForeignKey(User, on_delete=models.CASCADE)
    #um = models.IntegerField(blank=True,null=True)
    uc = UserForeignKey(auto_user_add=True,related_name='+')
    um = UserForeignKey(auto_user=True,related_name='+')
    
    # class Meta indica que no se cree este modelo
    class Meta:
        abstract=True
        
    
