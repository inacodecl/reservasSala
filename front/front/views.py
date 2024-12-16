from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.timezone import localdate, timedelta
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
from django.contrib import messages
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
#@csrf_exempt
#def agregar_usuario(request):
#    url = f"{NODE_API_URL}addUser"  # Cambia a la URL de tu API de producción
#    data = {
#        "correo": "ezapata@inacap.cl",
#        "nombre": "Eliaz",
#        "apellido": "zapata",
#        "pwd": "123456"
#    }
#
#    response = requests.post(url, json=data, headers=headers)
#
#    if response.status_code == 201:
#        return JsonResponse({"mensaje": "Usuario agregado correctamente"}, status=201)
#    else:
#        return JsonResponse({"mensaje": "Error al agregar usuario", "detalles": response.text}, status=400)


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

    


#@login_required
#@never_cache
#def users_dashboard(request):
    """
    Dashboard de usuarios que muestra el nombre del usuario y los proyectos filtrados (no en espera).
    """
    nombre_usuario = request.COOKIES.get('usuario_nombre')

    # Endpoint para obtener los proyectos
    api_url = f"{NODE_API_URL}proyectos"
    try:
        # Hacer la solicitud GET a la API
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            proyectos = response.json()  # Convertir la respuesta a JSON

            # Filtrar los proyectos cuyo estado no sea "en espera"
            proyectos = [proyecto for proyecto in proyectos if proyecto['estado'] != "en espera"]
        else:
            proyectos = []  # Si hay error, dejamos proyectos vacío
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {str(e)}")
        proyectos = []  # Si hay error de conexión, dejamos proyectos vacío

    # Renderizar la plantilla con el nombre del usuario y los proyectos filtrados
    return render(request, 'users.html', {
        'usuario': {'nombre': nombre_usuario},
        'proyectos': proyectos
    })

#@login_required
#@never_cache
#def users_dashboard(request):
    """
    Dashboard de usuarios que muestra el nombre del usuario y los proyectos filtrados
    (en espera y no en espera).
    """
    nombre_usuario = request.COOKIES.get('usuario_nombre')

    # Endpoint para obtener los proyectos
    api_url = f"{NODE_API_URL}proyectos"
    try:
        # Hacer la solicitud GET a la API
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            proyectos = response.json()  # Convertir la respuesta a JSON

            # Filtrar los proyectos en espera y los que no están en espera
            proyectos_en_espera = [proyecto for proyecto in proyectos if proyecto['estado'] == "en espera"]
            proyectos_no_en_espera = [proyecto for proyecto in proyectos if proyecto['estado'] != "denegado"and proyecto['estado'] != "en espera"]
        else:
            proyectos_en_espera = []
            proyectos_no_en_espera = []
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {str(e)}")
        proyectos_en_espera = []
        proyectos_no_en_espera = []

    # Renderizar la plantilla con las listas de proyectos
    return render(request, 'users.html', {
        'usuario': {'nombre': nombre_usuario},
        'proyectos_en_espera': proyectos_en_espera,
        'proyectos_no_en_espera': proyectos_no_en_espera
    })
#
@login_required
@never_cache
def users_dashboard(request):
    nombre_usuario = request.COOKIES.get('usuario_nombre')

    # Endpoint para obtener los proyectos
    api_url = f"{NODE_API_URL}proyectos"
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            proyectos = response.json()

            # Obtener IDs únicos de docentes y usuarios
            ids_docentes = {proyecto['id_docente'] for proyecto in proyectos if 'id_docente' in proyecto}
            ids_usuarios = {proyecto['id_usuario'] for proyecto in proyectos if 'id_usuario' in proyecto}

            # Obtener nombres de docentes y usuarios
            docentes = {}
            usuarios = {}
            if ids_docentes:
                docentes_response = requests.get(f"{NODE_API_URL}docentes", headers=headers)
                if docentes_response.status_code == 200:
                    docentes_data = docentes_response.json()
                    docentes = {docente['id']: docente['nombre'] for docente in docentes_data}

            if ids_usuarios:
                usuarios_response = requests.get(f"{NODE_API_URL}Users", headers=headers)
                if usuarios_response.status_code == 200:
                    usuarios_data = usuarios_response.json()
                    usuarios = {usuario['id']: usuario['nombre'] for usuario in usuarios_data}

            # Agregar nombres a los proyectos
            for proyecto in proyectos:
                proyecto['nombre_docente'] = docentes.get(proyecto.get('id_docente'))
                proyecto['nombre_usuario'] = usuarios.get(proyecto.get('id_usuario'))

            # Filtrar proyectos
            proyectos_en_espera = [proyecto for proyecto in proyectos if proyecto['estado'] == "en espera"]
            proyectos_no_en_espera = [proyecto for proyecto in proyectos if proyecto['estado'] != "denegado" and proyecto['estado'] != "en espera"]
        else:
            proyectos_en_espera = []
            proyectos_no_en_espera = []
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {str(e)}")
        proyectos_en_espera = []
        proyectos_no_en_espera = []

    return render(request, 'users.html', {
        'usuario': {'nombre': nombre_usuario},
        'proyectos_en_espera': proyectos_en_espera,
        'proyectos_no_en_espera': proyectos_no_en_espera,
    })


