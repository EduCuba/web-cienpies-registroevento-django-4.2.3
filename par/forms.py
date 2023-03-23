from django.contrib.auth import forms
#from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import models
from django.forms import fields
from django import forms
from django.forms.widgets import PasswordInput
from .models import Participante,Modalidad_Asistencia,Tipo_Participante
from eve.models import Evento
from django.core.exceptions import ValidationError





class ParticipanteForm(forms.ModelForm):
   
    
   # def clean(self):
   #     cleaned_data = super().clean()
   #     modalidad_asistencia = cleaned_data.get('modalidad_asistencia')
   #     if(not modalidad_asistencia):
   #         
   #         raise ValidationError("Lo logramos")
   #     return cleaned_data


    evento = forms.ModelChoiceField(
        queryset=Evento.objects.filter(estado=True)
        .order_by('nombre_evento')
    )
    
    tipo_participante = forms.ModelChoiceField(
        queryset=Tipo_Participante.objects.filter(estado=True)
        .order_by('descripcion_tipo_participante')
    )
    
    modalidad_asistencia = forms.ModelChoiceField(
        queryset=Modalidad_Asistencia.objects.filter(estado=True)
        .order_by('descripcion_modalidad_asistencia')
    )
        
    #evento_id = '3';
    class Meta:
        model=Participante
        fields = ['evento','apellido_participante','nombre_participante','empresa_participante','email_participante','telefono_participante',
                  'observaciones_participante','acompanante_de', 'cargo_participante','asistio_evento','confirmo_asistencia',
                  'tipo_participante','modalidad_asistencia','evento']
        labels = {'Apellido':"apellido_participante",
        'Nombre':"nombre_participante",
        'Email':"email_participante",
        'Teléfono':"telefono_participante",
        'Observaciones':"observaciones_participante",
        'Titular':"acompanante_de",
        }
        widget={'apellido_participante':forms.TextInput,
                'nombre_participante':forms.TextInput,
                'empresa_participante':forms.TextInput,
                'email_participante':forms.TextInput,
                'telefono_participante':forms.TextInput,
                'observaciones_participante':forms.TextInput,
                'acompanante_de':forms.TextInput               
                }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                     'class':'form-control'
                 })
        self.fields['tipo_participante'].empty_label="Seleccione Tipo"
        self.fields['modalidad_asistencia'].empty_label="Seleccione Modalidad"
        self.fields['evento'].empty_label="Seleccione Evento"
   
   

        
class BuscarParticipanteForm(forms.ModelForm):
    #evento = forms.ModelChoiceField(
    #    queryset=Evento.objects.filter(estado=True)
    #    .order_by('nombre_evento')
    #)
    
    class Meta:
        model=Participante
        fields = ['apellido_participante','nombre_participante','empresa_participante','evento']
        exclude = ['um','fm','uc','fc']
        labels = {'Apellido':"apellido_participante",
        'Nombre':"nombre_participante",
        'Empresa':"empresa_participante",
        
        }
        widget={'apellido_participante':forms.TextInput,
                'nombre_participante':forms.TextInput,
                'empresa_participante':forms.TextInput
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            print(field)
            self.fields[field].widget.attrs.update({
                'class': 'form-control'})
            if field!='evento':
               self.fields[field].required = False    
            
                
        
