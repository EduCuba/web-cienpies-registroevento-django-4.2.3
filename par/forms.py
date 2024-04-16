from django.contrib.auth import forms
#from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import models
from django.forms import fields
from django import forms
from django.forms.widgets import PasswordInput
from .models import Participante,Modalidad_Asistencia,Tipo_Participante,Participante_Csv
from eve.models import Evento
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _




class ParticipanteForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)
      
    
    def clean(self):
        
        cleaned_data = super().clean()
        modalidad_asistencia = cleaned_data.get('modalidad_asistencia')
        evento=cleaned_data.get("evento")
        print(cleaned_data.get("evento"))
        print("ddddd")
        email_participante=cleaned_data.get("email_participante")
        #modalidad_asistencia=cleaned_data.get("modalidad_asistencia")
        modalidad_asistencia=cleaned_data.get("modalidad_asistencia")
        tipo_participante=cleaned_data.get("tipo_participante")
        #codigo_qr=cleaned_data.get("codigo_qr")
        mensaje='Verifique ingrese de datos'
        print('uno ParticipanteForm')
        #print(codigo_qr)
        print("valid 11111111111111111111111111")
        
        '''
        if (codigo_qr==None):
            print("esta vacio")
        else:
            codigo_qr=codigo_qr.lower()
            codigo_qr=codigo_qr.strip()
            if (codigo_qr=='none' or codigo_qr==''):
                print('cambiando a nulo')
                cleaned_data["codigo_qr"]=None
        '''        
        print("salvame")
        if(not evento):
            print('no existe evento PORQUE: ')
            print(evento)
            #mensaje=f'Error verifique f'
            # form.add_error("evento","seleccione evento")
            self.add_error("evento", ValidationError(_("Evento no valido")))
            requestValido="OFF"
                    
        #if (not email_participante):
        #    mensaje=f'Error verifique'
        #    self.add_error("email_participante", ValidationError(_("Ingrese cuenta de correo")))
        #    requestValido="OFF"        
                        
        if(not modalidad_asistencia):
            print('uno c')
            print(modalidad_asistencia)
            mensaje=f'Error verifique'
            self.add_error("modalidad_asistencia",ValidationError(_("Seleccione modalidad de asistencia")))
            
            
                    #errors = form._errors.setdefault("modalidad_asistencia", ErrorList())
                    #errors.append(u"Seleccione modalidad de asistencia")
            requestValido="OFF"
           
        if(not tipo_participante):
            print('uno d')
            mensaje=f'Error verifique'
            #form.add_error("tipo_participante","seleccione tipo de participante")  
            requestValido="OFF"
        print ("cleaned_data 58")               
             
        return self.cleaned_data
    
    


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
                  'tipo_participante','modalidad_asistencia','participante_csv']
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
        #'codigo_qr': forms.TextInput(attrs={'readonly':'readonly'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
            
        self.fields['tipo_participante'].empty_label="Seleccione Tipo"
        self.fields['modalidad_asistencia'].empty_label="Seleccione Modalidad"
        self.fields['evento'].empty_label="Seleccione Evento"
        