@login_required
@never_cache
def docente_dashboard(request):
    nombre_docente = request.COOKIES.get('docente_nombre')
    if not nombre_docente:
        return redirect('login') #redirigir al login si no hay cookie

    # URL de las APIS
    docentes_url=f"{NODE_API_URL}Docentes"
    proyectos_url= f"{NODE_API_URL}proyectos"

    try:
        response = requests.get(docentes_url, headers=headers)
        if response.status_code == 200:
            docentes = response.json()
            docente = next((d for d in docentes if d['nombre'].lower() == nombre_docente.lower()), None)
            if not docente:
                return render(request, "error.html", {"error": "Docente no encontrado en la base de datos."})
            id_docente = docente['id']
        else:
            return render(request, "error.html", {"error": "Error al obtener los datos de los docentes."})
    except requests.exceptions.RequestException as e:
        return render(request, "error.html", {"error": f"Error de conexión con la API: {str(e)}"})

    # Obtener los proyectos asignados al docente
    try:
        response = requests.get(proyectos_url, headers=headers)
        if response.status_code == 200:
            proyectos = response.json()
            # Filtrar proyectos por el ID del docente
            proyectos_filtrados = [proyecto for proyecto in proyectos if proyecto.get('id_docente') == id_docente]
        else:
            proyectos_filtrados = []
    except requests.exceptions.RequestException as e:
        return render(request, "error.html", {"error": f"Error al conectar con la API: {str(e)}"})

    # Renderizar la plantilla con los datos
    return render(request, 'docente.html', {
        'docente': {'nombre': nombre_docente},
        'proyectos': proyectos_filtrados,
    })

@login_required
@never_cache
def horario_general(request):
    proyectos_url = f"{NODE_API_URL}proyectos"

    try:
        # Obtener todos los proyectos desde la API
        response = requests.get(proyectos_url, headers=headers)
        if response.status_code == 200:
            proyectos = response.json()
        else:
            proyectos = []
    except requests.exceptions.RequestException as e:
        return render(request, "error.html", {"error": f"Error al conectar con la API: {str(e)}"})

    # Crear un calendario para la semana actual
    fecha_actual = localdate()
    fecha_inicio_semana = fecha_actual - timedelta(days=fecha_actual.weekday())  # Inicio de la semana (Lunes)
    dias_semana = [(fecha_inicio_semana + timedelta(days=i)) for i in range(5)]  # Lunes a Viernes

    # Preparar la estructura del calendario
    calendario = {dia.strftime('%A'): [] for dia in dias_semana}

    # Procesar los proyectos y agregar las reservas al calendario
    for proyecto in proyectos:
        dias_reserva = proyecto.get('diasReserva', {})
        for dia, detalle in dias_reserva.items():
            rango_horas = detalle.get('rango_horas', {})
            inicio_hora = rango_horas.get('inicio')
            fin_hora = rango_horas.get('fin')

            if inicio_hora and fin_hora:
                # Convertir nombres de días a español
                dia_espanol = {
                    "Monday": "Lunes",
                    "Tuesday": "Martes",
                    "Wednesday": "Miercoles",
                    "Thursday": "Jueves",
                    "Friday": "Viernes",
                }.get(dia, dia)

                if dia_espanol in calendario:
                    calendario[dia_espanol].append({
                        'proyecto': proyecto.get('nombre', 'Sin nombre'),
                        'inicio': inicio_hora,
                        'fin': fin_hora,
                        'estado': proyecto.get('estado', 'Desconocido'),
                        'integrantes': proyecto.get('integrantes', [])
                    })

    # Renderizar la plantilla con los datos
    return render(request, 'docente.html', {
        'calendario': calendario,
    })


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
        # Recuperar el nombre del usuario o docente desde las cookies
        nombre_docente = request.COOKIES.get("docente_nombre")
        nombre_usuario = request.COOKIES.get("usuario_nombre")

        if not (nombre_docente or nombre_usuario):
            return redirect('login')  # Si no hay ningún nombre, redirigir al login

        # Determinar si es un docente o un usuario
        es_docente = bool(nombre_docente)

        # Obtener el ID correspondiente desde la API
        api_url = f"{NODE_API_URL}docentes" if es_docente else f"{NODE_API_URL}Users"
        nombre_referencia = nombre_docente if es_docente else nombre_usuario

        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return render(request, "error.html", {"error": "Error al obtener los datos del usuario/docente."})

        datos = response.json()
        id_referencia = next((dato['id'] for dato in datos if dato['nombre'] == nombre_referencia), None)

        if not id_referencia:
            tipo = "docente" if es_docente else "usuario"
            return render(request, "error.html", {"error": f"No se encontró el ID del {tipo}."})

        # Obtener datos de la reserva
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
            "id_docente": id_referencia if es_docente else None,
            "id_usuario": id_referencia if not es_docente else None,
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
            return redirect("docente_dashboard" if es_docente else "users_dashboard")  # Redirige según el tipo de usuario
        else:
            return render(request, "error.html", {"error": response.text})

    return render(request, "login.html")



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
    



