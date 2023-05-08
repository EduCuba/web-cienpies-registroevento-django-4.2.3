from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

#permisos para validar acceso de funciones
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *

from .models import Participante, Tipo_Participante, Modalidad_Asistencia
#from eve.models import Evento
from .forms import BuscarParticipanteForm,ParticipanteForm,CreateForm


from bases.views import SinPrivilegios


from eve.models import Evento


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
        form_buscar=BuscarParticipanteForm()
        lisEventos = Evento.objects.all()
        
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
        contexto={'eve':form_buscar,'lispar':lispar, 'liseventos':lisEventos}
        print(contexto)
        return render(request, template_name, contexto)    
        
    if request.method=='POST':    
        print('es pooooooooooossssttt')
        apellido_participante = request.POST.get("apellido_participante")
        nombre_participante = request.POST.get("nombre_participante")
        empresa_participante = request.POST.get("empresa_participante")
        evento = request.POST.get("evento")
        print(apellido_participante)    
        print(nombre_participante)    
        print("empresa")
        print(empresa_participante)
        print(evento)  
         
        
        if (len(empresa_participante)==0):  
            
            if (len(apellido_participante) == 0 and len(nombre_participante) == 0):    
                   lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento)).values("id",
                   "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                   "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
                   print('busqueda solo por evento')
            else:    
                if (len(apellido_participante) > 0 and len(nombre_participante) > 0):    
                   lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__unaccent__icontains=apellido_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).values("id",
                   "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                   "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
                   print('busqueda por apellido y nombre : caso empresa vacio')
                else:
                    if (nombre_participante == ""):
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(apellido_participante__unaccent__icontains=apellido_participante)).values("id",
                        "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
                        print('busqueda por apellido :  empresa vacio')
                    else:    
                        lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(nombre_participante__unaccent__icontains=nombre_participante)).values("id",
                        "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                        "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
                        print('busqueda por nombre caso empresa vacia')
            
        else:
            if (len(apellido_participante) > 0 and len(nombre_participante) > 0):    
                lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(apellido_participante__unaccent__icontains=apellido_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).values("id",
                "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
                print('busqueda por empresa, apellido y nombre : caso 4')
            else:    
                if (nombre_participante == ""):
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(apellido_participante__unaccent__icontains=apellido_participante)).values("id",
                    "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
                    print('busqueda por empresa y apellid : caso 5')
                else:    
                    lispar=list(Participante.objects.select_related("modalidad_asistencia","tipo_participante").filter(Q(evento_id=evento) & Q(empresa_participante__unaccent__icontains=empresa_participante) & Q(nombre_participante__unaccent__icontains=nombre_participante)).values("id",
                    "evento_id","modalidad_asistencia_id","modalidad_asistencia__descripcion_modalidad_asistencia","apellido_participante","nombre_participante",
                    "email_participante","empresa_participante","asistio_evento","tipo_participante__descripcion_tipo_participante","tipo_participante__background_tipo_participante"))
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





#@login_required(login_url="/login/")
#@permission_required("cmp.change_proveedor",login_url="bases:sin_privilegios")
#def proveedorInactivar(request,id):



@login_required(login_url='config:login')
@permission_required('par.edit_participante', login_url='bases:sin_privilegios')
#@permission_required('par.edit_participante', login_url='config:home')
#@permission_required('par.edit_participante', raise_exception=True)
def participanteAsistencia(request, id):
    
    
    
    try:
        permission_required = 'par.edit_participante'
    
        idPar=request.POST.get("id")
        tipo=request.POST.get("tipo")
        print("imprime id request")
        print(id)
        print("imprime idpar")
        print(idPar)
        print(tipo)
        participante = Participante.objects.filter(pk=id).first()
        
        print("edu 01")
        contexto={'rpta':'OFF'}          
    
        if request.method=="POST":
           print("edu 02") 
           if participante:
               if tipo=="A":
                   print("edu 03") 
                   participante.asistio_evento = not participante.asistio_evento
                   participante.save()
                   contexto={"id": participante.id,
                            'rpta':'OK',
                             'asistio_evento':participante.asistio_evento}      
                    
                   print(contexto)
                   return JsonResponse(contexto,safe=False)      
               
                   
        print("edu 04")
        return JsonResponse(contexto)      
        print("edu 05")
        return JsonResponse(contexto)     
    except ValueError as e:            
        mensaje=str(e)
        print("captura el error")
        mensaje=mensaje.replace('"','')
        mensaje=mensaje.replace("'","\\'")
        rptaServer="OFF"
        contexto={'rpta':'OFF',
                  'mensaje':mensaje}      
        return JsonResponse(contexto)     
        
        
     




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
        print("eduuuuuuuuuuuuuuuu get_context_data 238")
        print(context)        
        return context
        
    def form_valid(self, form):
        print(form.instance.id)
        print(form.instance.apellido_participante)
        
        print("es valido")
        print("no es valido")    
        print(form.instance.apellido_participante)
        
        
        
        try: 
            if (form.is_valid()):
                                
                status_code = 200
                form.instance.um = self.request.user   
                print(form.instance.id)
                print(form.instance.apellido_participante)
                form.save()                 
                
                ##return super().form_valid(form)                        
                
                contexto={'mensaje':"Datos actualizados",
                         'error':'',
                         'rptaServer':"OK"}  

                print("grabo edit ")
                response = JsonResponse(contexto)
                response.status_code = status_code
            else:
                status_code = 400
                error= form.errors 
               # print("form.errors")
               # print(form.errors.as_data())
               # print("solo error")
               # print(error)
                contexto={'mensaje':"Verifique Datos",
                        'error':error,
                        'rptaServer':'OFF'} 
                response = JsonResponse(contexto)
                response.status_code = status_code
                
                
            print("debe de regresar de edit")  
            print(contexto)
            print(response)
            return response

        except ValueError as e:
            
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':'mensaje',
                            'error':'',
                            'rptaServer':'OFF'}  
            print ('mensaje except')
            print (contexto)
            response = JsonResponse(contexto)
            print(response)
            return response
         
    

    def post(self, request, *args, **kwargs):
        print("post edi")
        print(request.POST.get("apellido_participante"))
        print(request.POST.get("id"))                
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

                    participante.uc = self.request.user   
                    
                    print("form.instance,id")
                    print(participante.id)
                    print(to_dict(participante))
                    
                    
                    participante.save() 
                    tipo_par= Tipo_Participante.objects.filter(pk=request.POST.get("tipo_participante")).first()
                    
                    data = {
                           "id": participante.id,
                           "asistio_evento": participante.asistio_evento,
                           "tipo_participante" : tipo_par.descripcion_tipo_participante,
                           "background_tipo_participante" : tipo_par.background_tipo_participante,
                           "rpta":"OK"
                           }


                    
                    contexto={'mensaje':"Datos actualizados EDIT",
                                'error':'',
                                'rptaServer':"OK",
                               'participante' : data}  
                    status_code = 200
                    print("grabo ")
                    response = JsonResponse(contexto)
                    response.status_code = status_code
                else:
                    contexto={'mensaje':"Participante no Existe",
                                'error':'',
                                'rptaServer':"OFF"}  
                    status_code = 200
                    print("grabo")
                    response = JsonResponse(contexto)
                    response.status_code = status_code
                    
                    
                        
            else:
                status_code = 400
                error= form.errors 
                print("form.errors 491")
               # print(form.errors.as_data())
               # print("solo error")
               # print(error)
                contexto={'mensaje':"Verifique Datos",
                        'error':error,
                        'rptaServer':'OFF'} 
                response = JsonResponse(contexto)
                response.status_code = status_code
                
                
            print("debe de regresar")  
            print(contexto)
            print(response)
            return response

        except ValueError as e:
            
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':'mensaje',
                            'error':'',
                            'rptaServer':'OFF'}  
            print ('mensaje except')
            print (contexto)
            response = JsonResponse(contexto)
            print(response)
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
        print("es valido")
        print("no es valido")    
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
                print("salvaod https://www.youtube.com/watch?v=JpPUX9GIFL8")
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
                print("form.errors")
                print(form.errors.as_data())
                print("solo error")
                print(error)
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
                    
                    print(contexto)
                    form.instance.uc = self.request.user   
                    form.save() 
                    print("grabo ")
                else:    
                    status_code = 400
                            
                        
                response = JsonResponse(contexto)
                response.status_code = status_code
                print (contexto)
                print(response)
            return response

        except ValueError as e:
            
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':mensaje,
                            'error':'',
                            'rptaServer':'OFF'}  
            print ('mensaje except')
            print (contexto)
            response = JsonResponse(contexto)
            print(response)
            return response
            
        
            
        return redirect('par:buscar_participante')



class ParticipanteAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):    
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
    def form_valid(self, form):
        print("es valido")
        print("no es valido")    
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
        print("post")
        requestValido="OK"
        response=""
        
        form = self.form_class(request.POST)
        try: 
            if (form.is_valid()):
                
                form.instance.uc = self.request.user   
                form.save() 
                contexto={'mensaje':"Datos actualizados",
                            'error':'',
                            'rptaServer':"OK"}  
                status_code = 200
                print("grabo ")
                response = JsonResponse(contexto)
                response.status_code = status_code
            else:
                status_code = 400
                error= form.errors 
                print("form.errors 491")
               # print(form.errors.as_data())
               # print("solo error")
               # print(error)
                contexto={'mensaje':"Verifique Datos",
                        'error':error,
                        'rptaServer':'OFF'} 
                response = JsonResponse(contexto)
                response.status_code = status_code
                
                
            print("debe de regresar")  
            print(contexto)
            print(response)
            return response

        except ValueError as e:
            
            mensaje=str(e)
            mensaje=mensaje.replace('"','')
            mensaje=mensaje.replace("'","\\'")
            rptaServer="OFF"
            contexto={'mensaje':'mensaje',
                            'error':'',
                            'rptaServer':'OFF'}  
            print ('mensaje except')
            print (contexto)
            response = JsonResponse(contexto)
            print(response)
            return response
            
        
            
        return redirect('par:buscar_participante')



def DetailForm(request):
    if request.method == "POST":  
        form = CreateForm(request.POST)
        print('Estoy aqui')
        if form.is_valid():
            print('First Name:', form.cleaned_data['apellido_participante'])
            print('Last Name:', form.cleaned_data['nombre_participante'])
            print('Email:', form.cleaned_data['Email'])
    else:
        print('salvame bb')
        #context = CreateForm(request)
        #context = super(Participante, self).get_context_data(**kwargs)
        #context["eventos"] = Evento.objects.all()
        #context["tipos"] = Tipo_Participante.objects.all()
        #context["modalidades"] = Modalidad_Asistencia.objects.all()
        #return context
    return redirect('par/participante_form.html')



def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data

