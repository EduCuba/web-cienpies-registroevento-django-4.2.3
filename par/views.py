from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

#permisos para validar acceso de funciones
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *

from .models import Participante, Tipo_Participante, Modalidad_Asistencia

from .forms import BuscarParticipanteForm,ParticipanteForm,CreateForm,TipoParticipanteForm,\
                   ModalidadAsistenciaForm,Participante_Csv,ParticipanteCsvForm,ParticipanteFormImportacion,ParticipanteFormImportacionSinQr


from bases.views import SinPrivilegios,SinPrivilegiosAjax
from eve.views import lista_Eventos_Por_Acceso

from eve.models import Evento, Usuario_Evento
from bases.models import Usuario

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.http import JsonResponse

from django.http import JsonResponse
from django.core.serializers import serialize
import json

from django.core.exceptions import ValidationError
# Create your views here.
from django.forms.utils import ErrorList
from django.utils.translation import gettext as _

from itertools import chain


from urllib.request import Request, urlopen
from urllib.error import HTTPError

#from email_validator import validate_email
from email_validator import validate_email, EmailNotValidError
import re
from django.db import transaction
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Count


#class ParticipanteList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
class ParticipanteList(ListView):
    #permission_required = 'eve.view_modalidad_evento'
    template_name = "par/registro_list.html"
    login_url = 'config:login'
    model = Participante
    context_object_name = 'obj'   

#@login_required(login_url='/login/')
#@permission_required('cmp.view_comprasenc', login_url='bases:sin_privilegios')
class xx_buscarparticipante():
    #permission_required = 'eve.add_evento'
    template_name = "eve/evento_form.html"
    model = Participante
    
    context_object_name = "obj"
    form_class = BuscarParticipanteForm
    success_url = reverse_lazy("eve:evento_list")
    login_url ="config:login"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)      
    

@login_required(login_url='config:login')
@permission_required('par.view_participante', login_url='config:home')
def buscarparticipante(request,participante_id=None):
#    class ModalidadEventoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'par.view_participante'

    template_name="par/busca_participante.html"
   
    form_compras={}
    contexto={}
    par_evento_id=0
    nombre=''
    apellido =''
    evento=0
    #lisparb=""
    print('edu 01')
    pkUser=request.user.pk
  
    if request.method=='GET':
        #print('es geeeeeeeeetttttttttttttt')
        #Formulario creado en forms.py
        form_buscar=BuscarParticipanteForm()
        #print('edu 02')
        lisEventos = lista_Eventos_Por_Acceso(pkUser,request.user.is_staff,"O")
        #print('edu 03')
        
        '''if request.user.is_staff:
           lisEventos = Evento.objects.all().only('id','estado','nombre_evento')
           #lisEventos = ""         
        else:
            #filtra por relacion
            lisEventos = Evento.objects.filter(usuario_evento__usuario_id=pkUser).only('id','estado','nombre_evento')
        '''

 
      
        #crea objeto vacio
        lispar=""
       
        
        #En el contexto definimos que mandamos a la plantilla
        
        contexto={'eve':form_buscar,'lispar':lispar, 'liseventos':lisEventos}
        # la impresion de contexto ejecutara consulta a la BD
        #print(contexto)
        return render(request, template_name,contexto )    
        
    if request.method=='POST':    
        #print('es pooooooooooossssttt')
        
        apellido_participante = request.POST.get("apellido_participante")
        nombre_participante = request.POST.get("nombre_participante")
        empresa_participante = request.POST.get("empresa_participante")
        evento = request.POST.get("evento")
        #print(apellido_participante)    
        #print(nombre_participante)    
        #print("empresa")
        #print(empresa_participante)
        #print(evento)  
        if (evento=='0'):
            #print('Seleccione Evento') 
            contexto={'rpta':'OFF',
                  'lispar':'',
                  'mensaje':'Seleccione Evento'}  
        else:    
        
            if (len(empresa_participante)==0):  
                
                if (len(apellido_participante) == 0 and len(nombre_participante) == 0):    
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento)).
                    values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                    #print('busqueda solo por evento')
                else:    
                    if (len(apellido_participante) > 0 and len(nombre_participante) > 0):    
                        # Utilizar esta linea para Postgresql
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__unaccent__icontains=apellido_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).
                        #lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__icontains=apellido_participante) & Q(nombre_participante__icontains=nombre_participante)).
                        values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                        #print('busqueda por apellido y nombre : caso empresa vacio')
                    else:
                        if (nombre_participante == ""):
                            # Utilizar esta linea para Postgresql
                            lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__unaccent__icontains=apellido_participante)).
                            #lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__icontains=apellido_participante)).
                            values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                            "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                            #print('busqueda por apellido :  empresa vacio')
                        else:
                            # Utilizar esta linea para Postgresql
                            lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(nombre_participante__unaccent__icontains=nombre_participante)).
                            #lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(nombre_participante__icontains=nombre_participante)).
                            values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                            "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                            #print('busqueda por nombre caso empresa vacia')
                
            else:
                if (len(apellido_participante) > 0 and len(nombre_participante) > 0):
                    # Utilizar esta linea para Postgresql    
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(apellido_participante__unaccent__icontains=apellido_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).
                    #lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__icontains=empresa_participante) & Q(apellido_participante__icontains=apellido_participante) & Q(nombre_participante__icontains=nombre_participante)).
                    values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                    #print('busqueda por empresa, apellido y nombre : caso 4')
                else:    
                    if (nombre_participante == ""):
                        # Utilizar esta linea para Postgresql
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(apellido_participante__unaccent__icontains=apellido_participante)).
                        #lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__icontains=empresa_participante) & Q(apellido_participante__icontains=apellido_participante)).
                        values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                        #print('busqueda por empresa y apellid : caso 5')
                    else:    
                        # Utilizar esta linea para Postgresql
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).
                        #lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__icontains=empresa_participante) & Q(nombre_participante__icontains=nombre_participante)).
                        values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                        #print('caso empresa y nombre')
                
                        
            #print('json es') 
            contexto={'rpta':'OK',
                  'lispar':lispar}            
       #print(contexto)                    
    return JsonResponse(contexto)
        
    return render(request, template_name, contexto)    



@login_required(login_url='config:login')
@permission_required('par.view_participante', login_url='config:home')
def lecturaqrevento(request,participante_id=None):
#    class ModalidadEventoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'par.view_participante'

    template_name="par/lectura_qr_evento.html"
   
    form_compras={}
    contexto={}
    par_evento_id=0
    nombre=''
    apellido =''
    evento=0,
    lisparb=""
   
    pkUser=request.user.pk
  
    if request.method=='GET':
        #print('es geeeeeeeeetttttttttttttt')
        #Formulario creado en forms.py
        form_buscar=BuscarParticipanteForm()
        
        lisEventos = lista_Eventos_Por_Acceso(pkUser,request.user.is_staff,"O")
        
        
       

 
      
        #crea objeto vacio
        lispar=""
       
        
        #En el contexto definimos que mandamos a la plantilla
        
        contexto={'eve':form_buscar,'lispar':lispar, 'liseventos':lisEventos}
        # la impresion de contexto ejecutara consulta a la BD
        #print(contexto)
        return render(request, template_name,contexto )    
        
    if request.method=='POST':    
        #print('es pooooooooooossssttt')
        
        apellido_participante = request.POST.get("apellido_participante")
        nombre_participante = request.POST.get("nombre_participante")
        empresa_participante = request.POST.get("empresa_participante")
        evento = request.POST.get("evento")
        #print(apellido_participante)    
        #print(nombre_participante)    
        #print("empresa")
        #print(empresa_participante)
        #print(evento)  
        if (evento=='0'):
            #print('Seleccione Evento') 
            contexto={'rpta':'OFF',
                  'lispar':'',
                  'mensaje':'Seleccione Evento'}  
        else:    
        
            if (len(empresa_participante)==0):  
                
                if (len(apellido_participante) == 0 and len(nombre_participante) == 0):    
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento)).values("id",
                    "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                    #print('busqueda solo por evento')
                else:    
                    if (len(apellido_participante) > 0 and len(nombre_participante) > 0):    
                        
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__icontains=apellido_participante) & Q(nombre_participante__icontains=nombre_participante)).
                        values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                        #print('busqueda por apellido y nombre : caso empresa vacio')
                    else:
                        if (nombre_participante == ""):
                            lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__icontains=apellido_participante)).
                            values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                            "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                            #print('busqueda por apellido :  empresa vacio')
                        else:    
                            lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(nombre_participante__icontains=nombre_participante)).
                            values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                            "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                            #print('busqueda por nombre caso empresa vacia')
                
            else:
                if (len(apellido_participante) > 0 and len(nombre_participante) > 0):    
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__icontains=empresa_participante) & Q(apellido_participante__icontains=apellido_participante) & Q(nombre_participante__icontains=nombre_participante)).
                    values("id","evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                    #print('busqueda por empresa, apellido y nombre : caso 4')
                else:    
                    if (nombre_participante == ""):
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__icontains=empresa_participante) & Q(apellido_participante__icontains=apellido_participante)).values("id",
                        "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                        #print('busqueda por empresa y apellid : caso 5')
                    else:    
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__icontains=empresa_participante) & Q(nombre_participante__icontains=nombre_participante)).values("id",
                        "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante","tipo_participante__tipo_identificacion_participante"))
                        #print('caso empresa y nombre')
                
                        
            #print('json es') 
            contexto={'rpta':'OK',
                  'lispar':lispar}            
        #print(contexto)                    
    return JsonResponse(contexto)
        
    return render(request, template_name, contexto)    



