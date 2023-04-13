from django.urls import path
from django.contrib.auth import views as auth_views
from bases.views import *
from par.views import ParticipanteList,buscarparticipante,ParticipanteAdd,participanteAsistencia,ParticipanteEdit,DetailForm
#app_name = 'eve'

urlpatterns = [
    path('par/registro_list', ParticipanteList.as_view(),name="registro_list"),
    path('par/buscar_participante',buscarparticipante,name="buscar_participante"),
    path('par/participante_add',ParticipanteAdd.as_view(),name="participante_add"),
    path('par/asistencia_participante/<int:id>',participanteAsistencia, name="asistencia_participante"),
    path('par/asistencia_participante',participanteAsistencia, name="asistencia_participante"),
    path('participante_edit/<int:pk>',ParticipanteEdit.as_view(), name='participante_edit'),
    
    path('participante/new',ParticipanteAdd.as_view(), name='participante_new'),
    path('participante/newb',DetailForm, name='participante_newb'),
    
    
    #path('proveedores/edit/<int:pk>',ProveedorEdit.as_view(), name='proveedor_edit'),
    #path('par/burcar_participante/<int:evento>/<str:apellido_participante>/<str:nombre_participante>/<str:empresa_participante>',buscarparticipante,name="participantes_encontrados"),
         
   # path('eve/modalidad_evento_list', ModalidadEventoList.as_view(),name="modalidad_evento_list"),
   # path('eve/modalidad_evento_add',ModalidadEventoAdd.as_view(),name="modalidad_evento_add"),
   # path('eve/modalidad_evento_edit/<int:pk>',ModalidadEventoEdit.as_view(),name="modalidad_evento_edit"),
   # path('eve/modalidad_evento_del/<int:pk>',ModalidadEventoDel.as_view(), name='modalidad_evento_del'),   
    
   # path('eve/evento_list', EventoList.as_view(),name="evento_list"),
   # path('eve/evento_add',EventoAdd.as_view(),name="evento_add"),
   # path('eve/evento_edit/<int:pk>',EventoEdit.as_view(),name="evento_edit"),
   # path('eve/evento_del/<int:pk>',EventoDel.as_view(), name='evento_del'),   
    
  #  path('proveedores/new',ProveedorNew.as_view(), name='proveedor_new'),
    
    
]