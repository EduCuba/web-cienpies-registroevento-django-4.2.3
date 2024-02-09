from django.contrib.auth import forms
#from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import models
from django.forms import fields
from django import forms
from django.forms.widgets import PasswordInput
from .models import Modalidad_Evento,Evento,Usuario_Evento
from par.models import Tipo_Participante
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ModalidadEventoForm(forms.ModelForm):
    #password = forms.CharField(widget=PasswordInput)
    
    class Meta:
        model = Modalidad_Evento
        fields = ['descripcion_modalidad_evento','estado']
        labels = {'descripcion_modalidad_evento':"Modalidad de Evento",
                  'estado':"Estado"}
        widget = {'descripcion_modalidad_evento': forms.TextInput}
        #           'password': forms.PasswordInput }

    # a cada elemento del form le agrega : class : form-control
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })        


class EventoForm(forms.ModelForm):
    modalidad_evento = forms.ModelChoiceField(
        queryset=Modalidad_Evento.objects.filter(estado=True)
        .order_by('descripcion_modalidad_evento')
    )
    '''
    nuevo_tipo_participante = forms.ModelChoiceField(
        queryset=Tipo_Participante.objects.filter(estado=True)
        .order_by('descripcion_tipo_participante')
    )'''
    class Meta:
        model=Evento
        fields = ['modalidad_evento','nombre_evento','nuevo_tipo_participante','estado']
        labels = {'Evento':"nombre_evento",
        'estado':"Estado",
        'nuevo_tipo_participante':"nuevo_tipo_participante"}
        
        widget={'nombre_evento':forms.TextInput,
                'nuevo_tipo_participante':forms.TextInput}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                     'class':'form-control'
                 })
        self.fields['modalidad_evento'].empty_label="Seleccione Modalidad"
        self.fields['nuevo_tipo_participante'].empty_label="Seleccione Tipo Participante"
    
    
    
class UsuarioEventoForm(forms.ModelForm):
   
    class Meta:
        model=Usuario_Evento
        fields = ['evento','usuario']
        labels = {'Evento':"nombre_evento",
        'usuario':"usuario"}
        widget={'nombre_evento':forms.TextInput}
        
        
    def clean(self):
        cleaned_data = super().clean()
        
        usuario = cleaned_data.get('usuario')
        evento=cleaned_data.get("evento")
        mensaje='Verifique ingrese de datos'
        print('uno UsuarioEventoForm forms.py')
        print(id)
        
        if(not evento or evento==0):
            print('uno a xxx')     
            self.add_error("evento", ValidationError(_("Evento no valido")))
            requestValido="OFF"
                        
        if(not usuario):
            print('uno c')
            mensaje=f'Error verifique'
            self.add_error("usuario",ValidationError(_("Seleccione modalidad de asistencia")))
            requestValido="OFF"
           
        print ("cleaned_data 58")               
             
        return self.cleaned_data
        
        
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                     'class':'form-control'
                 })
        self.fields['evento'].empty_label="Ingrese evento"
    