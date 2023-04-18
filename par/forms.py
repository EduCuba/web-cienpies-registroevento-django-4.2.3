from django.contrib.auth import forms
#from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import models
from django.forms import fields
from django import forms
from django.forms.widgets import PasswordInput
from .models import Participante,Modalidad_Asistencia,Tipo_Participante
from eve.models import Evento
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _




class ParticipanteForm(forms.ModelForm):
   
    
    def clean(self):
        cleaned_data = super().clean()
        
        modalidad_asistencia = cleaned_data.get('modalidad_asistencia')
        evento=cleaned_data.get("evento")
        email_participante=cleaned_data.get("email_participante")
        modalidad_asistencia=cleaned_data.get("modalidad_asistencia")
        tipo_participante=cleaned_data.get("tipo_participante")
        mensaje='Verifique ingrese de datos'
        print('uno')
        if(not evento):
            print('uno a')
            #mensaje=f'Error verifique f'
            # form.add_error("evento","seleccione evento")
            self.add_error("evento", ValidationError(_("Evento no valido")))
            requestValido="OFF"
                    
        if (not email_participante):
            #print('uno b')
            #mensaje=f'Error verifique'
            #raise ValueError(_("El correo es un campo obligatorio."))
            self.add_error("email_participante", ValidationError(_("Ingrese cuenta de correo")))
                    
                        
        if(not modalidad_asistencia):
            mensaje=f'Error verifique'
            self.add_error("modalidad_asistencia","seleccione modalidad de asistencia")
            
            
                    #errors = form._errors.setdefault("modalidad_asistencia", ErrorList())
                    #errors.append(u"Seleccione modalidad de asistencia")
            requestValido="OFF"
        if(not tipo_participante):
                mensaje=f'Error verifique'
                    #form.add_error("tipo_participante","seleccione tipo de participante")  
                requestValido="OFF"
                
        print (cleaned_data)       
        return cleaned_data


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
                  'tipo_participante','modalidad_asistencia']
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
            
                
        

class CreateForm(forms.ModelForm):
    
    def __init__(self, *args, user=None, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        #if Participante is not None:
            #self.fields['apellido_participante'].initial = "edu"

    class Meta:
        model=Participante
        fields = ['evento','apellido_participante','nombre_participante','empresa_participante','email_participante','telefono_participante',
                  'observaciones_participante','acompanante_de', 'cargo_participante','asistio_evento','confirmo_asistencia',
                  'tipo_participante','modalidad_asistencia','evento']
        
    def clean(self):
        print("form 1")
        cleaned_data = super().clean()
        print("form 2")
        apellido_participante = cleaned_data('apellido_participante')
        print("form 3")
        nombre_participante = cleaned_data('nombre_participante')
        print("form 4")
        