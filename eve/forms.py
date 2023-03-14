from django.contrib.auth import forms
#from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import models
from django.forms import fields
from django import forms
from django.forms.widgets import PasswordInput
from .models import Modalidad_Evento,Evento




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
    class Meta:
        model=Evento
        fields = ['modalidad_evento','nombre_evento','estado']
        labels = {'Evento':"nombre_evento",
        'estado':"Estado"}
        widget={'nombre_evento':forms.TextInput}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                     'class':'form-control'
                 })
        self.fields['modalidad_evento'].empty_label="Seleccione Modalidad"
    