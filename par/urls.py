from django.urls import path
from django.contrib.auth import views as auth_views
from bases.views import *
from par.views import ParticipanteList,buscarparticipante,ParticipanteAdd,participanteAsistencia,ParticipanteEdit,DetailForm,VistaParticipanteImportar,subir_csv,xx_ImportarCsv,contarasistencia
from par.views import TipoParticipanteList,TipoParticipanteAdd,TipoParticipanteEdit,TipoParticipanteDel,\
                      ModalidadAsistenciaAdd,ModalidadAsistenciaEdit,ModalidadAsistenciaDel,ModalidadAsistenciaList,\
                      ListarCsv,participante_csv_delete,TipoParticipanteDelete


#app_name = 'eve'
# path('par/registro_list', nombre dentro de la vista,name="nombre que se utilza en html")
urlpatterns = [
    path('par/registro_list', ParticipanteList.as_view(),name="registro_list"),
    path('par/buscar_participante',buscarparticipante,name="buscar_participante"),
    #path('par/buscar_participante',contarasistencia,name="contar_asistencia"),
    path('par/contar_asistencia',contarasistencia,name="contar_asistencia"),
    path('par/participante_add',ParticipanteAdd.as_view(),name="participante_add"),
    #path('par/participante_import_add',VistaParticipanteImportar.as_view(),name="participante_import_add"),
    path('par/participante_import_add',xx_ImportarCsv,name="participante_import_add"),
    
    path('par/participante_import_delete',ListarCsv,name="participante_import_delete"),
    path('par/participante_import_delete/<int:id>',participante_csv_delete,name="participante_import_delete"),
    
    
    path('par/subir_csv',subir_csv,name="subir_csv"),
    
    path('par/asistencia_participante/<int:id>',participanteAsistencia, name="asistencia_participante"),
    #path('par/asistencia_participante',participanteAsistencia, name="asistencia_participante"),
    path('par/participante_edit/<int:pk>',ParticipanteEdit.as_view(), name='participante_edit'),
    
    path('participante/new',ParticipanteAdd.as_view(), name='participante_new'),
    path('participante/newb',DetailForm, name='participante_newb'),
    
 
    path('par/tipo_participante_list', TipoParticipanteList.as_view(),name="tipo_participante_list"),
    path('par/tipo_participante_add',TipoParticipanteAdd.as_view(),name="tipo_participante_add"),
    path('par/tipo_participante_edit/<int:pk>',TipoParticipanteEdit.as_view(),name="tipo_participante_edit"),
    path('par/tipo_participante_delete/<int:pk>',TipoParticipanteDelete.as_view(), name='tipo_participante_delete'), 
    path('par/tipo_participante_del/<int:pk>',TipoParticipanteDel, name='tipo_participante_del'), 
     
    
    
    path('par/modalidad_asistencia_list', ModalidadAsistenciaList.as_view(),name="modalidad_asistencia_list"),
    path('par/modalidad_asistencia_add',ModalidadAsistenciaAdd.as_view(),name="modalidad_asistencia_add"),
    path('par/modalidad_asistencia_edit/<int:pk>',ModalidadAsistenciaEdit.as_view(),name="modalidad_asistencia_edit"),
    path('par/modalidad_asistencia_del/<int:pk>',ModalidadAsistenciaDel.as_view(), name='modalidad_asistencia_del'),  
 
    ##########path('sin_privilegios/',HomeSinPrivilegios.as_view(),name='sin_privilegios'),
    
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