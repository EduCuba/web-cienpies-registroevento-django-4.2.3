from django.urls import path
from django.contrib.auth import views as auth_views
from bases.views import *
from eve.views import ModalidadEventoList,ModalidadEventoAdd,ModalidadEventoEdit,ModalidadEventoDel,EventoList,EventoAdd,EventoEdit,EventoDel\
                      ,buscarusuarioevento,UsuarioEventoAdd,usuarioAccesoEvento
#app_name = 'eve'

urlpatterns = [
    
    path('eve/modalidad_evento_list', ModalidadEventoList.as_view(),name="modalidad_evento_list"),
    path('eve/modalidad_evento_add',ModalidadEventoAdd.as_view(),name="modalidad_evento_add"),
    path('eve/modalidad_evento_edit/<int:pk>',ModalidadEventoEdit.as_view(),name="modalidad_evento_edit"),
    path('eve/modalidad_evento_del/<int:pk>',ModalidadEventoDel.as_view(), name='modalidad_evento_del'),   
    
    path('eve/evento_list', EventoList.as_view(),name="evento_list"),
    path('eve/evento_add',EventoAdd.as_view(),name="evento_add"),
    path('eve/evento_edit/<int:pk>',EventoEdit.as_view(),name="evento_edit"),
    #path('eve/evento_del/<int:pk>',EventoDel.as_view(), name='evento_del'),   
    path('eve/evento_del/<int:pk>',EventoDel,name="evento_del"),
    
    
    
    
    path('eve/usuario_evento',buscarusuarioevento,name="usuario_evento"),
    path('eve/usuario_evento_add',UsuarioEventoAdd.as_view(),name="usuario_evento_add"),
    path('eve/usuario_evento_del',usuarioAccesoEvento, name='usuario_evento_del'),   
    
]