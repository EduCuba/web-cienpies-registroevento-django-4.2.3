from typing import Any
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
from par.models import Participante
from bases.views import SinPrivilegios, SinPrivilegiosAjax

from django.db.models import Q
import json

from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages


from django.db import transaction
from django.db import IntegrityError

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
   
   
#https://www.youtube.com/watch?v=IYQFt8XJiIU video de eliminar    
class ModalidadEventoDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario   
   
    print('educubaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    permission_required="eve.delete_modalidad_evento"
    model=Modalidad_Evento
    template_name = "eve/modalidad_evento_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("eve:modalidad_evento_list")
    success_message="Modalidad Eliminada Satisfactoriamente"
   
  
    
    
    
    def form_valid(self, form, **kwargs):
        
      # self.object = self.get_object() # assign the object to the view
      # form = self.get_form()
      # print(form)
       #if not (Modalidad_Evento.objects.filter(id= self.kwargs['pk']).exists()): 
       #    raise Exception('Modalidad no existe') 
       if Evento.objects.filter(modalidad_evento_id= self.kwargs['pk']).exists(): 
           messages.add_message(self.request,messages.WARNING,"Form is invalid")
           raise Exception('Modalidad esta siendo utilizada en Evento(s)') 
       return super(ModalidadEventoDel, self).form_valid(form)
       #return redirect('/eve/modalidad_evento_del.html')
       #response = redirect('/modalidad_evento_list/')
       #return response
       
   
    def form_invalid(self, form):
        'form is invalid'
        messages.add_message(self.request,messages.WARNING,"Form is invalid")
        return redirect('/modalidad_evento_list/')
    
        
   
    
   
   
   
    '''
    def get_context_data(self, **kwargs):
        r = super().get_context_data(**kwargs) 
        r['rptaServer'] ='OK'
        r['mensaje'] ='Datos Eliminados OK'
        r['list_url'] =reverse_lazy("eve:modalidad_evento_list")
        
        return r
        
    '''
    '''
    def get_context_data(self, **kwargs):
        r = super().get_context_data()
        r['g_name'] = Evento.objects.filter(id=self.kwargs['pk']).values('nombre_evento')
       
        return r
'''
  
      
   
      
   
   
  
    
#class EventoList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
class EventoList(SuccessMessageMixin, SinPrivilegios, ListView):
    permission_required = 'eve.view_evento'
    template_name = "eve/evento_list.html"
    login_url = 'config:login'
    model = Evento    
    context_object_name = 'obj'  
    def get_queryset(self):
        lisModel=lista_Eventos_Por_Acceso(self.request.user.id,self.request.user.is_staff,"O")
        #likes = Evento.objects.filter(like = True).count() #el resultado es un int
        #dislikes = Evento.objects.filter(dislike = True).count() #el resultado es un int

        return lisModel #o dislikes 
       
    
       
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


'''
Se desactivo , para poder controlar se creo una funcion definida
class EventoDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario
    permission_required="eve.delete_evento"
    model=Evento
    template_name = "eve/evento_del.html"
    context_object_name = "obj"
    success_url = reverse_lazy("eve:evento_list")
    success_message="Evento Eliminado Satisfactoriamente"   
'''    



@login_required(login_url='config:login')
@permission_required('eve.delete_evento', login_url='bases:denegado')
def EventoDel(request,pk=None):

   
    rptaServer="OFF"
    lista=""
    contexto={
                    'rptaServer':rptaServer
                   
                     } 
    if request.method == "POST":
        print('edu 02')
        opc= request.POST.get("opc")
        id= request.POST.get("id")
        
       
        if opc == "DEL":
           
            #sid = transaction.savepoint()
            try:
             
                if (Participante.objects.filter(evento_id=pk).exists()):
                   mensaje="Evento no se puede eliminar, tiene participantes"
                  
                else:
                        
                   
                   #eveDelete = Evento.objects.get(id=pk)
                   eveDelete = Evento.objects.filter(id=pk)
                  
                   if (eveDelete):       
                       eveDelete.delete()  
                       rptaServer="OK"
                       mensaje="Evento eliminado con exito"   
                       lista=lista_Eventos_Por_Acceso(request.user.id,request.user.is_staff,"Q")  
                    
                   else:
                       mensaje="No existe Evento"   
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
                print (contexto)
                
    else:
                contexto={'mensaje':'Acción desconocida (Post)',
                            'error':'',
                            'rptaServer':'OFF',
                            'lista':lista}  
                
    print(contexto)           
    response = JsonResponse(contexto) 
    if(rptaServer=='OK'):
        response.status_code = 200        
    return response
  

   
  
@login_required(login_url='config:login')
@permission_required('eve.view_usuario_evento', login_url='config:home')
def buscarusuarioevento(request,evento=None):
    permission_required = 'eve.view_usuario_evento'

    template_name="eve/usuario_evento.html"
    #eve=Evento.objects.filter(estado=True)
    form_compras={}
    contexto={}
   
    evento=0,
   
    print('eduuuuuuuuuuuuuu')
    if request.method=='GET':
        print('es geeeeeeeeetttttttttttttt')
        #Formulario creado en forms.py
        lisEventos=lista_Eventos_Por_Acceso(request.user.id,request.user.is_staff,"O")
     
       
    

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
    


#class UsuarioEventoAdd(SuccessMessageMixin, SinPrivilegios, generic.CreateView):    

class UsuarioEventoAdd(SuccessMessageMixin, SinPrivilegiosAjax, generic.CreateView):    
   
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

    #return redirect('par:buscar_participante')
    
    
    
class UsuarioEventoDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):    
# agregado para controlar acceso de usuario

    permission_required="eve.delete_usuario_evento"
    model = Usuario_Evento
    template_name="/eve/usuario_evento.html"       
    context_object_name = "obj"
    success_url = reverse_lazy("eve:usuario_evento")
    success_message="Acceso de usuario eliminado"
    
    

#@permission_required('bases.change_usuario', login_url='bases:login')
@login_required(login_url='config:login')
#@permission_required('eve.delete_usuario_evento', login_url='bases:login')
@permission_required('eve.delete_usuario_evento', login_url='bases:denegado')
#@permission_required('eve.delete_usuario_evento',raise_exception=True)
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
        

def lista_Eventos_Por_Acceso(pkUser,staff,tipo):
    if tipo=="O":
        if staff:
            lisEventos = Evento.objects.all().only('id','estado','nombre_evento')
            #lisEventos = ""         
        else:
                #filtra por relacion
            lisEventos = Evento.objects.filter(usuario_evento__usuario_id=pkUser).only('id','estado','nombre_evento')
                
           #lisEventos=list(Evento.objects.select_related("usuario_evento","modalidad_evento").filter(Q(usuario_evento__usuario_id=pkUser)).values("id",
           #         "nombre_evento","modalidad_evento__descripcion_modalidad_evento"))
    else:
        if staff:
                lisEventos=list(Evento.objects.select_related("usuario_evento","modalidad_evento").values("id",
                    "nombre_evento","modalidad_evento__descripcion_modalidad_evento"))
                 
        else:
                #filtra por relacion
                
                lisEventos=list(Evento.objects.select_related("usuario_evento","modalidad_evento").filter(Q(usuario_evento__usuario_id=pkUser)).values("id",
                    "nombre_evento","modalidad_evento__descripcion_modalidad_evento"))
        
        
                
    print(lisEventos)         
    return lisEventos;        
      