class ParticipanteFormImportacion(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
      
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['codigo_qr'].required = False
   
    
    def clean(self):
        
        cleaned_data = super().clean()
        modalidad_asistencia = cleaned_data.get('modalidad_asistencia')
        evento=cleaned_data.get("evento")
        email_participante=cleaned_data.get("email_participante")
        #modalidad_asistencia=cleaned_data.get("modalidad_asistencia")
        modalidad_asistencia=cleaned_data.get("modalidad_asistencia")
        tipo_participante=cleaned_data.get("tipo_participante")
        #codigo_qr=cleaned_data.get("codigo_qr")
        mensaje='Verifique ingrese de datos'
        print('uno ParticipanteForm')
        #print(codigo_qr)
        print("valid 11111111111111111111111111")
        
        
        if (codigo_qr==None):
            print("esta vacio jjjjjjjjjjjjjjjjj 160")
            cleaned_data["codigo_qr"]=None
        else:
            codigo_qr=codigo_qr.lower()
            codigo_qr=codigo_qr.strip()
            if (codigo_qr=='none' or codigo_qr==''):
                print('cambiando a nulo')
                cleaned_data["codigo_qr"]=None
                self.add_error("codigo_qr", ValidationError(_("Código QR es obligatorio")))
              
          
        if(not evento):
            print('no existe evento: ')
            print(evento)
            #mensaje=f'Error verifique f'
            # form.add_error("evento","seleccione evento")
            self.add_error("evento", ValidationError(_("Evento no valido")))
            requestValido="OFF"
                    
        #if (not email_participante):
        #    mensaje=f'Error verifique'
        #    self.add_error("email_participante", ValidationError(_("Ingrese cuenta de correo")))
        #    requestValido="OFF"        
                        
        if(not modalidad_asistencia):
            print('uno c')
            print(modalidad_asistencia)
            mensaje=f'Error verifique'
            self.add_error("modalidad_asistencia",ValidationError(_("Seleccione modalidad de asistencia")))
            
            
                    #errors = form._errors.setdefault("modalidad_asistencia", ErrorList())
                    #errors.append(u"Seleccione modalidad de asistencia")
            requestValido="OFF"
           
        if(not tipo_participante):
            print('uno d')
            mensaje=f'Error verifique'
            #form.add_error("tipo_participante","seleccione tipo de participante")  
            requestValido="OFF"
        print ("cleaned_data 58")               
             
        return self.cleaned_data
    
    


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
                  'tipo_participante','modalidad_asistencia','participante_csv','codigo_qr']
        labels = {'Apellido':"apellido_participante",
        'Nombre':"nombre_participante",
        'Email':"email_participante",
        'Teléfono':"telefono_participante",
        'Observaciones':"observaciones_participante",
        'Titular':"acompanante_de",
        'QR':"codigo_qr"
        }
        widget={'apellido_participante':forms.TextInput,
                'nombre_participante':forms.TextInput,
                'empresa_participante':forms.TextInput,
                'email_participante':forms.TextInput,
                'telefono_participante':forms.TextInput,
                'observaciones_participante':forms.TextInput,
                'acompanante_de':forms.TextInput,
                'codigo_qr':forms.TextInput
                        
                }
        #'codigo_qr': forms.TextInput(attrs={'readonly':'readonly'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
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
            #print(field)
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
        
        
        
class TipoParticipanteForm(forms.ModelForm):
    #password = forms.CharField(widget=PasswordInput)
    
    class Meta:
        model = Tipo_Participante
        fields = ['descripcion_tipo_participante','tipo_identificacion_participante','background_tipo_participante']
        labels = {'descripcion_tipo_participante':"Tipo Participante",
                  'tipo_identificacion_participante':"Tipo Identificación",
                  'background_tipo_participante':"Background"
                  }
        widget = {'descripcion_tipo_participante': forms.TextInput,
                  'tipo_identificacion_participante': forms.TextInput,
                  'background_tipo_participante': forms.TextInput
                  }
        

    # a cada elemento del form le agrega : class : form-control
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })        
        
        
        
class ModalidadAsistenciaForm(forms.ModelForm):
    #password = forms.CharField(widget=PasswordInput)
    
    class Meta:
        model = Modalidad_Asistencia
        fields = ['descripcion_modalidad_asistencia','color_modalidad_asistencia']
        labels = {'descripcion_modalidad_asistencia':"Modalidad Asistencia",
                  'color_modalidad_asistencia':"Color Letra"}
        widget = {'descripcion_modalidad_asistencia': forms.TextInput,
                  'color_modalidad_asistencia': forms.TextInput
                  }
        
    # a cada elemento del form le agrega : class : form-control
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })        
                
                
class ParticipanteCsvForm(forms.ModelForm):
    class Meta:
        model=Participante_Csv
        fields = ['archivo_csv','evento','cantidad']
        labels = {'Evento':"nombre_evento",
        'Archivo':"archivo_csv",
        'Cantidad':"cantidad"}
        widget={'archivo_csv':forms.TextInput,
                'id':forms.TextInput}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        #super(ParticipanteCsvForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                     'class':'form-control'
                 })
        self.fields['evento'].empty_label="Seleccione Evento form"
        
        
