from django.contrib import admin
from django.urls import path
from appReservarSala import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('calendario', views.calendario_view, name='calendario'),
    path('logout', views.logout_view, name='logout'),
    path('autorizar_proyecto/<str:proyecto_id>/', views.autorizar_proyecto, name='autorizar_proyecto'),
    path('solicitar_reserva/', views.solicitar_reserva, name='solicitar_reserva'),
    path('obtener_docentes/', views.obtener_docentes, name='obtener_docentes'),    
    path('listar_proyectos/', views.listar_proyectos, name='listar_proyectos'),
    path('terminar_proyecto/<str:proyecto_id>/', views.terminar_proyecto, name='terminar_proyecto'),
    
    path('deshabilitar_proyecto/<str:proyecto_id>/', views.deshabilitar_proyecto, name='deshabilitar_proyecto'), 
    path('modificar_reserva/<str:proyecto_id>/', views.modificar_reserva, name='modificar_reserva'),
    path('habilitar_proyecto/<str:proyecto_id>/', views.habilitar_proyecto, name='habilitar_proyecto'),
    path('eliminar_integrante/<str:proyecto_id>/', views.eliminar_integrante, name='eliminar_integrante'),
    path('agregar_integrante/<str:proyecto_id>/', views.agregar_integrante, name='agregar_integrante'),
    path('rechazar_proyecto/<str:proyecto_id>/', views.rechazar_proyecto, name='rechazar_proyecto'),
]