@csrf_exempt
@login_required
def mostrar_proyectos(request):
    """
    Obtiene los proyectos de la API y filtra aquellos que están en estado 'en espera'.
    """
    api_url = f"{NODE_API_URL}proyectos"
    try:
        response = requests.get(api_url, headers=HEADERS)
        if response.status_code == 200:
            proyectos = response.json()  # Datos en formato JSON
            # Filtrar proyectos con estado 'en espera'
            proyectos_en_espera = [
                proyecto for proyecto in proyectos if proyecto.get("estado") == "en espera"
            ]
            return render(request, "users.html", {"proyectos": proyectos_en_espera})
        else:
            # En caso de error en la API
            return render(
                request,
                "error.html",
                {"error": f"Error al obtener los proyectos: {response.status_code}"},
            )
    except requests.exceptions.RequestException as e:
        # En caso de error de conexión o de red
        return render(request, "error.html", {"error": f"Error al conectar con la API: {str(e)}"})


@login_required
def cambiar_estado_proyecto(request, proyecto_id, nuevo_estado):
    """
    Cambia el estado del proyecto (reservado, denegado, o terminado) y actualiza su autorización si aplica.
    """
    if nuevo_estado not in ["reservado", "denegado", "terminado"]:
        return JsonResponse({'mensaje': 'Estado no válido'}, status=400)

    # Determinar el endpoint y los datos a enviar según el nuevo estado
    if nuevo_estado == "reservado":
        url = f"{NODE_API_URL}habilitarproyecto/{proyecto_id}"
        data = {
            "estado": nuevo_estado,
            "autorizado": 1
        }
    elif nuevo_estado == "denegado":
        url = f"{NODE_API_URL}updateProyecto/{proyecto_id}"
        data = {
            "estado": nuevo_estado
        }
    elif nuevo_estado == "terminado":
        url = f"{NODE_API_URL}deshabilitarProyecto/{proyecto_id}"
        data = {
            "estado": "Terminado",
            "autorizado": 0
        }

    try:
        response = requests.put(url, json=data, headers=headers )
        if response.status_code == 200:
            return redirect("users_dashboard")
        else:
            return JsonResponse({'mensaje': 'Error al actualizar el proyecto'}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'mensaje': f'Error al conectar con la API: {str(e)}'}, status=500)


@login_required
def agregar_usuario(request):
    """
    Agrega un nuevo usuario o docente mediante la API y redirige al dashboard.
    """
    if request.method == "POST":
        # Obtener datos del formulario
        tipo = request.POST.get("tipo")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        pwd = request.POST.get("pwd")

        # Validar que los campos requeridos no estén vacíos
        if not nombre or not apellido or not correo or not pwd:
            return JsonResponse({"mensaje": "Todos los campos son obligatorios"}, status=400)

        # Crear la carga útil
        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "pwd": pwd,
        }

        # Determinar la URL según el tipo
        if tipo == "usuario":
            url = f"{NODE_API_URL}addUser"
        elif tipo == "docente":
            url = f"{NODE_API_URL}addDocentes"
        else:
            return JsonResponse({"mensaje": "Tipo inválido"}, status=400)

        try:
            # Enviar la solicitud a la API
            response = requests.post(url, json=datos, headers=headers)
            if response.status_code == 201:
                return redirect("users_dashboard")
            else:
                return JsonResponse(
                    {"mensaje": f"Error al agregar: {response.text}"},
                    status=response.status_code,
                )
        except requests.exceptions.RequestException as e:
            return JsonResponse({"mensaje": f"Error al conectar con la API: {str(e)}"}, status=500)   
    return render(request, "users.html")