#@login_required(login_url="/login/")
#@permission_required("cmp.change_proveedor",login_url="bases:sin_privilegios")
#def proveedorInactivar(request,id):



@login_required(login_url='config:login')
@permission_required('par.change_participante', login_url='bases:sin_privilegios')
#@permission_required('par.edit_participante', login_url='config:home')
#@permission_required('par.edit_participante', raise_exception=True)
def participanteAsistencia(request, id):
     
    #print("a001")
    try:
        permission_required = 'par.change_participante'
        #print("a002")
        idPar=request.POST.get("id")
        tipo=request.POST.get("tipo")
        anulAsis=request.POST.get("anularAsistencia")
        evento=request.POST.get("evento")
        anulAsis=anulAsis.upper()
        swparamValido="NO"
        nomEve=""
        medLec=""
        if(tipo=='A' or tipo=='QA'):
           #print("a003")
           qrAsignado=request.POST.get("qrAsignado") 
           participante = Participante.objects.filter(pk=id).first()
           swparamValido="SI"
        else:
            #print("a004")
            if(tipo=="Q"):
               #print("a005") 
               #evento=request.POST.get("evento")
               codigo_qr=request.POST.get("id")
               nomEve=request.POST.get("nomEve")
               medLec=request.POST.get("medLec")
               #participante = Participante.objects.filter(evento=evento,codigo_qr=id).first()
               participante = Participante.objects.filter(evento_id=evento).filter(codigo_qr=id).first()
               
               #participante=Participante.objects.get(evento_id=evento,codigo_qr=id)
               ##participante = Participante.objects.get(evento=evento).get(codigo_qr=codigo_qr)
               swparamValido="SI"
                   
        
        if(swparamValido=="NO"):
          #print("a006")
          contexto={'rpta':'OFF',
                    'mensaje':'Parametros no validos'}          
        else:
            #print("a007") 
            if request.method=="POST":
                #print("a008")
                swOk="NO"
                if participante:
                   #print("a009") 
                    if participante.asistio_evento:
                       #print("a010")
                        if (tipo=="A" and anulAsis=="TRUE"):
                            swOk="SI"
                            #print("a011")
                        else:    
                            if (tipo=="A"):
                                msj="Participante ya esta registrado, refresque listado"
                                #print("a012")
                            else:
                                #print("a013")
                                msj="Código ya esta registrado :"+id    
                            
                            contexto={
                                    'rpta':"OFF",
                                    'mensaje':msj,
                                    'nomEve':nomEve,
                                    'medLec':medLec
                                }
                    else: 
                        # Si se asigna QR a participante
                        #print("a014")
                        if (tipo=="QA"):
                            if (participante.codigo_qr==None or participante.codigo_qr==""):
                                swOk="SI"
                               #print("a015")
                            else:
                                #print("a016")
                                contexto={
                                'rpta':"OFF",
                                'mensaje':"Ya tiene código registrado "+participante.codigo_qr,
                                'nomEve':nomEve,
                                'medLec':medLec
                                }           
                        else:
                            #print("a017")             
                            swOk="SI"
                                      
                    if swOk=="SI":
                        #print("a018")
                        if (tipo=="QA"):
                            #print("a019")
                            # Verifica que código QR no exista
                            #print(evento)
                            #print(qrAsignado)
                            #qrExiste=Participante.objects.filter(Q(evento_id=evento) & Q(codigo_qr=qrAsignado))
                            qrExiste=Participante.objects.filter(evento_id=evento).filter(codigo_qr=qrAsignado).values("apellido_participante","nombre_participante")
                            #.first()
                          
                            #print(qrExiste)
                          
                            if qrExiste: 
                                for duplicado in qrExiste:
                                   
                                   grabaAsistencia=False
                                   contexto={
                                    'rpta':"OFF",
                                    'mensaje':"Código :" + qrAsignado + " ya esta asignado a "+duplicado['nombre_participante'] + " "+duplicado['apellido_participante'],
                                    'nomEve':nomEve,
                                    'medLec':medLec
                                    }
                            else:
                                grabaAsistencia=True
                                participante.codigo_qr=qrAsignado
                                participante.asistio_evento = not participante.asistio_evento
                        else:    
                            #print("a020")
                            grabaAsistencia=True
                            participante.asistio_evento = not participante.asistio_evento
                        #print("a021")
                        if grabaAsistencia:
                            participante.save()
                            tipo_participante=participante.tipo_participante.descripcion_tipo_participante
                            tipo_identificacion_participante=participante.tipo_participante.tipo_identificacion_participante
                            modalidad_asistencia=participante.modalidad_asistencia.descripcion_modalidad_asistencia
                            if (tipo=="A" or tipo=="QA"):
                                #print("a022")    
                                contexto={"id": participante.id,
                                        'asistio_evento':participante.asistio_evento,
                                        "apellido_participante" : participante.apellido_participante,
                                        "nombre_participante" : participante.nombre_participante,
                                        "email_participante" : participante.email_participante, 
                                        "empresa_participante": participante.empresa_participante, 
                                        "modalidad_asistencia": participante.modalidad_asistencia.descripcion_modalidad_asistencia,
                                        "tipo_participante": tipo_participante,
                                        "tipo_identificacion_participante": tipo_identificacion_participante,
                                        "rpta":'OK'}                                           
                            else:
                                #print("a023")  
                                contexto={"rpta":"OK",
                                        "mensaje":"Bienvenido",
                                        'nomEve':nomEve,
                                        'medLec':medLec    
                                        }      
                                            
                else:
                   
                    #participante=Participante.objects.create(id=id,evento_id=evento)
                    #print("a024")
                    participante=None
                    contexto={
                                'rpta':"OFF",
                                'mensaje':"Código No existe "+id,
                                'nomEve':nomEve,
                                'medLec':medLec
                        }
                
            else:
                #print("a025")
                contexto={'rpta':"OFF",
                        'mensaje':"Metodo de solicitud no valido",
                        'nomEve':nomEve,
                        'medLec':medLec
                        }
            if tipo=="A" or tipo=="QA":
                #print("a026")
                return JsonResponse(contexto,safe=False)
            else:
                #print("a027")
                #print(contexto)
                #print("para todod")
                return render(request, 'par/lectura_qr_resultado.html',{'conDic':contexto,'obj':participante})    
                    
  
        return JsonResponse(contexto,safe=False)      
        #return JsonResponse(contexto)     
    except ValueError as e:  
        mensaje=str(e)
      
        #print("try 1")
        mensaje=mensaje.replace('"','')
        mensaje=mensaje.replace("'","\\'")
        rptaServer="OFF"
        contexto={'rpta':'OFF',
                  'mensaje':mensaje}      
        return JsonResponse(contexto,safe=False)  
        
    except ObjectDoesNotExist as e:
        #print("try 2")
        if tipo=="A":
            contexto={'rpta':'OFF',
                            'mensaje':'No existe código participante '+id
                    }
            return JsonResponse(contexto,safe=False)  
        else: 
            contexto={
                    'rpta':"ERR",
                    'mensaje':"No existe código participante: "+id,
                    'nomEve':nomEve
                    }
            return render(request, 'par/lectura_qr_resultado.html',{'conDic':contexto,'obj':''})
    except IntegrityError as e:
        #print("try 3")
        if tipo=="A" or tipo=="QA":
            contexto={'rpta':'OFF',
                            'mensaje':'Error de integridad de datos '
                    }
            return JsonResponse(contexto,safe=False)  
        else: 
            contexto={
                    'rpta':"ERR",
                    'mensaje':"Error de integridad de datos  "+id,
                    'nomEve':nomEve
                    }
            return render(request, 'par/lectura_qr_resultado.html',{'conDic':contexto,'obj':''})
        
        
    #return render_to_response("template.html", {"message": e.message})
                        
                                
           

          
        
        
     




