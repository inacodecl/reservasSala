"""
URL configuration for front project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,  include
from . import views

urlpatterns = [
    ## Ruta para la vista de inicio de sesión
    #path('usuario/', views.usuario_view, name='usuario'),  # Redirige a usuario.html
    #path('docente/', views.docente_view, name='docente'),  # Redirige a docente.html
    #path('', views.login_view, name='login_view'),  # Ruta de loginpath('read_users/', views.obtener_usuarios, name='obtener_usuario'),  # Leer usuarios
    path('update_users/<str:docente_id>/', views.update_usuario, name='update_usuario'),  # Actualizar usuario
    path('deleteusers/<str:docente_id>/', views.delete_usuario, name='delete_usuario'),  # Eliminar usuario
    path('create_docente/', views.agregar_docente, name='agregar_docente'),  # Crear docente
    path('read_docentes/', views.obtener_docentes, name='obtener_docentes'),  # Leer docentes
    path('update_docente/<str:docente_id>/', views.update_docente, name='update_docente'),  # Actualizar docente
    path('deleteDocente/<str:docente_id>/', views.delete_docente, name='delete_docente'),  # Eliminar docente
    path('create_proyecto/', views.agregar_proyecto, name='agregar_proyecto'),  # Crear proyecto
   # path('read_proyectos/', views.obtener_proyectos, name='obtener_proyecto'),  # Leer proyectos
    #path('update_proyecto/<str:proyecto_id>/', views.update_proyecto, name='update_proyecto'),  # Actualizar proyecto
    #path('deleteproyecto/<str:proyecto_id>/', views.delete_proyecto, name='delete_proyecto'),  # Eliminar proyecto
    path('', views.login_view, name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('users_dashboard/', views.users_dashboard, name='users_dashboard'),
    path('docente_dashboard/', views.docente_dashboard, name='docente_dashboard'),
    path('users_dashboard/obtener_proyectos/', views.obtener_proyectos, name='obtener_proyectos'),
    path('actualizar_reserva/<int:reserva_id>/', views.actualizar_reserva, name="actualizar_reserva"),
   # path('calendario/', views.calendario_view, name='calendario'),
    path("crear-reserva/", views.crear_reserva, name="crear_reserva"),
]