#funciones de calendario que funciona
def obtener_calendario(request):
    """
    Genera un calendario semanal basado en los proyectos reservados.
    """
    try:
        # Hacer una solicitud al endpoint de Node.js para obtener los proyectos
        url = f"{NODE_API_URL}proyectos"  # Cambia la URL según corresponda
        response = requests.get(url,headers=headers)
        
        if response.status_code != 200:
            return JsonResponse({'error': 'No se pudieron obtener los proyectos'}, status=response.status_code)

        proyectos = response.json()
        calendario = generar_calendario(proyectos)
        return JsonResponse(calendario, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al conectar con el servidor: {str(e)}'}, status=500)

def generar_calendario(proyectos):
    """
    Crea un cronograma semanal basado en los proyectos y fechas dinámicas.
    """
    # Obtener el inicio de la semana (Lunes) basado en la fecha actual
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de esta semana

    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    calendario = []

    for i, dia in enumerate(dias):
        fecha_dia = inicio_semana + timedelta(days=i)
        fecha_formateada = fecha_dia.strftime('%d/%m')

        # Filtrar proyectos reservados para este día
        proyectos_dia = []
        for proyecto in proyectos:
            if proyecto['estado'] == 'Terminado' and 'diasReserva' in proyecto:
                if dia in proyecto['diasReserva']:
                    proyectos_dia.append({
                        'nombre': proyecto['nombre'],
                        'horario': proyecto['diasReserva'][dia]['rango_horas'],
                        'integrantes': proyecto['integrantes']
                    })

        # Añadir la información del día al calendario
        calendario.append({
            'dia': f"{dia} {fecha_formateada}",
            'proyectos': proyectos_dia
        })

    return calendario

# Calendario no funciona
@login_required
@never_cache
def calendario_view(request):
    # Realizar la solicitud a la API para obtener todos los proyectos
    url_proyectos = f"{NODE_API_URL}proyectos"
    response_proyectos = requests.get(url_proyectos, headers=headers)
    proyectos = response_proyectos.json() if response_proyectos.status_code == 200 else []

    # Obtener todos los docentes
    url_docentes = f"{NODE_API_URL}docentes"
    response_docentes = requests.get(url_docentes, headers=headers)
    docentes = response_docentes.json() if response_docentes.status_code == 200 else []

    # Crear un diccionario para buscar fácilmente los nombres de los docentes por ID
    docentes_dict = {docente["id"]: f"{docente['nombre']} {docente['apellido']}" for docente in docentes}

    # Filtrar proyectos pendientes y agregar el nombre del docente correspondiente
    proyectos_pendientes = [
        {
            **proyecto,
            "docente_nombre": docentes_dict.get(proyecto["id_docente"], "Desconocido"),
        }
        for proyecto in proyectos if proyecto.get("estado") == "pendiente"
    ]

    # Colores para diferenciar los proyectos en el calendario
    colores = ["bg-danger", "bg-primary", "bg-success", "bg-warning", "bg-info"]
    color_por_proyecto = {}

    # Generar intervalos de tiempo de 8:30 a 22:30 con una duración de 1.5 horas
    hora_actual = datetime.strptime("08:30", "%H:%M")
    hora_fin = datetime.strptime("22:30", "%H:%M")
    horarios = []

    while hora_actual <= hora_fin:
        fin_intervalo = hora_actual + timedelta(minutes=45)
        if fin_intervalo > hora_fin:
            fin_intervalo = hora_fin
        horario_reservado = []

        # Generar la estructura de reservas por día de la semana
        for dia in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
            reservas_dia = []
            for proyecto in proyectos:
                if proyecto.get("autorizado") != 1:
                    continue  # Solo mostrar proyectos autorizados
                
                # Asignar un color al proyecto si no tiene uno
                if proyecto["id"] not in color_por_proyecto:
                    color_por_proyecto[proyecto["id"]] = random.choice(colores)
                
                # Obtener la información de la reserva para cada día
                reserva_info = proyecto.get("diasReserva", {}).get(dia, {}).get("rango_horas", {})
                hora_inicio_str = reserva_info.get("inicio")
                hora_fin_str = reserva_info.get("fin")

                if hora_inicio_str and hora_fin_str:
                    hora_inicio_obj = datetime.strptime(hora_inicio_str.strip(), "%H:%M")
                    hora_fin_obj = datetime.strptime(hora_fin_str.strip(), "%H:%M")
                    if hora_inicio_obj <= hora_actual < hora_fin_obj:
                        reservas_dia.append({
                            "nombre": proyecto.get("nombre", "Reserva de Sala"),
                            "lugar": "Laboratorio InaCode",
                            "color": color_por_proyecto[proyecto["id"]],
                            "inicio": proyecto.get("inicio"),
                            "fin": proyecto.get("fin"),
                        })

            horario_reservado.append({
                "dia": dia,
                "reservas": reservas_dia
            })

        horarios.append({
            "inicio": hora_actual.strftime("%H:%M"),
            "fin": fin_intervalo.strftime("%H:%M"),
            "reservas_dia": horario_reservado
        })

        hora_actual += timedelta(minutes=90)

    # Renderizar todos los horarios con las reservas en el calendario
    return render(request, 'users_dashboard', {
        'horarios': horarios,
        'proyectos_pendientes': proyectos_pendientes,  # Enviar proyectos pendientes al contexto
    })