#class ParticipanteEdit(SuccessMessageMixin, MixinFormInvalid, SinPrivilegios,\
#                   generic.UpdateView):

class ParticipanteEdit(SuccessMessageMixin, SinPrivilegios,generic.UpdateView):        
    permission_required="par.change_participante"
    model=Participante
    template_name="par/participante_form.html"
    context_object_name = 'obj'
    form_class=ParticipanteForm
    success_url= reverse_lazy("par:buscar_participante")
    success_message="Participante Editado"
    #permission_required="cmp.change_proveedor"
    
    def get_context_data(self, **kwargs):
        context = super(ParticipanteEdit, self).get_context_data(**kwargs)
        context["eventos"] = Evento.objects.all()
        context["tipos"] = Tipo_Participante.objects.all()
        context["modalidades"] = Modalidad_Asistencia.objects.all()
       
        #print(context)  
       
        return context    
       
        
    def form_valid(self, form):
       # form.instance.
       #print(form.instance.id)
       #print(form.instance.apellido_participante)
        
       #print("es valido")
       #print("no es valido")    
       #print(form.instance.apellido_participante)
        
         
        
        try: 
            
          
            if (form.is_valid()):
                   
                status_code = 200
                form.instance.um = self.request.user   
                #print(form.instance.id)
                #print(form.instance.apellido_participante)
                form.save()                 
                
                ##return super().form_valid(form)                        
                
                contexto={'mensaje':"Datos actualizados",
                         'error':'',
                         'rptaServer':"OK"}  

                #print("grabo edit ")
                response = JsonResponse(contexto)
                response.status_code = status_code
            else:
              
                status_code = 400
                error= form.errors 
               #print("form.errors")
               #print(form.errors.as_data())
               #print("solo error")
               #print(error)
                contexto={'mensaje':"Verifique Datos",
                        'error':error,
                        'rptaServer':'OFF'} 
                response = JsonResponse(contexto)
                response.status_code = status_code
                
                
            #print("debe de regresar de edit")  
            #print(contexto)
            #print(response)
            return response

        except ValueError as e:
            
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':'mensaje',
                            'error':'',
                            'rptaServer':'OFF'}  
            #print ('mensaje except')
            #print (contexto)
            response = JsonResponse(contexto)
            #print(response)
            return response
         
    

    def post(self, request, *args, **kwargs):
        #print("post edi")
        #print(request.POST.get("apellido_participante"))
        #print(request.POST.get("id"))
                     
        busca=request.POST.get("id")
        requestValido="OK"
        response=""
        
        #form = self.form_class(request.POST)
        #form = ParticipanteForm(request.POST)
        form = self.form_class(request.POST)
        participante = Participante.objects.filter(pk=request.POST.get("id")).first()
        
        
        #participante=Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(pk=busca)).values("id",
        #           "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
        #           "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante")
        
        

            
        try: 
          
            if (form.is_valid()):
              
                if participante:
                  
                
                    participante.apellido_participante = form.instance.apellido_participante
                    participante.nombre_participante = form.instance.nombre_participante
                    participante.empresa_participante = form.instance.empresa_participante
                    participante.email_participante = form.instance.email_participante
                    participante.telefono_participante = form.instance.telefono_participante
                    participante.observaciones_participante = form.instance.observaciones_participante
                    participante.acompanante_de = form.instance.acompanante_de
                    participante.cargo_participante = form.instance.cargo_participante
                    participante.asistio_evento = form.instance.asistio_evento
                    participante.confirmo_asistencia = form.instance.confirmo_asistencia
                    participante.tipo_participante  = form.instance.tipo_participante
                    participante.modalidad_asistencia = form.instance.modalidad_asistencia
                    #participante.codigo_qr = form.instance.codigo_qr
                    participante.uc = self.request.user   
                    
                    #print("form.instance,id")
                    #print(participante.id)
                    
                    #print(to_dict(participante))
                 
                    
                    participante.save()
                    
                    tipo_par= Tipo_Participante.objects.filter(pk=request.POST.get("tipo_participante")).first()
                    moda_asi= Modalidad_Asistencia.objects.filter(pk=request.POST.get("modalidad_asistencia")).first()
                    data = {
                           "id": participante.id,
                           "asistio_evento": participante.asistio_evento,
                           "tipo_participante" : tipo_par.descripcion_tipo_participante,
                           "background_tipo_participante" : tipo_par.background_tipo_participante,
                            "apellido_participante" : participante.apellido_participante,
                           "nombre_participante" : participante.nombre_participante,
                           "email_participante" : participante.email_participante, 
                           "empresa_participante": participante.empresa_participante, 
                           "modalidad_asistencia": moda_asi.descripcion_modalidad_asistencia, 
                           "tipo_participante": tipo_par.descripcion_tipo_participante,
                           "tipo_identificacion_participante": tipo_par.tipo_identificacion_participante,
                           "rpta":"OK"
                           }


                    
                    contexto={'mensaje':"Datos actualizados EDIT",
                                'error':'',
                                'rptaServer':"OK",
                               'participante' : data}  
                    status_code = 200
                    #print("grabo ")
                    response = JsonResponse(contexto)
                    response.status_code = status_code
                else:
                  
                    contexto={'mensaje':"Participante no Existe",
                                'error':'',
                                'rptaServer':"OFF"}  
                    status_code = 200
                    #print("grabo")
                    response = JsonResponse(contexto)
                    response.status_code = status_code
                    
                    
                        
            else:
               #print(form.errors.as_data())
              
                status_code = 400
                error= form.errors 
               #print(form.errors.as_json(escape_html=True))
                #print("form.errors 491")
               #print(form.errors.as_data())
               #print("solo error")
             
                contexto={'mensaje':"Verifique Datos",
                        'error':error,
                        'rptaServer':'OFF'} 
                response = JsonResponse(contexto)
                response.status_code = status_code
                
                
            #print("debe de regresar 465")  
            #print(contexto)
            #print(response)
            return response

        except ValueError as e:
         
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':'mensaje',
                            'error':'',
                            'rptaServer':'OFF'}  
            #print ('mensaje except')
            #print (contexto)
            response = JsonResponse(contexto)
            #print(response)
            return response
            
        
            
        return redirect('par:buscar_participante')

           
     
    



