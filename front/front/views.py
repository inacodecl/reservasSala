from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import decorator_from_middleware
from django.utils.cache import add_never_cache_headers
from django.views.decorators.cache import never_cache
from datetime import datetime, timedelta
import random
import locale
import calendar
import requests
import os
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
# Cargar clave de autenticación desde variables de entorno
AUTHENTICATION_KEY = '[=kF!8QE`"&"YYQp$8,9W%n<&MCxjI;q'
NODE_API_URL = os.getenv('NODE_API_URL', 'https://reservassala.inacode.cl/api/')
headers = {
    "Clave-De-Autenticacion": AUTHENTICATION_KEY
}
class DisableCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response

# ------------------------- Usuarios -------------------------

# Vista para agregar un usuario
@csrf_exempt
def agregar_usuario(request):
    url = f"{NODE_API_URL}addUser"  # Cambia a la URL de tu API de producción
    data = {
        "correo": "ezapata@inacap.cl",
        "nombre": "Eliaz",
        "apellido": "zapata",
        "pwd": "123456"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return JsonResponse({"mensaje": "Usuario agregado correctamente"}, status=201)
    else:
        return JsonResponse({"mensaje": "Error al agregar usuario", "detalles": response.text}, status=400)


# Vista para obtener todos los usuarios
@csrf_exempt
def obtener_usuarios(request):
    url = f"{NODE_API_URL}Users"  # Cambia a la URL de tu API de producción
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        usuarios = response.json()
        return JsonResponse({"usuarios": usuarios}, status=200)
    else:
        return JsonResponse({"mensaje": "Error al obtener usuarios", "detalles": response.text}, status=400)


# Vista para actualizar un usuario
@csrf_exempt
def update_usuario(request, user_id):
    url = f"{NODE_API_URL}updateUser/{user_id}"  # URL para actualizar el usuario específico

    data = {
        "id": user_id,
        "correo": "ezapata@inacap.cl",
        "nombre": "Eliaz",
        "apellido": "zapata",
        "pwd": "123456"
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        return JsonResponse({"mensaje": "Usuario actualizado correctamente"}, status=200)
    else:
        return JsonResponse({"mensaje": "Error al actualizar usuario", "detalles": response.text}, status=400)


# Vista para eliminar un usuario
@csrf_exempt
def delete_usuario(request, user_id):
    url = f"{NODE_API_URL}deleteUser/{user_id}"  # URL para eliminar el usuario específico
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse({"mensaje": "Usuario eliminado correctamente"}, status=200)
    else:
        return JsonResponse({"mensaje": "Error al eliminar usuario", "detalles": response.text}, status=400)


# ------------------------- Docentes -------------------------

# Vista para agregar un docente
@csrf_exempt
def agregar_docente(request):
    url = f"{NODE_API_URL}addDocentes"  # Cambia a la URL de tu API de producción
    data = {
        "nombre": "TEST1",
        "apellido": "TEST1",
        "correo": "TEST1@inacapmail.cl",
        "pwd": "123456",
        "status": 1
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return JsonResponse({"mensaje": "Docente agregado correctamente"}, status=201)
    else:
        return JsonResponse({"mensaje": "Error al agregar docente", "detalles": response.text}, status=400)


# Vista para obtener todos los docentes
@csrf_exempt
def obtener_docentes(request):
    url = f"{NODE_API_URL}docentes"  # Cambia a la URL de tu API de producción
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        docentes = response.json()
        return JsonResponse({"docentes": docentes}, status=200)
    else:
        return JsonResponse({"mensaje": "Error al obtener docentes", "detalles": response.text}, status=400)


# Vista para actualizar un docente
@csrf_exempt
def update_docente(request, docente_id):
    url = f"{NODE_API_URL}updateDocente/{docente_id}"  # URL para actualizar el docente específico
    data = {
        "id": docente_id,
        "nombre": "Paulo",
        "apellido": "Taipe",
        "correo": "paulo.taipe@inacapmail.cl",
        "pwd": "123456",
        "status": 1
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        return JsonResponse({"mensaje": "Docente actualizado correctamente"}, status=200)
    else:
        return JsonResponse({"mensaje": "Error al actualizar docente", "detalles": response.text}, status=400)


# Vista para eliminar un docente
@csrf_exempt
def delete_docente(request, docente_id):
    url = f"{NODE_API_URL}deleteDocente/{docente_id}"  # URL para eliminar el docente específico
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse({"mensaje": "Docente eliminado correctamente"}, status=200)
    else:
        return JsonResponse({"mensaje": "Error al eliminar docente", "detalles": response.text}, status=400)


# ------------------------- Proyectos -------------------------

# Vista para agregar un proyecto
@csrf_exempt
def agregar_proyecto(request):
    url = f"{NODE_API_URL}addProyecto"  # Cambia a la URL de tu API de producción
    data = {
        "id_docente": "INwqScv25D2mDguGV0XF",
        "inicio": "2024-11-01",
        "fin": "2024-11-30",
        "nombre": "MiCancha",
        "integrantes": [
            {
                "nombre": "Gerard Vazquez",
                "correo": "gv@inacapmail.cl"
            }
        ],
        "diasReserva": {
            "Viernes": {
                "rango_horas": {
                    "inicio": "08:30",
                    "fin": "12:30"
                }
            }
        },
        "autorizado": 0,
        "autorizadoPor": "",
        "estado": ""
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return JsonResponse({"mensaje": "Proyecto agregado correctamente"}, status=201)
    else:
        return JsonResponse({"mensaje": "Error al agregar proyecto", "detalles": response.text}, status=400)


# Vista para obtener todos los proyectos
@csrf_exempt
def obtener_proyectos(request):
    url = f"{NODE_API_URL}proyectos"  # Cambia a la URL de tu API de producción
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        proyectos = response.json()
        return JsonResponse({"proyectos": proyectos}, status=200)
    else:
        return JsonResponse({"mensaje": "Error al obtener proyectos", "detalles": response.text}, status=400)
    


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        tipo_usuario = request.COOKIES.get('tipo_usuario')

        # Verificar si el tipo de usuario es válido y la cookie correspondiente existe
        if tipo_usuario == 'user':
            if not request.COOKIES.get('usuario_nombre'):
                return redirect('login')
        elif tipo_usuario == 'docente':
            if not request.COOKIES.get('docente_nombre'):
                return redirect('login')
        else:
            # Redirigir al login si el tipo de usuario es inválido o no está autenticado
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return wrapper


# Middleware para deshabilitar caché (prevenir retroceder a páginas protegidas tras logout)
class DisableCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        return response

# Vista de login
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        pwd = request.POST.get('pwd')

        # Verificar usuarios en la colección "Users"
        user_url = f"{NODE_API_URL}Users"
        user_response = requests.get(user_url, headers=headers)

        # Verificar usuarios en la colección "docentes"
        docente_url = f"{NODE_API_URL}docentes"
        docente_response = requests.get(docente_url, headers=headers)

        if user_response.status_code == 200 and docente_response.status_code == 200:
            usuarios = user_response.json()
            docentes = docente_response.json()

            # Buscar en la colección "Users"
            usuario_valido = next((u for u in usuarios if u['correo'] == correo and u['pwd'] == pwd), None)
            if usuario_valido:
                response = redirect('users_dashboard')
                response.set_cookie('usuario_nombre', usuario_valido['nombre'], httponly=True)
                response.set_cookie('tipo_usuario', 'user', httponly=True)
                return response

            # Buscar en la colección "docentes"
            docente_valido = next((d for d in docentes if d['correo'] == correo and d['pwd'] == pwd), None)
            if docente_valido:
                response = redirect('docente_dashboard')
                response.set_cookie('docente_nombre', docente_valido['nombre'], httponly=True)
                response.set_cookie('tipo_usuario', 'docente', httponly=True)
                return response

        # Si no encuentra credenciales válidas
        return render(request, 'login.html', {'error': 'Credenciales incorrectas'})

    # Si es GET, renderiza la página de login
    return render(request, 'login.html')


@login_required
@never_cache
def users_dashboard(request):
    nombre_usuario = request.COOKIES.get('usuario_nombre')
    return render(request, 'users.html', {'usuario': {'nombre': nombre_usuario}})

@login_required
@never_cache
def docente_dashboard(request):
    nombre_docente = request.COOKIES.get('docente_nombre')
    return render(request, 'docente.html', {'docente': {'nombre': nombre_docente}})


def cerrar_sesion(request):
    response = redirect('login')
    response.delete_cookie('usuario_nombre')
    response.delete_cookie('docente_nombre')
    response.delete_cookie('tipo_usuario')
    request.session.flush()
    return response


@login_required
def crear_reserva(request):
    if request.method == "POST":
        # Recuperar el nombre del docente desde las cookies
        nombre_docente = request.COOKIES.get("docente_nombre")  
        if not nombre_docente:
            return redirect('login')  # Si no hay nombre, redirigir al login

        nombre = request.POST.get("nombre")
        inicio = request.POST.get("inicio")
        fin = request.POST.get("fin")

        # Obtener integrantes
        integrantes = []
        integrantes_data = request.POST.getlist("integrantes[][nombre]")
        correos_data = request.POST.getlist("integrantes[][correo]")
        for integrante_nombre, correo in zip(integrantes_data, correos_data):
            integrantes.append({"nombre": integrante_nombre, "correo": correo})

        # Obtener días reservados
        diasReserva = {}
        dias_data = request.POST.getlist("diasReserva[][dia]")
        rangos_inicio = request.POST.getlist("diasReserva[][rango_inicio]")
        rangos_fin = request.POST.getlist("diasReserva[][rango_fin]")
        for dia, rango_inicio, rango_fin in zip(dias_data, rangos_inicio, rangos_fin):
            diasReserva[dia] = {"rango_horas": {"inicio": rango_inicio, "fin": rango_fin}}

        # Crear el JSON para la solicitud
        reserva_data = {
            "nombre_docente": nombre_docente,  # Usar el nombre del docente
            "inicio": inicio,
            "fin": fin,
            "nombre": nombre,
            "integrantes": integrantes,
            "diasReserva": diasReserva,
            "autorizado": 0,
            "autorizadoPor": "",
            "estado": "en espera",
        }

        # Hacer la solicitud POST a la API
        api_url = f"{NODE_API_URL}addProyecto"
        response = requests.post(api_url, headers=headers, json=reserva_data)

        if response.status_code == 201:
            return redirect("docente_dashboard")  # Redirige a una página de éxito
        else:
            return render(request, "error.html", {"error": response.text})

    return render(request, "login.html")



@login_required
def actualizar_reserva(request, reserva_id):
    if request.method == "POST":
        # Obtener el nuevo estado (aceptada o rechazada)
        nuevo_estado = request.POST.get("estado")

        # Comprobar que el nuevo estado es válido
        if nuevo_estado not in ["aceptada", "rechazada"]:
            return JsonResponse({"error": "Estado no válido"}, status=400)

        # Realizar la solicitud PUT a la API para actualizar la reserva
        api_url = f"{NODE_API_URL}updateProyecto/{reserva_id}"
        data = {
            "estado": nuevo_estado,
        }
        response = requests.put(api_url, json=data, headers=headers)

        if response.status_code == 200:
            return JsonResponse({"message": "Reserva actualizada correctamente"}, status=200)
        else:
            return JsonResponse({"error": "Error al actualizar la reserva"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)