class ParticipanteFormImportacionSinQr(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.fields['codigo_qr'].required = False
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['codigo_qr'].required = False
    
    def clean(self):
        
        cleaned_data = super().clean()
        modalidad_asistencia = cleaned_data.get('modalidad_asistencia')
        evento=cleaned_data.get("evento")
        email_participante=cleaned_data.get("email_participante")
        #modalidad_asistencia=cleaned_data.get("modalidad_asistencia")
        modalidad_asistencia=cleaned_data.get("modalidad_asistencia")
        tipo_participante=cleaned_data.get("tipo_participante")
        codigo_qr=cleaned_data.get("codigo_qr")
        mensaje='Verifique ingrese de datos'
        print('uno ParticipanteForm')
        #print(codigo_qr)
        print("valid 11111111111111111111111111")
        
        
       
        if(not evento):
            print('no existe evento: ')
            print(evento)
            #mensaje=f'Error verifique f'
            # form.add_error("evento","seleccione evento")
            self.add_error("evento", ValidationError(_("Evento no valido")))
            requestValido="OFF"
            
        if (codigo_qr==None):
            print("esta vacio jjjjjjjjjjjjjjjjj 409")
            cleaned_data["codigo_qr"]=None
        else:
            codigo_qr=codigo_qr.lower()
            codigo_qr=codigo_qr.strip()
            if (codigo_qr=='none' or codigo_qr==''):
                print('cambiando a nulo')
                cleaned_data["codigo_qr"]=None
                #self.add_error("codigo_qr", ValidationError(_("Código QR es obligatorio")))
              
           # cleaned_data["codigo_qr"]="Bingo"
            #request.data["codigo_qr"] = None
            
            #form.instance.status = 'r'    
                    
        #if (not email_participante):
        #    mensaje=f'Error verifique'
        #    self.add_error("email_participante", ValidationError(_("Ingrese cuenta de correo")))
        #    requestValido="OFF"        
                        
        if(not modalidad_asistencia):
            print('uno c')
            print(modalidad_asistencia)
            mensaje=f'Error verifique'
            self.add_error("modalidad_asistencia",ValidationError(_("Seleccione modalidad de asistencia")))
            
            
                    #errors = form._errors.setdefault("modalidad_asistencia", ErrorList())
                    #errors.append(u"Seleccione modalidad de asistencia")
            requestValido="OFF"
           
        if(not tipo_participante):
            print('uno d')
            mensaje=f'Error verifique'
            #form.add_error("tipo_participante","seleccione tipo de participante")  
            requestValido="OFF"
        print ("cleaned_data 58")               
             
        return self.cleaned_data
    
    


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
                  'tipo_participante','modalidad_asistencia','participante_csv','codigo_qr']
        labels = {'Apellido':"apellido_participante",
        'Nombre':"nombre_participante",
        'Email':"email_participante",
        'Teléfono':"telefono_participante",
        'Observaciones':"observaciones_participante",
        'Titular':"acompanante_de",
        'QR':"codigo_qr"
        }
        widget={'apellido_participante':forms.TextInput,
                'nombre_participante':forms.TextInput,
                'empresa_participante':forms.TextInput,
                'email_participante':forms.TextInput,
                'telefono_participante':forms.TextInput,
                'observaciones_participante':forms.TextInput,
                'acompanante_de':forms.TextInput,
                'codigo_qr':forms.TextInput
                        
                }
        #'codigo_qr': forms.TextInput(attrs={'readonly':'readonly'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})
        self.fields['tipo_participante'].empty_label="Seleccione Tipo"
        self.fields['modalidad_asistencia'].empty_label="Seleccione Modalidad"
        self.fields['evento'].empty_label="Seleccione Evento"
        
      