#SuccessMessageMixin, = necesario para enviar mensajes
#class ParticipanteAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
class ParticipanteAdd_xx(SuccessMessageMixin,generic.CreateView):    
    #permission_required = 'eve.add_modalidad_evento'
    model = Participante
    #template_name="par/participante_add.html"    
    template_name="par/participante_form.html"    
    context_object_name = "obj"
    form_class = ParticipanteForm
    success_url = reverse_lazy("par:buscar_participante")
    #login_url ="bases:login"
    success_message="Participante registrado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user   
        form.save()     
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(ParticipanteAdd, self).get_context_data(**kwargs)
        context["eventos"] = Evento.objects.all()
        context["tipos"] = Tipo_Participante.objects.all()
        context["modalidades"] = Modalidad_Asistencia.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        requestValido="OK"
        response=""
        
        form = self.form_class(request.POST)
        try: 
            if (form.is_valid() | (not form.is_valid())):
             #   mensaje=f'{self.model.nombre_participante} datos correctos'
            #else:
                #mensaje=f'{self.model._modalidad_asistencia_} no se ha podido registrar'
                #print("salvaod https://www.youtube.com/watch?v=JpPUX9GIFL8")
                evento=form.cleaned_data.get("evento")
                email_participante=form.cleaned_data.get("email_participante")
                modalidad_asistencia=form.cleaned_data.get("modalidad_asistencia")
                tipo_participante=form.cleaned_data.get("tipo_participante")
                mensaje='Verifique ingrese de datos'
                if(not evento):
                    mensaje=f'Error verifique'
                   # form.add_error("evento","seleccione evento")
                    form.add_error("evento", ValidationError(_("Evento no valido")))
                    
                    requestValido="OFF"
                    
                if (not email_participante):
                   raise ValueError(_("El correo es un campo obligatorio."))
                    
                        
                if(not modalidad_asistencia):
                    mensaje=f'Error verifique'
                    #form.add_error("modalidad_asistencia","seleccione modalidad de asistencia")

                    #errors = form._errors.setdefault("modalidad_asistencia", ErrorList())
                    #errors.append(u"Seleccione modalidad de asistencia")
                    requestValido="OFF"
                if(not tipo_participante):
                    mensaje=f'Error verifique'
                    #form.add_error("tipo_participante","seleccione tipo de participante")  
                    requestValido="OFF"
                        
                error= form.errors 
                # error= form.errors.as_data()
                #print(form.errors.as_data())
                contexto={'mensaje':mensaje,
                        'error':error,
                        'rptaServer':'OFF'}  

                            #response = JsonResponse({'mensaje':mensaje, 'error':error})
                status_code = 400    
                if(requestValido=="OK"):
                    mensaje="Datos actualizados"
                    contexto={'mensaje':mensaje,
                            'error':'',
                            'rptaServer':"OK"}  
                    status_code = 200
                    
                    form.instance.uc = self.request.user   
                    form.save() 
                else:    
                    status_code = 400
                            
                        
                response = JsonResponse(contexto)
                response.status_code = status_code
                #print(contexto)
                #print(response)
            return response

        except ValueError as e:
            
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':mensaje,
                            'error':'',
                            'rptaServer':'OFF'}  
            #print ('mensaje except')
            #print (contexto)
            response = JsonResponse(contexto)
            #print(response)
            return response
            
        
            
        return redirect('par:buscar_participante')


class ParticipanteAdd(SuccessMessageMixin, SinPrivilegiosAjax, generic.CreateView):    
    permission_required = 'par.add_participante'
    model = Participante
    #template_name="par/participante_add.html"    
    template_name="par/participante_form.html"    
    context_object_name = "obj"
    form_class = ParticipanteForm
    success_url = reverse_lazy("par:buscar_participante")
    #login_url ="bases:login"
    success_message="Participante registrado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    #def __init__(self, request, evento=None):
    #    print("sss")
    #    self.evento= evento
    
   # def get_success_url(self):
    #   #return reverse('participante_new', args = [self.object.evento.id])
     #  return reverse('participante_new', kwargs={'evento_id':1})
    
   
    
   ## def form_valid(self, form):
        # Obtén la ID del libro desde los argumentos de la URL
    ##    evento_id = self.kwargs['evento_id']
    ##    print("ingesoooo")
        # Asigna el libro correspondiente a la instancia
      ##  form.instance.evento= Evento.objects.get(evento_id=evento_id)
        ##return super().form_valid(form)
    
    
   # def get_absolute_url(self):
   #     return reverse('participante_new', kwargs={'evento_id': self.evento.evento_id})
        
    def form_valid(self, form):
       #print("es valido")
       #print("no es valido")    
        form.instance.uc = self.request.user   
        form.save()     
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
       #print("self.tipo_participante_id")
        evento_id = self.kwargs['evento_id']
        # print("ingesoooo context_Data")
        # print(evento_id)
       
        context = super(ParticipanteAdd, self).get_context_data(**kwargs)
        #context["eventos"] = Evento.objects.all()
        eventos=lista_Eventos_Por_Acceso(self.request.user.id,self.request.user.is_staff,"O")
        param=eventos.filter(id=evento_id).first()
        context["eventos"]=eventos
        context["tipos"] = Tipo_Participante.objects.all()
        context["modalidades"] = Modalidad_Asistencia.objects.all()
        context["eventoId"] = evento_id
        context["nuevoTipo"] = param.nuevo_tipo_participante
        
      
        
     
        '''
        testprodms = TestPROD.objects.order_by().values_list('prodID', flat=True).distinct()
        AllProdcts = TestPROD.objects.all()
        listtests  =  [AllProdcts.filter(prodID__exact=prodtest).first() for prodtest in testprodms]        listtests  =  [eventos.filter(id=evento_id).first()
        '''
       #print(context)
        
        
        return context
    
    def post(self, request, *args, **kwargs):
        #self.request = kwargs.pop("request")
        #self.fields["evento"]=456
        #print("post views 978")
        requestValido="OK"
        response=""
       
        idEvento=request.POST.get("evento")
        #print(idEvento)
        #print(idEvento)
        idEvento=idEvento.replace('*', '')
        
        ww=request.POST.get("evento",idEvento)
        #print(ww)
        form = self.form_class(request.POST)
        #form.instance.evento=idEvento
        try: 
            if (form.is_valid()):
                
                form.instance.uc = self.request.user   
                form.save() 
               
                contexto={'mensaje':"Participante agregado",
                            'error':'',
                            'rptaServer':"OK"}  
                status_code = 200
                
                response = JsonResponse(contexto)
                response.status_code = status_code
            else:
                status_code = 400
                error= form.errors 
                #print("no graba")
                #print(form.errors.as_data())
               #print("solo error")
                #print(error)
                contexto={'mensaje':"Verifique Datos",
                        'error':error,
                        'rptaServer':'OFF'} 
                response = JsonResponse(contexto)
                response.status_code = status_code
                
                
            #print("debe de regresar 645")  
            #print(contexto)
            #print(response)
            return response

        except ValueError as e:
            
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':'mensaje',
                            'error':'',
                            'rptaServer':'OFF'}  
            #print ('mensaje except')
            #print (contexto)
            response = JsonResponse(contexto)
            #print(response)
            return response
            
        
            
        return redirect('par:buscar_participante')



def DetailForm(request):
    if request.method == "POST":  
        form = CreateForm(request.POST)
       
        #if form.is_valid():
            #print('First Name:', form.cleaned_data['apellido_participante'])
            #print('Last Name:', form.cleaned_data['nombre_participante'])
            #print('Email:', form.cleaned_data['Email'])
   
    return redirect('par/participante_form.html')



def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data





