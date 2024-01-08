from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#permisos para validar acceso de funciones
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *

from .models import Modalidad_Evento, Evento, Usuario, Usuario_Evento
from .forms import ModalidadEventoForm,EventoForm, UsuarioEventoForm

from bases.views import SinPrivilegios

from django.db.models import Q
import json


# Create your views here.
#class TipoEventoList(LoginRequiredMixin, PermissionRequiredMixin):
    #template_name = "eve/tipo_evento_list.html"
#class TipoEventoList(ListView):    

class ModalidadEventoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'eve.view_modalidad_evento'
    template_name = "eve/tipo_evento_list.html"
    login_url = 'config:login'
    model = Modalidad_Evento
    
    context_object_name = 'obj'    


@login_required(login_url='config:login')
@permission_required('bases.change_modalidad_evento', login_url='config:home')
def x_ModalidadEventoAdd(request,pk=None):
    template_name = "eve/modalidad_evento_add.html"
    context = {}
    form = None
    obj = None

    if request.method == "GET":
        if not pk:
            form = ModalidadEventoForm(instance = None )
        else:
            obj = Modalidad_Evento.objects.filter(id=pk).first()
            form = ModalidadEventoForm(instance = obj)
        context["form"] = form
        
        
    
    if request.method == "POST":
        data = request.POST
        e = data.get("descripcion_modalidad_evento")
        #fn = data.get("first_name")
        #ln = data.get("last_name")
        fn = data.get("estado")
        

        if pk:
            obj = Modalidad_Evento.objects.filter(id=pk).first()
            if not obj:
                print("Error Modalidad No Existe")
            else:
                obj.descripcion_modalidad_evento = e                
                obj.estado = fn
                obj.save()
        else:
            obj = Modalidad_Evento.objects.create_Modalidad_Evento(
            
                descripcion_modalidad_evento = e,
                estado = fn                

            )
            print(obj.descripcion_modalidad_evento,obj.estado)
        return redirect('eve:modalidad_evento_list')
    
    return render(request,template_name,context)




class ModalidadEventoAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'eve.add_modalidad_evento'
    model = Modalidad_Evento
    template_name="eve/modalidad_evento_add.html"    
    context_object_name = "obj"
    form_class = ModalidadEventoForm
    success_url = reverse_lazy("eve:modalidad_evento_list")
    #login_url ="bases:login"
    success_message="Modalidad creada satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user        
        return super().form_valid(form)
    
    
class ModalidadEventoEdit(SuccessMessageMixin,SinPrivilegios,generic.UpdateView):
    permission_required="eve.change_modalidad_evento"
    model=Modalidad_Evento
    template_name = "eve/modalidad_evento_add.html"    
    context_object_name = "obj"
    form_class = ModalidadEventoForm
    success_url = reverse_lazy("eve:modalidad_evento_list")
    #login_url ="bases:login"
    success_message="Modalidad actualizda satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.um_id = self.request.user.id
        return super().form_valid(form)    
    
class ModalidadEventoDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario
    permission_required="eve.delete_modalidad_evento"
    model=Modalidad_Evento
    template_name = "eve/modalidad_evento_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("eve:modalidad_evento_list")
    success_message="Modalidad Eliminada Satisfactoriamente"     
    
    
    
#class EventoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
class EventoList(SuccessMessageMixin, SinPrivilegios, ListView):
    permission_required = 'eve.view_evento'
    template_name = "eve/evento_list.html"
    login_url = 'config:login'
    model = Evento    
    context_object_name = 'obj'    
    
       
#class EventoAdd(LoginRequiredMixin, generic.CreateView):
class EventoAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):    
    permission_required = 'eve.add_evento'
    model = Evento
    template_name = "eve/evento_form.html"
    context_object_name = "obj"
    form_class = EventoForm
    success_url = reverse_lazy("eve:evento_list")
    login_url ="config:login"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)        
    

class EventoEdit(SuccessMessageMixin,SinPrivilegios,generic.UpdateView):    
#class EventoEdit(LoginRequiredMixin, generic.UpdateView):
    permission_required="eve.change_evento"
    model=Evento
    template_name = "eve/evento_form.html"
    context_object_name = "obj"
    form_class = EventoForm
    success_url = reverse_lazy("eve:evento_list")
    login_url ="config:login"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.um_id = self.request.user.id
        print ("form.instance.id")
        print (form.instance.id)
        return super().form_valid(form)



class EventoDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario
    permission_required="eve.delete_evento"
    model=Evento
    template_name = "eve/evento_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("eve:evento_list")
    success_message="Evento Eliminado Satisfactoriamente"   
    
    
    
#@login_required(login_url='config:login')
#@permission_required('par.view_participante', login_url='config:home')
def buscarusuarioevento(request,evento=None):
#    permission_required = 'par.view_participante'

    template_name="eve/usuario_evento.html"
    #eve=Evento.objects.filter(estado=True)
    form_compras={}
    contexto={}
   
    evento=0,
   
    print('eduuuuuuuuuuuuuu')
    if request.method=='GET':
        print('es geeeeeeeeetttttttttttttt')
        #Formulario creado en forms.py
        lisEventos=Evento.objects.filter(estado=True)
      
       
    

        #contexto={'eve':form_buscar,'lispar':lispar, 'liseventos':lisEventos}
        contexto={'liseventos':lisEventos}
        print(contexto)
        return render(request, template_name, contexto)    
        
    if request.method=='POST':    
        print('es pooooooooooossssttt')
        evento = request.POST.get("evento")
        print(evento)
        lisUSuarios = []  
        lisUsuariosEvento = []
          
        if evento=='0':
           lisUsuariosEvento=[]
           lisUSuarios=[] 
           print("evento vacio")
        else:    
            print("evento lleno")
            #lisUsuariosEvento=list(Usuario_Evento.objects.select_related("evento","usuario").filter(Q(evento_id=evento)).values("id",
            #       "evento_id","usuario_id","usuario__nombre","usuario__apellido"))
            lisUsuariosEvento=lista_Usuarios_Evento(evento)
            
        
            
            #lisUsuarios=list(Usuario.objects.all().exclude(id__in=(Usuario.objects.select_related("usuario_evento").filter(Q(usuario_evento__evento_id=evento)).values("id"))).values('id','apellido','nombre'))                
            lisUsuarios=lista_Usuarios_No_Evento(evento)
            #lisUsuarios=list(Usuario.objects.all().values('id','apellido','nombre'))
            #lisUsuarios=list(Usuario.objects.all().exclude(id=lisUsuariosEvento).values('id','apellido','nombre'))    
                 
                 
                 
        
        contexto={'rpta':'OK',
                  'lisUsuariosEvento':lisUsuariosEvento,
                  'lisUsuarios':lisUsuarios
                  }      
              
        print(contexto) 
       
        return JsonResponse(contexto)
        
    return render(request, template_name, contexto) 


class UsuarioEventoAdd_2(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    permission_required = 'eve.add_modalidad_evento'
    model = Usuario_Evento
    template_name="eve/modalidad_evento_add.html"    
    context_object_name = "obj"
    form_class = ModalidadEventoForm
    success_url = reverse_lazy("eve:modalidad_evento_list")
    #login_url ="bases:login"
    success_message="Modalidad creada satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        form.instance.uc = self.request.user        
        return super().form_valid(form) 
    


class UsuarioEventoAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):    
  
    permission_required = 'eve.add_usuario_evento'
    model = Usuario_Evento
    template_name="/eve/usuario_evento.html"    
    context_object_name = "obj"
    form_class = UsuarioEventoForm
    success_url = reverse_lazy("eve:usuario_evento")
    #login_url ="bases:login"
    success_message="Usuario asignado satisfactoriamente"
    
    #se carga en el form el usuario logueado
    def form_valid(self, form):
        print("es valido")
        print("no es valido xxxxxxxxxxxxxxxxx")  
          
        form.instance.uc = self.request.user 
        evento = form.instance.evento  
        form.save()     
        print("nuevo usuario")
        return super().form_valid(form)
    
    #def get_context_data(self, **kwargs):
    #    context = super(ParticipanteAdd, self).get_context_data(**kwargs)
    #    context["eventos"] = Evento.objects.all()
    #    context["tipos"] = Tipo_Participante.objects.all()
    #    context["modalidades"] = Modalidad_Asistencia.objects.all()
    #    return context
    
    def post(self, request, *args, **kwargs):
        print("post")
        requestValido="OK"
        response=""
        
        form = self.form_class(request.POST)
        try: 
            if (form.is_valid()):
                form.instance.uc = self.request.user 
                pkEvento=request.POST.get("evento") 
                form.save() 
                
                lisUsuEve=lista_Usuarios_Evento(pkEvento)
                lisUsuario=lista_Usuarios_No_Evento(pkEvento)
               
                
                contexto={'mensaje':"Acceso a usuario realizado",
                          'error':'',
                          'rptaServer':"OK",
                          'lisUsuariosEvento': lisUsuEve,
                          'lisUsuarios': lisUsuario}  
                          
                            
                status_code = 200
                print("grabo ")
                response = JsonResponse(contexto)
                response.status_code = status_code
            else:
                status_code = 400
                error= form.errors 
                print("form.errors 491")
                contexto={'mensaje':"Verifique Datos",
                        'error':error,
                        'rptaServer':'OFF'} 
                response = JsonResponse(contexto)
                response.status_code = status_code
                
                
            print("debe de regresar 645")  
            print(contexto)
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
    
    
    
class UsuarioEventoDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario

    permission_required="eve.delete_usuario_evento"
    model = Usuario_Evento
    template_name="/eve/usuario_evento.html"       
    context_object_name = "obj"
    success_url = reverse_lazy("eve:usuario_evento")
    success_message="Acceso de usuario eliminado"
    
    
    
    
@login_required(login_url='config:login')
@permission_required('bases.change_usuario', login_url='bases:login')
def usuarioAccesoEvento(request,accion=None):
    permission_required = 'eve.delete_usuario_evento'
    if request.method == "POST":
        opc= request.POST.get("opc")
        usuario = request.POST.get("usuario")
        evento = request.POST.get("evento")
        print("accion a ejecutar ")
      
        if opc == "DEL":
            try:
                #record = Usuario_Evento.objects.get(id=usuario)
                record = Usuario_Evento.objects.filter(usuario_id=usuario,evento_id=evento)
                record.delete()  
                lisUsuEve=lista_Usuarios_Evento(evento)
                lisUsuario=lista_Usuarios_No_Evento(evento)
                             
                contexto={'mensaje':"Acceso de usuario eliminado",
                                'error':'',
                                'rptaServer':"OK",
                                'lisUsuariosEvento': lisUsuEve,
                                'lisUsuarios': lisUsuario}  
                status_code = 200
                print("grabo ")
                response = JsonResponse(contexto)
                response.status_code = status_code
                
           
            except Exception as e:
            
                mensaje=str(e)
                mensaje=mensaje.replace('"','')
                mensaje=mensaje.replace("'","\\'")
                mensaje=mensaje.lower()
                mensaje=mensaje.replace("usuario_evento",'')
                rptaServer="OFF"
                contexto={'mensaje':mensaje,
                            'error':'',
                            'rptaServer':'OFF'}  
                print ('mensaje except')
               
                print (e)
                response = JsonResponse(contexto)
                
        else:
                contexto={'mensaje':'Acción desconocida',
                            'error':'',
                            'rptaServer':'OFF'}  
                print (contexto)
                response = JsonResponse(contexto)
    else:
                contexto={'mensaje':'Acción desconocida',
                            'error':'',
                            'rptaServer':'OFF'}  
                print (contexto)
                response = JsonResponse(contexto)
    return response
        
        
       
       
def lista_Usuarios_Evento(evento):
    lisUsuariosEvento=list(Usuario_Evento.objects.select_related("evento","usuario").filter(Q(evento_id=evento)).values("id",
                   "evento_id","usuario_id","usuario__nombre","usuario__apellido")) 
    return lisUsuariosEvento;


def lista_Usuarios_No_Evento(evento):
    lisUsuarios=list(Usuario.objects.all().exclude(id__in=(Usuario.objects.select_related("usuario_evento").filter(Q(usuario_evento__evento_id=evento)).values("id"))).values('id','apellido','nombre'))                
    return lisUsuarios;        
        

def lista_Eventos_Por_Acceso(pkUser,staff):
    if staff:
           lisEventos = Evento.objects.all().only('id','estado','nombre_evento')
           #lisEventos = ""         
    else:
            #filtra por relacion
            lisEventos = Evento.objects.filter(usuario_evento__usuario_id=pkUser).only('id','estado','nombre_evento')
    return lisEventos;        
      
