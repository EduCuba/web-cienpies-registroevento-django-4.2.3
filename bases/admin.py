from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
#obsoleto
#from django.utils.translation import ugettext_lazy as _
from .models import Usuario
from .forms import UserCreationForm,UserChangeForm,UsuarioChangeForm,UsuarioCreationForm




# Register your models here.


class UsuarioAdmin(UserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    list_display = ('email', 'nombre', 'apellido')
    #list_filter = ('is_staff')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre','apellido')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','fecha_registro')}),
    )
  
  #  # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
  #  # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','nombre','apellido')
    ordering = ('email',)
    filter_horizontal = ()
    
    
#   Esto agrega la opcion usuario al panel de Django
admin.site.register(Usuario,UsuarioAdmin)    