#@login_required(login_url='config:login')
#@permission_required('par.view_participante', login_url='config:home')
def xx_ImportarCsv(request,participante_id=None):
   # permission_required = 'par.view_participante'

    template_name="par/participante_import_add.html"
    form_compras={}
    contexto={}
    par_evento_id=0
    nombre=''
    apellido =''
    evento=0,
    lisparb=""
    
   
    if request.method=='GET':
       
        #Formulario creado en forms.py
        #form_buscar=BuscarParticipanteForm()
        #lisEventos = Evento.objects.all()
        lisEventos = lista_Eventos_Por_Acceso(request.user.pk,request.user.is_staff,"O")

        #lispar=Participante.objects.filter(Q(evento_id=par_evento_id))
        
        #En el contexto definimos que mandamos a la plantilla
        contexto={'liseventos':lisEventos}
       
        return render(request, template_name, contexto)    
        
    if request.method=='POST':
        
        msg=""
       
        #print(request.FILES['csv_file'].name)
        
        if  (request.POST.get("evento")== None or request.POST.get("evento")=='' or request.POST.get("evento")=='0'):
           msg+='Seleccione evento'
        
        #if (request.FILES['csv_file'].name==''):
        #    msg+="Seleccione archivo csv"
       
    
        
        
        
        if(msg==""):        
            csv_file = request.FILES['csv_file']
            evento = request.POST.get("evento")
            csv_nombre =  request.FILES['csv_file'].name 
            
            #print("impor 1")
            mensaje=valida_csv(request)  
            #print("impor 2")
            if (mensaje["rptaServer"]=='OK'):
            #if ('OK'=='OK'):
                #print("impor 3")
                mensaje=subir_csv(mensaje['dataValidado'],csv_file,evento,csv_nombre)
                '''
                if (mensaje["rptaServer"]=='OK'):
                    #print('es pooooooooooossssttt cargo csv')
                    evento = request.POST.get("evento")
                    #print(evento)  
            
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento)).values("id",
                    "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
                    #print('busqueda solo por evento')
                '''
        else:
            mensaje={
                'rptaServer':'OFF',
                'errorData':'',
                'mensaje':msg
                }        
                           
        response = JsonResponse(mensaje)
        #print(response)
        return response
    
    


def ListarCsv(request,participante_id=None):
   # permission_required = 'par.view_participante'

    template_name="par/participante_import_delete.html"
    form_compras={}
    contexto={}
    par_evento_id=0
    nombre=''
    apellido =''
    evento=0,
    lisparb=""
    
    #print('eduuuuuuuuuuuuuu')
    if request.method=='GET':
        #print('es geeeeeeeeetttttttttttttt')
        #Formulario creado en forms.py
        #form_buscar=BuscarParticipanteForm()
        #lisEventos = Evento.objects.all()
        lisEventos = lista_Eventos_Por_Acceso(request.user.pk,request.user.is_staff,"O")

        #lispar=Participante.objects.filter(Q(evento_id=par_evento_id))
        
        #En el contexto definimos que mandamos a la plantilla
        contexto={'liseventos':lisEventos}
        #print(contexto)
        return render(request, template_name, contexto)    
        
    if request.method=='POST':
        
        msg=""
       
        #print(request.FILES['csv_file'].name)
        
        if  (request.POST.get("evento")== None or request.POST.get("evento")=='' or request.POST.get("evento")=='0'):
           msg+='Seleccione evento'
        
      
        
        
        if(msg==""):        
                   
            evento = request.POST.get("evento")
            #print(evento)  
            
           
            liscsv=lista_participante_csv(evento)
            #print('busqueda solo por evento')
            
            
            contexto={
            'rptaServer':'OK',
            'liscsv': liscsv,
            'mensaje':'Listado de archivos importados'
            }
               
        else:
            contexto={
                'rptaServer':'OFF',
                'liscsv':'',
                'mensaje':msg
                }        
                           
        response = JsonResponse(contexto)
       #print(response)
       #print(liscsv)
        return response
        
    


class VistaParticipanteImportar(ListView):
    template_name="par/participante_import_add.html"
    model = Participante
    context_object_name="obj"
    
 

       
class ParticipanteCsvAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    #permission_required = 'par.add_tipo_participante'
    model = Participante_Csv
    template_name="par/tipo_participante_add.html"    
    context_object_name = "obj"
    form_class = Participante_Csv
    success_url = reverse_lazy("par:tipo_participante_list")
    #login_url ="bases:login"
    success_message="Nombre archivo creado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user        
        return super().form_valid(form)    



def valida_csv(request):
#    template_name = "par/subir_csv.html"
    swCabecera=""
    swCabeceraVeri=""
   
    errorData = list()
    if request.method =="POST":
        csv_file = request.FILES['csv_file']
        evento = request.POST.get("evento")
        
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        msg=""
        fila=0
        swError=""
        lines = file_data.split("\n")
        dataValidado=list()
        for line in lines:
            fields = line.split(",")
            fila=fila+1
            if len(fields)>1:
                if (fila==1):
                    swCabecera=valida_cabecera_csv(fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],fields[8])
                    #print("validador cabecera :"+swCabecera)
                    if not(swCabecera=="OK"):
                        swError="SI"
                        msg="Verificar cabera de archivo"
                        break
                if (swCabecera=="OK" and fila>1):
                    try:
                        swErrorReg="0"
                        msgValid=""
                        swMail=(validar_email_personalizado(fields[2]))
                        swApellido=validar_solo_caracteres(fields[0].strip())
                        swNombre=validar_solo_caracteres(fields[1].strip())
                        if not(swMail+swApellido+swNombre=='OKOKOK'):    
                            #errorData.append({'fila':fila,'apellido':swApellido,'nombre':swNombre,'email':swMail})
                            msg="Datos tiene caracteres no validos"
                            swError="SI"
                            swErrorReg="1" 
                        
                        data_dict = {}
                        data_dict["evento"]=evento
                        #evento
                        data_dict["apellido_participante"]=fields[0]                
                        data_dict["nombre_participante"]=fields[1]                
                        data_dict["email_participante"]=fields[2]
                        data_dict["empresa_participante"]=fields[3]
                        data_dict["cargo_participante"]=fields[4]
                        data_dict["modalidad_asistencia"]=fields[5]
                        data_dict["tipo_participante"]=fields[6]
                        confirmo = fields[7]
                        
                        confirmo = confirmo.strip()
                        confirmo = confirmo.lower()
                        if (confirmo == "si"):
                             data_dict["confirmo_asistencia"]=True
                            
                        else:    
                             data_dict["confirmo_asistencia"]=False
                            
                             
                        data_dict["codigo_qr"]=fields[8]
                        
                        #form = ParticipanteFormImportacion(data_dict)
                        #print("aquiiiiiiiiiiiiiiiiiiiiii esta")
                        form = ParticipanteFormImportacionSinQr(data_dict)
                       
                        if not(form.is_valid()):                            
                            #print("error en valida_csv")
                            #print(fields[5])
                            swError="SI"
                            swErrorReg="1"
                            msg+=" Error de integridad de datos"
                            
                            for key in form.errors.items():
                                #print(key ,"->")
                                dato=str(key)
                                ini=dato.index('[')+1
                                fin=dato.index(']')
                                #print(dato[ini:fin],' kkkkk ')
                                msgValid +=(dato[ini:fin])+"; "
                                msgValid = re.sub(r"[^a-zA-Z0-9-!?¡¿;óéíáú-]", " ", msgValid)
                                
                        if (swErrorReg=='1'):
                            errorData.append({'fila':fila,'apellido':swApellido ,'nombre':swNombre,'email':swMail,'is_valid':msgValid})
                                
                           
                        else:
                            dataValidado.append({'evento':data_dict["evento"],\
                                'apellido_participante':data_dict["apellido_participante"],\
                                'nombre_participante':data_dict["nombre_participante"],\
                                'email_participante':data_dict["email_participante"],\
                                'empresa_participante':data_dict["empresa_participante"],\
                                'cargo_participante':data_dict["cargo_participante"],\
                                'modalidad_asistencia':data_dict["modalidad_asistencia"],\
                                'tipo_participante':data_dict["tipo_participante"],\
                                'confirmo_asistencia':data_dict["confirmo_asistencia"],\
                                'codigo_qr':data_dict["codigo_qr"]
                                })
                            #dataValidado.update(data_dict)   
                        
                                        
                    except Exception as ex:
                      
                        #print(repr(ex))
                        swError="SI"
                        msg=repr(ex)
        if(swError=="SI"):
            contexto={
                'rptaServer':'OFF',
                'errorData': errorData,
                'mensaje':msg
                }
        else: 
            contexto={
                'rptaServer':'OK',
                'errorData': '',
                'mensaje':'Cabecera y datos verificados',
                'dataValidado':dataValidado
                }    
       
      ##  return redirect("par:participante_import_add")           
    else:
        contexto={
            'rptaServer':'OFF',
            'errorData': '',
            'mensaje':'Opción no es enviada desde aplicativo'
                    }
       
    return contexto


