from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#permisos para validar acceso de funciones
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *

from .models import Modalidad_Evento, Evento
from .forms import ModalidadEventoForm,EventoForm

from bases.views import SinPrivilegios

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