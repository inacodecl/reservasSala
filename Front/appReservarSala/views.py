import requests
from datetime import datetime, timedelta
from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json

headers = {
        'Clave-De-Autenticacion': '[=kF!8QE`"&"YYQp$8,9W%n<&MCxjI;q'
    }

def logout_view(request):
    request.session.flush()  # Elimina todos los datos de sesión
    return redirect('login')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        # Verifica en la colección de Usuarios
        user_response = requests.get('https://reservassala.inacode.cl/api/Users', headers=headers)
        users = user_response.json()

        # Itera sobre cada usuario en la respuesta JSON
        for user in users:
            if user["correo"] == email and user["pwd"] == password:
                # Guardar información del usuario en la sesión
                request.session['user_name'] = f"{user['nombre']} {user['apellido']}"
                request.session['user_type'] = 'usuario'
                request.session['usuario_id'] = user["id"]  # Almacena el ID del usuario
                return redirect('calendario')

        # Si no es Usuario, verifica en la colección de Docentes
        docente_response = requests.get('https://reservassala.inacode.cl/api/docentes', headers=headers)
        docentes = docente_response.json()
        
        for docente in docentes:
            if docente["correo"] == email and docente["pwd"] == password:
                # Guardar información del docente en la sesión
                request.session['user_name'] = f"{docente['nombre']} {docente['apellido']}"
                request.session['user_type'] = 'docente'
                request.session['docente_id'] = docente["id"]  # Almacena el ID del docente
                return redirect('calendario')

        error_message = "Correo o contraseña incorrectos. Inténtalo nuevamente."
        return render(request, 'myapp/login.html', {'error_message': error_message})

    return render(request, 'myapp/login.html')



def calendario_view(request):
    # Realizar la solicitud a la API para obtener todos los proyectos
    url_proyectos = "https://reservassala.inacode.cl/api/proyectos"
    response_proyectos = requests.get(url_proyectos, headers=headers)
    proyectos = response_proyectos.json() if response_proyectos.status_code == 200 else []

    # Obtener todos los docentes
    url_docentes = "https://reservassala.inacode.cl/api/docentes"
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
        for dia in ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]:
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
    return render(request, 'myapp/admin.html', {
        'horarios': horarios,
        'proyectos_pendientes': proyectos_pendientes,  # Enviar proyectos pendientes al contexto
    })