@transaction.atomic 
def subir_csv(lista,archivo,evento,nombre_csv):
    fila=0
    nsave=0
    msg=""   
    mensaje=""
   
    #archivo_csv = Participante_Csv.objects.filter(id=0).first()
    data_csv={}
    
    data_csv["evento"]=evento
    data_csv["archivo_csv"]=nombre_csv
    data_csv["cantidad"]=len(lista)
   # archivo_csv.archivo_csv=archivo
   # archivo_csv.evento=evento
    farchivo_csv = ParticipanteCsvForm(data_csv)
    #farchivo_csv = Participante_Csv.objects.filter(id=15).first()
    #farchivo_csv = Participante_Csv()
    #print(farchivo_csv)
    
    #print(data_csv)
    
    nuevoId=farchivo_csv.save()
    
    id_csv=nuevoId.id
    #id_csv=farchivo_csv.par_participante_csv.id
    #id_csv=farchivo_csv.id
    
    #print(id_csv)
    sid = transaction.savepoint()
    nuevoId=farchivo_csv.save()
    id_csv=nuevoId.id
    try:
       
        for imp in lista:
                fila=fila+1
                data_dict = {}
                data_dict["evento"]=imp['evento']
                data_dict["apellido_participante"]=imp['apellido_participante']                
                data_dict["nombre_participante"]=imp['nombre_participante']                
                data_dict["email_participante"]=imp['email_participante']
                data_dict["empresa_participante"]=imp['empresa_participante']
                data_dict["cargo_participante"]=imp['cargo_participante']
                data_dict["modalidad_asistencia"]=imp['modalidad_asistencia']
                data_dict["tipo_participante"]=imp['tipo_participante']
                data_dict["confirmo_asistencia"]=imp['confirmo_asistencia']
                
                data_dict["participante_csv"]=id_csv
                data_dict["codigo_qr"]=imp['codigo_qr']
               
                #form = ParticipanteFormImportacion(data_dict)
                form = ParticipanteFormImportacionSinQr(data_dict)
                #print("esta en subir_csv")            
                if form.is_valid():
                    form.save()
                    nsave=nsave+1 
                    
                else:
                    msg="OFF"
    except IntegrityError:
        transaction.savepoint_rollback(sid)
   

    if not (fila==nsave):    
        transaction.savepoint_rollback(sid)
        msg="OFF"
        mensaje="Error al grabar datos, importanción cancelado (rollback)"
       
    else:
        mensaje='Se importo '+str(nsave)+' de '+str(fila) + ' registros'
        msg="OK"
            
    contexto={
            'rptaServer':msg,
            'errorData': '',
            'mensaje':mensaje
            }
    return contexto        
                
                                                  
                     
def subir_csv_req(request):
#    template_name = "par/subir_csv.html"
    swCabecera=""
    swCabeceraVeri=""
    errorData = list()
    if request.method =="POST":
        csv_file = request.FILES['csv_file']
        evento = request.POST.get("evento")
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        msg=""
        nsave=0
        msg="Error en datos"
        fila=0
        swError=""
        lines = file_data.split("\n")
        for line in lines:
            fields = line.split(",")
            fila=fila+1
           
            if len(fields)>1:
                if (fila>1):
                    try:
                         
                        #print('verifican '+str(fila))    
                        data_dict = {}
                        data_dict["evento"]=evento
                        #evento
                        data_dict["apellido_participante"]=fields[0]                
                        data_dict["nombre_participante"]=fields[1]                
                        data_dict["email_participante"]=fields[2]
                        data_dict["empresa_participante"]=fields[3]
                        data_dict["cargo_participante"]=fields[4]
                        data_dict["modalidad_asistencia"]=fields[5]
                        data_dict["tipo_participante"]=fields[6]
                        confirmo = fields[7]
                        confirmo = confirmo.strip()
                        confirmo = confirmo.lower()
                        if (confirmo == "si"):
                             data_dict["confirmo_asistencia"]=True
                             #print("campos verdad")
                        else:    
                             data_dict["confirmo_asistencia"]=False
                             #print("campos falso")
                        form = ParticipanteForm(data_dict)
                       
                        if form.is_valid():
                            form.save()
                            nsave=nsave+1                                        
                        else:
                           
                            #print("muestra los mensajes de error")
                            #print(form.errors)
                            #print(form.errors.items())
                            #print("muestra los mensajes de error")
                            swError="SI"
                            msg=""
                            for key in form.errors.items():
                                #print(key ,"->")
                                dato=str(key)
                                ini=dato.index('[')+1
                                fin=dato.index(']')
                                #print(dato[ini:fin],' kkkkk ')
                                msg =(dato[ini:fin])
                                msg = re.sub(r"[^a-zA-Z0-9-!?¡¿-]", " ", msg)
                                errorData.append({'fila':fila,'apellido':fields[0] ,'nombre':fields[1],'email':fields[2],'is_valid':msg})
                                
                            msg="Error de integridad de datos"    
                            #msg=form.errors 
                            #print(msg)
                            #for key,value in form.errors.items():
                              #print(value, 'zzzzzzzzzz')
                                #forms[key]=BeautifulSoup(value,'html.parser').get_text()
                            
                                
                            #for key in form.errors:
                            #print(key, " xxx")
                                
                            
                            #for item in form.errors.as_data().items():
                             #print(fields[item[0]])
                             
                                   
                            #for item in self.errors.as_data().items():
                            #   if item[0] in self.fields:
                            #   self.fields[item[0]].widget.attrs['class'] = 'input is-danger'
        
                           
                    #except Exception as ex:
                    except Exception as msg_error:
                                #print(f"¡Lo siento, {msg_error} !")    
                        
                                msg=(f"¡Lo siento, {msg_error}!")
                              
                                msg = re.sub(r"[^a-zA-Z0-9-!?¡¿-]", " ", msg)

                                errorData.append({'fila':fila,'apellido':fields[0] ,'nombre':fields[1],'email':fields[2],'is_valid':msg})
                                swError="EXCEPTION"
                                break
            
        
        if(swError=="EXCEPTION"):
            contexto={
                'rptaServer':'OFF',
                'errorData': '',
                'mensaje': msg
                    }
            #print(contexto)
        else:    
            if(swError=="SI"):
                #print('caso edu 1')
                contexto={
                    'rptaServer':'OFF',
                    'errorData': errorData,
                    'mensaje': msg
                        }
            else: 
                #print('caso edu 2')              
                contexto={
                    'rptaServer':'OK',
                    'errorData': '',
                    'mensaje':'Se importo '+str(nsave)+' de '+str(fila-2) + ' registros'
                        }
               
    else:
        #print('caso edu 3')
        contexto={
            'rptaServer':'OFF',
            'errorData': '',
            'mensaje':'Opción no es enviada desde aplicativo'
                    }
       
    #print(contexto)  
    #print("eeee")  
    return contexto
 







