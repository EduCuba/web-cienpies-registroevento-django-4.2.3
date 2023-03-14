from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

#permisos para validar acceso de funciones
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *

from .models import Participante
#from eve.models import Evento
from .forms import BuscarParticipanteForm,ParticipanteForm


from bases.views import SinPrivilegios


from eve.models import Evento


from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.http import JsonResponse


from django.http import JsonResponse
from django.core.serializers import serialize
import json

# Create your views here.

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
    
    

def buscarparticipante(request,participante_id=None):
    template_name="par/busca_participante.html"
    #eve=Evento.objects.filter(estado=True)
    form_compras={}
    contexto={}
    par_evento_id=0
    nombre=''
    apellido =''
    evento=0,
    lisparb=""
    print('eduuuuuuuuuuuuuu')
    if request.method=='GET':
        print('es geeeeeeeeetttttttttttttt')
        #Formulario creado en forms.py
        form_compras=BuscarParticipanteForm()
        #lispar = Participante.objects.filter(pk=participante_id).first()
        #lispar = Participante.objects.filter(evento_id=par_evento_id)
        #lisparb = Participante.objects.filter(nombre_participante__search=nombre) 
        #lispar = Participante.objects.filter(nombre_participante__unaccent__icontains=nombre)
        #consulta or
        #lispara = Participante.objects.filter(nombre_participante__unaccent__icontains=nombre,apellido_participante__unaccent__icontains=apellido)
        #consulta And
        #lisparb = Participante.objects.filter(nombre_participante__unaccent__icontains=nombre).filter(apellido_participante__unaccent__icontains=apellido)
                                                                
        
        

        #lispar=Participante.objects.filter(Q(evento_id=evento) & (Q(nombre_participante__unaccent__icontains=nombre) | Q(apellido_participante__unaccent__icontains=apellido)))
        lispar=Participante.objects.filter(Q(evento_id=par_evento_id))
        
        #lisparb = Participante.objects.filter(nombre_participante__trigram_similar=nombre) 

        
        #print("lisparA")   
        #print(lispara)
        #print("lisparb")   
        #print(lisparb)
        #print("lisparc")   
        #print(lispar)
        #En el contexto definimos que mandamos a la plantilla
        contexto={'eve':form_compras,'lispar':lispar}
        return render(request, template_name, contexto)    
        
    if request.method=='POST':    
        print('es pooooooooooossssttt')
        apellido_participante = request.POST.get("apellido_participante")
        nombre_participante = request.POST.get("nombre_participante")
        empresa_participante = request.POST.get("empresa_participante")
        evento = request.POST.get("evento")
        print(apellido_participante)    
        print(nombre_participante)    
        print(empresa_participante)
        print(evento)  
        
        if (len(empresa_participante)==0):  
            if(nombre_participante==""):
                lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__unaccent__icontains=apellido_participante)).values("id",
                "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante"))
                print('busqueda por apellido : caso 1')
            else:
                if(apellido_participante==""):
                   lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(nombre_participante__unaccent__icontains=nombre_participante)).values("id",
                   "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                   "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante"))
                   print('busqueda por nombre : caso 2')
                else:   
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(nombre_participante__unaccent__icontains=nombre_participante) & Q(apellido_participante__unaccent__icontains=apellido_participante)).values("id",
                   "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                   "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante"))
                    print('busqueda por apellido y nombre : caso 3')
        else:
            if (len(apellido_participante) > 0 and len(nombre_participante) > 0):    
                lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(apellido_participante__unaccent__icontains=apellido_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).values("id",
                "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante"))
                print('busqueda por empresa, apellido y nombre : caso 4')
            else:    
                if (nombre_participante == ""):
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(apellido_participante__unaccent__icontains=apellido_participante)).values("id",
                    "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante"))
                    print('busqueda por empresa y apellid : caso 5')
                else:    
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).values("id",
                    "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante"))
                    print('caso empresa y nombre')
                
                        
        print('json es') 
        
        #serialized_data = serialize("json", lispar)
        #serialized_data = json.loads(serialized_data)
        #serialized_data 
                                           
        
        contexto={'rpta':'OK',
                  'lispar':lispar}            
        print(contexto)                    
        return JsonResponse(contexto)
        
    return render(request, template_name, contexto)    



def participanteAsistencia(request, id):
    idPar=request.POST.get("id")
    print("imprime id request")
    print(id)
    participante = Participante.objects.filter(pk=id).first()
    
    print("edu 01")
    contexto={'rpta':'OFF'}          
    if request.method=="POST":
        print("edu 02") 
        if participante:
            print("edu 03") 
            participante.asistio_evento = not participante.asistio_evento
            participante.save()
            contexto={'rpta':'OK',
                     'asistio_evento':participante.asistio_evento}  
            return JsonResponse(contexto,safe=False)      
        print("edu 04")
        return JsonResponse(contexto)      
    print("edu 05")
    return JsonResponse(contexto)      

    

    
    
      







#class ParticipanteAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
class ParticipanteAdd(generic.CreateView):    
    #permission_required = 'eve.add_modalidad_evento'
    model = Participante
    template_name="par/participante_add.html"    
    context_object_name = "obj"
    form_class = ParticipanteForm
    success_url = reverse_lazy("par:buscar_participante")
    #login_url ="bases:login"
    success_message="Participante registrado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user        
        return super().form_valid(form)
    

