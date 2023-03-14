from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import models
from django.forms import fields
from django import forms
from django.forms.widgets import PasswordInput
from .models import Usuario

#Estas clases son lo que modifica la vista de creación y modificación de usuario
class UsuarioCreationForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(UsuarioCreationForm,self).__init__(*args,**kwargs)
        
    class Meta:
        model = Usuario
        fields = ("email",)
    

class UsuarioChangeForm(UserChangeForm):
    def __init__(self,*args,**kwargs):
        super(UsuarioChangeForm,self).__init__(*args,**kwargs)
      #  super().__init__(*args, **kwargs).
    class Meta:
        model = Usuario
        fields = '__all__'
        
class Userform(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['email','nombre','apellido','password']
        widget = {'email': forms.EmailInput,
                   'password': forms.PasswordInput }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })        
    