@login_required(login_url='config:login')
@permission_required('bases.change_usuario', login_url='bases:login')
@transaction.atomic
def participante_csv_delete(request,id=None):
    permission_required = 'par.delete_participante'
    #print('edu 01')
    if request.method == "POST":
        #print('edu 02')
        opc= request.POST.get("opc")
        idCsv = request.POST.get("id")
        evento = request.POST.get("evento")
        #print("accion a ejecutar ")
      
        if opc == "DEL":
            #print('edu 03')
            sid = transaction.savepoint()
            try:
               
                delParticipantes=Participante.objects.filter(participante_csv_id=idCsv).delete()
                
               
                record = Participante_Csv.objects.get(id=idCsv)
                record.delete()  
                liscsv = lista_participante_csv(evento)
               # lisUsuEve=lista_Usuarios_Evento(evento)
               # lisUsuario=lista_Usuarios_No_Evento(evento)
                             
                contexto={'mensaje':"Importación eliminada",
                                'error':'',
                                'rptaServer':"OK",
                                'liscsv': liscsv
                                }  
                status_code = 200
                #print("grabo ")
                #print(contexto)
                response = JsonResponse(contexto)
                response.status_code = status_code
                
           
            except Exception as e:
                transaction.savepoint_rollback(sid)
               # mensaje=str(e)
               # mensaje=mensaje.replace('"','')
               # mensaje=mensaje.replace("'","\\'")
               # mensaje=mensaje.lower()
               # mensaje=mensaje.replace("usuario_evento",'')
                rptaServer="OFF"
                contexto={'mensaje':'Error de integridad de datos (p)',
                            'error':'',
                            'rptaServer':'OFF'}  
                #print ('mensaje except')
                #print(contexto)
                response = JsonResponse(contexto)   
            except IntegrityError:
                transaction.savepoint_rollback(sid) 
                contexto={'mensaje':"Error de Integridad de datos (p)",
                            'error':'',
                            'rptaServer':'OFF'}  
               
                response = JsonResponse(contexto)   
            
                                
        else:
                contexto={'mensaje':'Acción desconocida ()',
                            'error':'',
                            'rptaServer':'OFF'}  
                #print (contexto)
                response = JsonResponse(contexto)
    else:
                contexto={'mensaje':'Acción desconocida (Post)',
                            'error':'',
                            'rptaServer':'OFF'}  
                #print (contexto)
                response = JsonResponse(contexto)
           
    return response
   



class TipoParticipanteList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'par.view_tipo_participante'
    template_name = "eve/tipo_participante_list.html"
    login_url = 'config:login'
    model = Tipo_Participante
    
    context_object_name = 'obj'    





class TipoParticipanteAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'par.add_tipo_participante'
    model = Tipo_Participante
    template_name="par/tipo_participante_add.html"    
    context_object_name = "obj"
    form_class = TipoParticipanteForm
    success_url = reverse_lazy("par:tipo_participante_list")
    #login_url ="bases:login"
    success_message="Tipo de participante creado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user        
        return super().form_valid(form)
    
    
class TipoParticipanteEdit(SuccessMessageMixin,SinPrivilegios,generic.UpdateView):
    permission_required="par.change_tipo_participante"
    model=Tipo_Participante
    template_name = "par/tipo_participante_add.html"    
    context_object_name = "obj"
    form_class = TipoParticipanteForm
    success_url = reverse_lazy("par:tipo_participante_list")
    #login_url ="bases:login"
    success_message="Tipo participante actualizado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.um_id = self.request.user.id
        return super().form_valid(form)    
    
    
    
