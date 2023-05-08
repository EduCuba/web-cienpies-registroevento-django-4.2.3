from django.urls import path
from django.contrib.auth import views as auth_views
from bases.views import *

#from django.conf.urls import include
app_name = 'config'

urlpatterns = [
    
    path('',Home.as_view(), name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='bases/login.html'), 
       name='login'),
    path('logout/',
       auth_views.LogoutView.as_view(template_name='bases/login.html'), 
       name='logout'),
    path('sin_privilegios/',
       HomeSinPrivilegios.as_view(), 
       name='sin_privilegios'),
    
    
    #path("accounts/", include("django.contrib.auth.urls")),
  
    
    
    path('users/lists',UserList.as_view(),name="users_list"),
    path('users/add',user_admin,name="user_add"),
    path('users/modify/<int:pk>',user_admin,name="user_modify"),
    path('users/groups/list',UserGroupList.as_view(),name="user_groups_list"),
    path('users/groups/add',user_groups_admin,name="user_groups_new"),
    path('users/groups/modify/<int:pk>',user_groups_admin,name="user_groups_modify"),
    path('users/groups/delete/<int:pk>',user_group_delete,name="user_groups_delete"),
    
    path('users/groups/permission/<int:id_grp>/<int:id_perm>',user_group_permission,name="user_groups_permission"),
    path('users/groups/admin/<int:id_usr>/<int:id_grp>',user_group_add, \
        name="user_groups_admin"),
        
 
    
]