@require_POST
def rechazar_proyecto(request, proyecto_id):
    docente_id = request.session.get('docente_id')
    if not docente_id:
        return JsonResponse({"error": "No se pudo identificar al docente"}, status=403)

    url = f"https://reservassala.inacode.cl/api/updateProyecto/{proyecto_id}"
    data = {
        "autorizado": 0,  # Asegurar que no está autorizado
        "estado": "rechazado",  # Cambiar el estado a rechazado
        "autorizadoPor": docente_id,  # Guardar quién rechazó el proyecto
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        messages.success(request, "Proyecto rechazado con éxito.")
    else:
        messages.error(request, "Error al rechazar el proyecto. Intenta de nuevo.")

    return redirect('calendario')


@require_POST
def autorizar_proyecto(request, proyecto_id):
    # Obtener el ID del usuario administrador desde la sesión
    admin_name = request.session.get('user_name')
    if not admin_name:
        return JsonResponse({"error": "No se pudo identificar al administrador"}, status=403)

    # Obtener el proyecto desde la API
    proyecto_url = f"https://reservassala.inacode.cl/api/proyectos/{proyecto_id}"
    proyecto_response = requests.get(proyecto_url, headers=headers)
    
    if proyecto_response.status_code != 200:
        return JsonResponse({"error": "No se pudo obtener el proyecto"}, status=404)

    proyecto = proyecto_response.json()
    id_docente = proyecto.get('id_docente')

    # Obtener la lista de docentes desde la API
    docente_url = f"https://reservassala.inacode.cl/api/docentes"
    docente_response = requests.get(docente_url, headers=headers)

    if docente_response.status_code != 200:
        return JsonResponse({"error": "No se pudo obtener la colección de docentes"}, status=404)

    docentes = docente_response.json()

    # Buscar el docente correspondiente al ID del proyecto
    docente_encontrado = next((docente for docente in docentes if docente["id"] == id_docente), None)
    if not docente_encontrado:
        return JsonResponse({"error": "El docente asociado al proyecto no se encontró en la colección de docentes"}, status=404)

    # Actualizar el proyecto con los datos de autorización
    url_update = f"https://reservassala.inacode.cl/api/updateProyecto/{proyecto_id}"
    data = {
        "autorizado": 1,
        "estado": "reservado",
        "autorizadoPor": admin_name,  # Nombre del administrador
    }

    response = requests.put(url_update, headers=headers, json=data)

    if response.status_code == 200:
        messages.success(request, f"Proyecto autorizado con éxito por {admin_name}.")
    else:
        messages.error(request, "Error al autorizar el proyecto. Intenta de nuevo.")

    return redirect('calendario')



@csrf_exempt
def solicitar_reserva(request):
    if request.method == "POST":
        id_docente = request.session.get("docente_id")
        if not id_docente:
            return JsonResponse({"error": "No se pudo identificar al docente"}, status=403)

        nombre_proyecto = request.POST.get("nombreProyectoReserva")
        fecha_inicio = request.POST.get("fechaInicioReserva")
        fecha_fin = request.POST.get("fechaFinReserva")

        integrantes = [
            {"nombre": nombre, "correo": correo}
            for nombre, correo in zip(request.POST.getlist("nombreIntegrante[]"), request.POST.getlist("correoIntegrante[]"))
        ]
        
        dias_reserva = {
            dia: {"rango_horas": {"inicio": inicio, "fin": fin}}
            for dia, inicio, fin in zip(request.POST.getlist("diaReserva[]"), request.POST.getlist("horaInicioReserva[]"), request.POST.getlist("horaFinReserva[]"))
        }

        data = {
            "id_docente": id_docente,  # Usa el ID del docente de sesión
            "inicio": fecha_inicio,
            "fin": fecha_fin,
            "nombre": nombre_proyecto,
            "integrantes": integrantes,
            "diasReserva": dias_reserva,
            "estado": "pendiente",
            "autorizado": 0,
            "autorizadoPor": None
        }
        
        response = requests.post("https://reservassala.inacode.cl/api/addProyecto", headers=headers, json=data)
        
        if response.status_code == 201:
            return redirect('calendario')
        else:
            return JsonResponse({"error": "No se pudo enviar la solicitud"}, status=500)
    
def obtener_docentes(request):    
    url = "https://reservassala.inacode.cl/api/docentes"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        docentes = response.json()
        if isinstance(docentes, list) and all("id" in d and "nombre" in d and "apellido" in d for d in docentes):
            return JsonResponse({"docentes": docentes})
        else:
            return JsonResponse({"error": "Datos de docentes no válidos"}, status=500)
    else:
        return JsonResponse({"error": "No se pudieron obtener los docentes"}, status=500)

def listar_proyectos(request):
    docente_id = request.session.get('docente_id')
    if not docente_id:
        return JsonResponse({"error": "No se pudo identificar al docente"}, status=403)

    proyectos_url = "https://reservassala.inacode.cl/api/proyectos"
    response = requests.get(proyectos_url, headers=headers)
    
    if response.status_code == 200:
        proyectos = response.json()
        # Incluye el nombre del docente en cada proyecto filtrado
        proyectos_filtrados = [
            {
                **proyecto,
                "docente_nombre": f"{request.session['user_name']}"
            } 
            for proyecto in proyectos if proyecto.get("id_docente") == docente_id
        ]
        return JsonResponse({"proyectos": proyectos_filtrados})
    else:
        return JsonResponse({"error": "No se pudieron obtener los proyectos"}, status=500)


@csrf_exempt
def terminar_proyecto(request, proyecto_id):
    if request.method == "PUT":
        data = {
            "autorizado": 0,
            "estado": "Terminado"
        }
        
        url = f"https://reservassala.inacode.cl/api/updateProyecto/{proyecto_id}"
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return JsonResponse({"success": "Proyecto terminado con éxito"})
        else:
            return JsonResponse({"error": "No se pudo terminar el proyecto"}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def habilitar_proyecto(request, proyecto_id):
    if request.method == 'PUT':
        headers = {
            'Clave-De-Autenticacion': '[=kF!8QE`"&"YYQp$8,9W%n<&MCxjI;q'
        }
        url = f"https://reservassala.inacode.cl/api/habilitarproyecto/{proyecto_id}/"
        data = {
            "autorizado": 1,
            "estado": "reservado"
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            return JsonResponse({"success": "Proyecto habilitado con éxito"})
        else:
            return JsonResponse({"error": "No se pudo habilitar el proyecto"}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def deshabilitar_proyecto(request, proyecto_id):
    url = f"https://reservassala.inacode.cl/api/proyectos/proyectos_update/{proyecto_id}/"
    data = {
        "autorizado": 0,
        "estado": "Terminado"
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        return JsonResponse({"success": "Proyecto terminado correctamente"})
    return JsonResponse({"error": "Error al terminar el proyecto"}, status=500)

@csrf_exempt
def agregar_integrante(request, proyecto_id):
    if request.method == 'POST':
        try:
            # Verificar la existencia del proyecto
            url_proyecto = f"https://reservassala.inacode.cl/api/proyectos/{proyecto_id}"
            url_update = f"https://reservassala.inacode.cl/api/updateProyecto/{proyecto_id}"
            proyecto_response = requests.get(url_proyecto, headers=headers)
            
            if proyecto_response.status_code != 200:
                return JsonResponse({"error": "No se pudo obtener el proyecto"}, status=proyecto_response.status_code)
            
            proyecto = proyecto_response.json()

            # Agregar el nuevo integrante
            data = json.loads(request.body)
            nuevo_integrante = {"nombre": data.get("nombre"), "correo": data.get("correo")}
            
            # Verificar que los datos del integrante están completos
            if not nuevo_integrante["nombre"] or not nuevo_integrante["correo"]:
                return JsonResponse({"error": "Nombre y correo del integrante son requeridos"}, status=400)

            proyecto["integrantes"].append(nuevo_integrante)

            # Enviar el proyecto actualizado a la API
            response = requests.put(url_update, headers=headers, json=proyecto)

            if response.status_code == 200:
                return JsonResponse({"success": "Integrante agregado con éxito"})
            else:
                return JsonResponse({"error": "No se pudo agregar el integrante", "detalles": response.json()}, status=response.status_code)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato de los datos JSON"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def eliminar_integrante(request, proyecto_id):
    if request.method == 'PUT':  # Usamos PUT para simular un update
        try:
            # Verificar la existencia del proyecto
            url_proyecto = f"https://reservassala.inacode.cl/api/proyectos/{proyecto_id}"
            url_update = f"https://reservassala.inacode.cl/api/updateProyecto/{proyecto_id}"
            proyecto_response = requests.get(url_proyecto, headers=headers)
            
            if proyecto_response.status_code != 200:
                return JsonResponse({"error": "No se pudo obtener el proyecto"}, status=proyecto_response.status_code)
            
            proyecto = proyecto_response.json()

            # Extraer el correo del integrante a eliminar del cuerpo de la solicitud
            data = json.loads(request.body)
            correo = data.get("correo")

            # Verificar que el correo fue proporcionado
            if not correo:
                return JsonResponse({"error": "Correo de integrante no proporcionado"}, status=400)

            # Filtrar la lista de integrantes para excluir el integrante con el correo proporcionado
            proyecto["integrantes"] = [i for i in proyecto["integrantes"] if i["correo"] != correo]

            # Actualizar el proyecto en la API con la lista de integrantes modificada
            response = requests.put(url_update, headers=headers, json=proyecto)

            if response.status_code == 200:
                return JsonResponse({"success": "Integrante eliminado con éxito"})
            else:
                return JsonResponse({"error": "No se pudo eliminar el integrante", "detalles": response.json()}, status=response.status_code)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato de los datos JSON"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def modificar_reserva(request, proyecto_id):
    if request.method == 'PUT':
        try:
            # Verificar la existencia del proyecto
            url_proyecto = f"https://reservassala.inacode.cl/api/proyectos/{proyecto_id}"
            url_update = f"https://reservassala.inacode.cl/api/updateProyecto/{proyecto_id}"
            proyecto_response = requests.get(url_proyecto, headers=headers)

            if proyecto_response.status_code != 200:
                return JsonResponse({"error": "No se pudo obtener el proyecto"}, status=proyecto_response.status_code)
            
            proyecto = proyecto_response.json()
            data = json.loads(request.body)
            dias_reserva_nuevo = data.get("diasReserva")
            
            if dias_reserva_nuevo and isinstance(dias_reserva_nuevo, dict):
                if "diasReserva" not in proyecto:
                    proyecto["diasReserva"] = {}
                
                # Actualizar o añadir los días específicos dentro de `diasReserva`
                for dia, horario in dias_reserva_nuevo.items():
                    if isinstance(horario, dict) and "rango_horas" in horario:
                        proyecto["diasReserva"][dia] = horario
                    else:
                        return JsonResponse({"error": f"Formato inválido para el día {dia}"}, status=400)

                # Confirmar que `diasReserva` está en el objeto `proyecto` y enviarlo a la API
                response = requests.put(url_update, headers=headers, json=proyecto)

                if response.status_code == 200:
                    return JsonResponse({"success": "Reserva modificada correctamente"})
                else:
                    return JsonResponse({"error": "Error al modificar la reserva", "detalles": response.json()}, status=response.status_code)
            else:
                return JsonResponse({"error": "Datos de reserva incompletos o inválidos"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato de los datos JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