class TipoParticipanteDelete(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario
    permission_required="par.delete_tipo_participante"
    model=Tipo_Participante
    template_name = "par/tipo_participante_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("par:tipo_participante_list")
    success_message="Tipo Participante eliminado Satisfactoriamente"   
    
    
    #def delete(request, *args, **kwargs):
   
    
  #  def form_valid(self, form):
  #      print('prision')
  #      print (self)
  #      print (form)
  #      if Participante.objects.filter(tipo_participante_id= self.id).exists():
  #          raise Exception('This team is related to a game.')  # or you can throw your custom exception here.
    
   #     return super().form_valid(form)
    
        
   # def delete(self, *args, **kwargs):
   #     print ('delte personalizado')
   #     if Participante.objects.filter(tipo_participante_id= self.pk).exists():
   #         raise Exception('This team is related to a game.')  # or you can throw your custom exception here.
   #     super(Tipo_Participante, self).delete(*args, **kwargs)    
    
    '''
    def form_valid(self, form, *args, **kwargs):
        print('VIEWSSS')
       #imprime url
       #print(self.request)
      
        #print('VIEWSSS 3333')
        #imprime datos configurados en _self
        #print(self.get_object())
        #print('VIEWSSS 4444')
        if Participante.objects.filter(tipo_participante_id= 3).exists():
            raise Exception('Tipo de Participante se esta utilizando VISTA')  # or you can throw your custom exception here.
        super(Tipo_Participante, self).delete(*args, **kwargs)  
        return super().form_valid(form)
   '''
    
@login_required(login_url='config:login')
@permission_required('par.delete_tipo_participante', login_url='bases:denegado')
def TipoParticipanteDel(request,pk=None):

   
    rptaServer="OFF"
    lista=""
    contexto={ 'rptaServer':rptaServer} 
    if request.method == "POST":
        #print('edu 02')
        opc= request.POST.get("opc")
        id= request.POST.get("id")
        
       
        if opc == "DEL":
           
            #sid = transaction.savepoint()
            try:
             
                if (Participante.objects.filter(tipo_participante_id=pk).exists()):
                   mensaje="Tipo participante existe en Evento, no se puede eliminar"
                  
                else:
                        
                   
                   #eveDelete = Evento.objects.get(id=pk)
                   parDelete = Tipo_Participante.objects.filter(id=pk)
                  
                   if (parDelete):       
                       parDelete.delete()  
                       rptaServer="OK"
                       mensaje="Tipo Participante eliminado con exito"   
                       lista=lista_Tipo_Participante(request.user.id,request.user.is_staff,"Q")  
                    
                   else:
                       mensaje="No existe Tipo Participante"   
                status_code = 200
                
           
            except Exception as e:
                rptaServer="OFF"
                mensaje="Error de integridad de datos 1(p)" 
                  
            except IntegrityError:
                 
                mensaje="Error de integridad de datos 2(p)" 
                rptaServer="OFF"
               
               
            contexto={'mensaje':mensaje,
                    'error':'',
                    'rptaServer':rptaServer,
                    'lista':lista
                     } 
                                
        else:
                contexto={'mensaje':'Acción desconocida ()',
                            'error':'',
                            'rptaServer':'OFF',
                            'lista':lista}  
                #print (contexto)
                
    else:
                contexto={'mensaje':'Acción desconocida (Post)',
                            'error':'',
                            'rptaServer':'OFF',
                            'lista':lista}  
                
    #print('contexto')
    #print(contexto)           
    response = JsonResponse(contexto) 
    if(rptaServer=='OK'):
        response.status_code = 200        
    return response
      



#class TipoParticipanteList(LoginRequiredMixin, PermissionRequiredMixin, ListView): 
#class ModalidadAsistenciaList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
class ModalidadAsistenciaList(LoginRequiredMixin, PermissionRequiredMixin, ListView): 
    permission_required = 'par.view_modalidad_asistencia'
    template_name = "eve/modalidad_asistencia_list.html"
    login_url = 'config:login'
    model = Modalidad_Asistencia    
    context_object_name = 'obj'    


class ccccccTipoParticipanteList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'par.view_tipo_participante'
    template_name = "eve/tipo_participante_list.html"
    login_url = 'config:login'
    model = Tipo_Participante
    
    context_object_name = 'obj'   


class ModalidadAsistenciaAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'par.add_modalidad_asistencia'
    model = Tipo_Participante
    template_name="par/modalidad_asistencia_add.html"    
    context_object_name = "obj"
    form_class = ModalidadAsistenciaForm
    success_url = reverse_lazy("par:modalidad_asistencia_list")
    #login_url ="bases:login"
    success_message="Modalidad de asistencia creada satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user        
        return super().form_valid(form)
    
    
class ModalidadAsistenciaEdit(SuccessMessageMixin,SinPrivilegios,generic.UpdateView):
    permission_required="par.change_modalidad_asistencia"
    model=Modalidad_Asistencia
    template_name = "par/modalidad_asistencia_add.html"    
    context_object_name = "obj"
    form_class = ModalidadAsistenciaForm
    success_url = reverse_lazy("par:modalidad_asistencia_list")
    #login_url ="bases:login"
    success_message="Modalidad de asistencia actualizado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.um_id = self.request.user.id
        return super().form_valid(form)    
    
class ModalidadAsistenciaDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario
    permission_required="par.delete_modalidad_asistencia"
    model=Modalidad_Asistencia
    template_name = "par/modalidad_asistencia_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("par:modalidad_asistencia_list")
    success_message="Modalidad asistencia eliminado Satisfactoriamente"     




@login_required(login_url='config:login')
@permission_required('par.view_participante', login_url='config:home')
def contarasistencia(request,participante_id=None):
#    class ModalidadEventoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'par.view_participante'

    template_name="par/busca_participante.html"
    #eve=Evento.objects.filter(estado=True)
    form_compras={}
    contexto={}
   #cuba
   
    evento = request.POST.get("evento")
    asistencia=Participante.objects.filter(Q(evento_id=evento) & Q(asistio_evento=True)).count()
    lisGrupalAsistencia=list(Participante.objects.filter(Q(evento_id=evento) & Q(asistio_evento=True)).values('tipo_participante','tipo_participante__descripcion_tipo_participante','tipo_participante__background_tipo_participante').annotate(dcount=Count('tipo_participante__id')))
    #print("este es el listado")   
    #print(lisGrupalAsistencia)
    
    
    

    
    #print('eduuuuuuuuuuuuuu')     
    if request.method=='POST':    
        #print('es pooooooooooossssttt')
        
        contexto={'rpta':'OK',
                  'asistencia':asistencia,
                  'lisGrupalAsistencia':lisGrupalAsistencia}            
        #print(contexto)                    
        return JsonResponse(contexto)
        
    return render(request, template_name, contexto)  


def valida_cabecera_csv(cp0,cp1,cp2,cp3,cp4,cp5,cp6,cp7,cp8):
    ret=""
   

    if cp0.strip() != 'apellido':
       ret+=","+cp0
    if cp1.strip() != 'nombre':
       ret+=","+cp1
    if cp2.strip() != 'email':
       ret+=","+cp2
    if cp3.strip() != 'empresa':
       ret+=","+cp3
    if cp4.strip() != 'cargo':
       ret+=","+cp4 
    if cp5.strip() != 'asistencia':
       ret+=","+cp5
    if cp6.strip() != 'tipo':
       ret+=","+cp6
    if cp7.strip() != 'asistira':
       ret+=","+cp7
    if cp8.strip() != 'qr':
       ret+=","+cp8     
    if(ret==''):  
       ret="OK"                     
    return ret       



def valida_email(email):
   emailObject = validate_email(email)
   #print(emailObject.email+" - " +email)


#user_email = input("Enter your Email Address: ")
#pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
def valida_email_fullmatch(user_email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

    msj="No valido"
    if not re.fullmatch(pattern, user_email):
       msj="OK"
    else:
       msj="OFF"
    #print(f"{user_email} is "+msj)
    return msj


def validar_email_personal(mail):
    mal = [mail,"i"]
    bien= [mail,"c"]
    if mail.count("@")!=1: return mal 
    name,dom=mail.split('@')
    if len(name)>=5 and ("." in dom):
        dom = f"@{dom}"
        if dom.index(".") in (len(dom), 1): return mal
        return bien 
    else: return mal 


def validar_email_personalizado(mail):
    mail=mail.lower()
  
    msg=""
    if(mail==''): return 'OK'
    if mail.count("@")!=1: return "Error no tiene @ "+mail 
    #print("El valor de {} es {}".format(letra, ord(letra)))

    lista=mail.split('@')
    
    for i in lista: 
        dato=i
        control=0
        for indice in range(len(dato)):
            caracter=dato[indice]
            nOrd = ord(caracter)
            if((nOrd >= 97 and nOrd <= 122) or (nOrd >= 48 and nOrd <= 57) ):
               control=0
            else:
                if(indice==0):
                    msg += "Error (i) " + caracter + " "+dato
                else:      
                    if(nOrd == 46 or nOrd == 95 or nOrd==45):
                       if(control == 0):
                           #msg += "Error " + caracter + " duplicado " +str(indice)   
                           control = indice                    
                       else:
                           
                           msg += "Error " + caracter + " duplicado " +str(indice)
                    
                    else:
                        msg += "Error caracter " + caracter
        #verifica que el ultimo caracter sea alfabetico o numerico            
        if(not((nOrd >= 97 and nOrd <= 122) or (nOrd >= 48 and nOrd <= 57))):      
            msg += "Error (f) " + caracter  +" "+dato    

    if(msg==""):
        msg="OK"                
    return msg
    


def validar_solo_caracteres(dato):
    #dato=dato.lower()
    control=0
    msg=""
    for indice in range(len(dato)):
        caracter=dato[indice]
        nOrd = ord(caracter)
        #if((nOrd >= 97 and nOrd <= 122) or (nOrd==164)):
        #or (nOrd >= 48 and nOrd <= 57)
        if(nOrd >= 97 and nOrd <= 122) or (nOrd >= 65 and nOrd <= 90)  or (nOrd in [225,233,237,243,250,193,201,205,211,218,209,241]):
    
            
            control=0
        else:    
            if(nOrd==32):
                if(control + 1 == indice):
                   msg += " Error espacio duplicado "                        
                else:
                    control = indice
                    
            else:
               
                msg += dato+" Error caracter no valido " + caracter + str(nOrd)
    if(msg==""):
        msg="OK"                
    return msg
  
#cadena = "¡Hola, mundo!"

# Método 2, con índice
"""for indice in range(len(cadena)):
    caracter = cadena[indice]
    print("En el índice {} tenemos a '{}'".format(indice, caracter))"""
    
    
def lista_participante_csv(evento):
 liscsv=list(Participante_Csv.objects.select_related("Usuario").filter(Q(evento_id=evento)).values("id",
                       "evento_id","archivo_csv","cantidad","fc"))
 return liscsv



def lista_Tipo_Participante(pkUser,staff,tipo):
    if tipo=="O":
        
        lisTipoParticipante = Tipo_Participante.objects.all()
        
    else:
       
        lisTipoParticipante=list(Tipo_Participante.objects.filter().values("id","descripcion_tipo_participante",
    "background_tipo_participante","tipo_identificacion_participante"))
                 
   
    #print("sergio")           
    #print(lisTipoParticipante)         
    return lisTipoParticipante;   




@login_required(login_url='config:login')
@permission_required('par.view_participante', login_url='config:home')
def x__lecturaqr(request,participante_id=None):
#    class ModalidadEventoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'par.view_participante'

    template_name="par/lectura_qr.html"
   
    form_compras={}
    contexto={}
    par_evento_id=0
    nombre=''
    apellido =''
    evento=0,
    lisparb=""
    #print('eduuuuuuuuuuuuuu')
    pkUser=request.user.pk
  
    if request.method=='GET':
        #print('es geeeeeeeeetttttttttttttt')
        #Formulario creado en forms.py
        form_buscar=BuscarParticipanteForm()
        
        lisEventos = lista_Eventos_Por_Acceso(pkUser,request.user.is_staff,"O")
        
       
        #crea objeto vacio
        lispar=""
       
        
        #En el contexto definimos que mandamos a la plantilla
        
        contexto={'eve':form_buscar,'lispar':lispar, 'liseventos':lisEventos}
        # la impresion de contexto ejecutara consulta a la BD
        #print(contexto)
        return render(request, template_name,contexto )    
        
    if request.method=='POST':    
        #print('es pooooooooooossssttt')
        
        evento = request.POST.get("evento")
        codigo_qr = request.POST.get("codigo_qr")
       
       
        if (evento=='0'):
            #print('Seleccione Evento') 
            contexto={'rpta':'OFF',
                  'lispar':'',
                  'mensaje':'Seleccione Evento'}  
        else:    
        
            if (len(codigo_qr)==0):  
                contexto={'rpta':'OFF',
                  'lispar':'',
                  'mensaje':'Seleccione Evento'}  
            #else:    
                #print('Actualiza')
                   
                
           
               
                
                        
            #print('json es') 
            contexto={'rpta':'OK',
                  'lispar':lispar}            
        #print(contexto)                    
    return JsonResponse(contexto)
        
    return render(request, template_name, contexto)  