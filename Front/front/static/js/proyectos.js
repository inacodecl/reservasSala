// Variables globales para las URLs
//const URL_LISTAR_PROYECTOS = document.getElementById('modalListaProyectos').dataset.urlListarProyectos;

// Manejar el evento de apertura del modal "Gestión de Reservas"
document.getElementById('modalGestionReservas').addEventListener('show.bs.modal', function () {
    // Aquí puedes realizar una solicitud para cargar las solicitudes de reserva pendientes si no están ya en el contexto
    fetch("{% url 'listar_reservas_pendientes' %}") // Endpoint para obtener las reservas pendientes
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#modalGestionReservas table tbody');
            tbody.innerHTML = ''; // Limpiar la tabla actual
            if (data.proyectos && data.proyectos.length > 0) {
                data.proyectos.forEach(proyecto => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${proyecto.autorizado_por}</td>
                        <td>${proyecto.nombre}</td>
                        <td>${proyecto.rut_docente}</td>
                        <td>${proyecto.inicio}</td>
                        <td>${proyecto.fin}</td>
                        <td>
                            <form onsubmit="autorizarProyecto(event, ${proyecto.id})">
                                <input type="hidden" name="proyecto_id" value="${proyecto.id}">
                                <button type="submit" class="btn btn-primary btn-sm">Autorizar</button>
                            </form>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            } else {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay proyectos pendientes.</td></tr>';
            }
        })
        .catch(error => console.error('Error al cargar reservas:', error));
});

// Agregar más integrantes dinámicamente en el modal de docentes
document.getElementById("btnAddIntegranteReserva").addEventListener("click", function() {
    const container = document.getElementById("integrantesContainerReserva");
    const div = document.createElement("div");
    div.classList.add("input-group", "mb-2", "integrante");
    div.innerHTML = `
        <input type="text" class="form-control" placeholder="Nombre del Integrante" name="nombreIntegrante[]">
        <input type="email" class="form-control" placeholder="Correo del Integrante" name="correoIntegrante[]">
        <button type="button" class="btn btn-danger btn-remove-integrante">Eliminar</button>
    `;
    container.appendChild(div);
    div.querySelector(".btn-remove-integrante").addEventListener("click", function() {
        div.remove();
    });
});

// Agregar más días de reserva dinámicamente en el modal de docentes
document.getElementById("btnAddDiaReservaDocente").addEventListener("click", function() {
    const container = document.getElementById("diasReservaContainerReserva");
    const div = document.createElement("div");
    div.classList.add("input-group", "mb-2", "dia-reserva");
    div.innerHTML = `
        <select class="form-select" name="diaReserva[]">
            <option selected>Seleccionar Día</option>
            <option value="Lunes">Lunes</option>
            <option value="Martes">Martes</option>
            <option value="Miercoles">Miércoles</option>
            <option value="Jueves">Jueves</option>
            <option value="Viernes">Viernes</option>
        </select>
        <input type="time" class="form-control" name="horaInicioReserva[]" placeholder="Hora de Inicio">
        <input type="time" class="form-control" name="horaFinReserva[]" placeholder="Hora de Fin">
        <button type="button" class="btn btn-danger btn-remove-dia">Eliminar</button>
    `;
    container.appendChild(div);
    div.querySelector(".btn-remove-dia").addEventListener("click", function() {
        div.remove();
    });
});

document.getElementById('modalSolicitarReservaDocente').addEventListener('show.bs.modal', function () {
    fetch(URL_OBTENER_DOCENTES)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById("docenteSelect");
            select.innerHTML = '';
            data.docentes.forEach(docente => {
                const option = document.createElement("option");
                option.value = docente.id;
                option.textContent = `${docente.nombre} ${docente.apellido}`;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error al cargar docentes:', error));
});

document.addEventListener('DOMContentLoaded', function () {
    const modalListaProyectos = document.getElementById('modalListaProyectos');
    
    if (modalListaProyectos) {
        modalListaProyectos.addEventListener('show.bs.modal', function () {
            fetch(URL_LISTAR_PROYECTOS, {
                headers: {
                    'Clave-De-Autenticacion': '[=kF!8QE`"&"YYQp$8,9W%n<&MCxjI;q'
                }
            })
                .then(response => response.json())
                .then(data => {
                    const listaProyectos = document.getElementById("listaProyectos");
                    listaProyectos.innerHTML = '';  // Limpiar lista existente
                    proyectosData = {};  // Resetear proyectosData para nuevas actualizaciones

                    if (data.proyectos && data.proyectos.length > 0) {
                        data.proyectos.forEach(proyecto => {
                            proyectosData[proyecto.id] = proyecto;  // Almacenar proyecto inicial

                            const card = document.createElement("div");
                            card.classList.add("col-md-4", "mb-3");

                            card.innerHTML = `
                                <div class="card h-100">
                                    <div class="card-body">
                                        <h5 class="card-title">
                                            <input type="text" class="form-control" name="nombre" value="${proyecto.nombre}" required 
                                                onchange="actualizarCampo('${proyecto.id}', 'nombre', this.value)">
                                        </h5>
                                        <p class="card-text"><strong>Inicio:</strong> 
                                            <input type="date" class="form-control" name="inicio" value="${proyecto.inicio}" required 
                                                onchange="actualizarCampo('${proyecto.id}', 'inicio', this.value)">
                                        </p>
                                        <p class="card-text"><strong>Fin:</strong> 
                                            <input type="date" class="form-control" name="fin" value="${proyecto.fin}" required 
                                                onchange="actualizarCampo('${proyecto.id}', 'fin', this.value)">
                                        </p>
                                        <p class="card-text"><strong>Estado:</strong> 
                                            <input type="text" class="form-control" name="estado" value="${proyecto.estado}" required 
                                                onchange="actualizarCampo('${proyecto.id}', 'estado', this.value)">
                                        </p>
                                        <p class="card-text"><strong>Autorizado:</strong> 
                                            <select name="autorizado" class="form-select" 
                                                onchange="actualizarCampo('${proyecto.id}', 'autorizado', this.value)">
                                                <option value="1" ${proyecto.autorizado ? 'selected' : ''}>Sí</option>
                                                <option value="0" ${!proyecto.autorizado ? 'selected' : ''}>No</option>
                                            </select>
                                        </p>
                                        <p class="card-text"><strong>Docente:</strong> ${proyecto.docente_nombre || 'Desconocido'}</p>

                                        <h6>Integrantes:</h6>
                                        <ul id="integrantes_${proyecto.id}">
                                            ${proyecto.integrantes.map((integrante, index) => `
                                                <li>
                                                    <input type="text" value="${integrante.nombre}" class="form-control mb-1" 
                                                        onchange="actualizarIntegrante('${proyecto.id}', ${index}, 'nombre', this.value)" />
                                                    <input type="email" value="${integrante.correo}" class="form-control mb-1" 
                                                        onchange="actualizarIntegrante('${proyecto.id}', ${index}, 'correo', this.value)" />
                                                    <button type="button" class="btn btn-danger btn-sm" onclick="eliminarIntegrante('${proyecto.id}', ${index})">Eliminar</button>
                                                </li>
                                            `).join('')}
                                        </ul>
                                        <button type="button" class="btn btn-secondary btn-sm" onclick="agregarIntegrante('${proyecto.id}')">Agregar Integrante</button>

                                        <h6>Días Reservados:</h6>
                                        <ul id="diasReserva_${proyecto.id}">
                                            ${Object.keys(proyecto.diasReserva).map(dia => {
                                                const horario = proyecto.diasReserva[dia].rango_horas;
                                                return `
                                                    <li>
                                                        <strong>${dia}:</strong> 
                                                        <input type="time" value="${horario.inicio.padStart(5, '0')}" class="form-control mb-1" 
                                                            onchange="actualizarDiaReserva('${proyecto.id}', '${dia}', 'inicio', this.value)">
                                                        <input type="time" value="${horario.fin.padStart(5, '0')}" class="form-control mb-1" 
                                                            onchange="actualizarDiaReserva('${proyecto.id}', '${dia}', 'fin', this.value)">
                                                        <button type="button" class="btn btn-danger btn-sm" onclick="eliminarDiaReserva('${proyecto.id}', '${dia}')">Eliminar</button>
                                                    </li>`;
                                            }).join('')}
                                        </ul>
                                        <button type="button" class="btn btn-secondary btn-sm" onclick="agregarDiaReserva('${proyecto.id}')">Agregar Día de Reserva</button>
                                    </div>
                                    <div class="card-footer">
                                        <button class="btn btn-primary btn-sm" onclick="guardarProyecto('${proyecto.id}')">Guardar Cambios</button>
                                        <button class="btn btn-danger btn-sm" onclick="terminarProyecto('${proyecto.id}')">Terminar</button>
                                    </div>
                                </div>
                            `;
                            listaProyectos.appendChild(card);
                        });
                    } else {
                        listaProyectos.innerHTML = '<div class="text-center">No hay proyectos disponibles.</div>';
                    }
                })
                .catch(error => console.error('Error al cargar proyectos:', error));
        });
    }
});

let proyectosData = {}; // Objeto global para almacenar datos de proyectos temporalmente

function actualizarCampo(proyectoId, campo, valor) {
    proyectosData[proyectoId] = proyectosData[proyectoId] || {};
    proyectosData[proyectoId][campo] = campo === "autorizado" ? parseInt(valor) : valor;
}

function guardarProyecto(proyectoId) {
    const data = proyectosData[proyectoId];
    fetch(`https://reservassala.inacode.cl/api/updateProyecto/${proyectoId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Clave-De-Autenticacion': '[=kF!8QE`"&"YYQp$8,9W%n<&MCxjI;q'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
        if (responseData.success) {
            alert("Proyecto guardado con éxito.");
            location.reload();
        } else {
            alert("Error al guardar el proyecto: " + (responseData.error || "Inténtalo de nuevo."));
        }
    })
    .catch(error => console.error('Error al guardar el proyecto:', error));
}

function terminarProyecto(proyectoId) {
    actualizarCampo(proyectoId, 'estado', "Terminado");
    actualizarCampo(proyectoId, 'autorizado', 0);
    guardarProyecto(proyectoId);
}

function agregarIntegrante(proyectoId) {
    const nombre = prompt("Nombre del integrante:");
    const correo = prompt("Correo del integrante:");
    
    if (nombre && correo) {
        // Asegurarse de que los datos del proyecto existan
        proyectosData[proyectoId] = proyectosData[proyectoId] || {};
        proyectosData[proyectoId].integrantes = proyectosData[proyectoId].integrantes || [];

        // Agregar el nuevo integrante al array de integrantes
        proyectosData[proyectoId].integrantes.push({ nombre, correo });

        // Actualizar la lista de integrantes en la UI
        const ul = document.getElementById(`integrantes_${proyectoId}`);
        const li = document.createElement("li");
        li.innerHTML = `
            <input type="text" value="${nombre}" class="form-control mb-1" 
                onchange="actualizarIntegrante('${proyectoId}', ${proyectosData[proyectoId].integrantes.length - 1}, 'nombre', this.value)" />
            <input type="email" value="${correo}" class="form-control mb-1" 
                onchange="actualizarIntegrante('${proyectoId}', ${proyectosData[proyectoId].integrantes.length - 1}, 'correo', this.value)" />
            <button type="button" class="btn btn-danger btn-sm" onclick="eliminarIntegrante('${proyectoId}', ${proyectosData[proyectoId].integrantes.length - 1})">Eliminar</button>
        `;
        ul.appendChild(li);
    } else {
        alert("Debe ingresar tanto el nombre como el correo del integrante.");
    }
}
function eliminarIntegrante(proyectoId, index) {
    proyectosData[proyectoId].integrantes.splice(index, 1);
    guardarProyecto(proyectoId); // Guarda el proyecto después de eliminar
}
function eliminarDiaReserva(proyectoId, dia) {
    delete proyectosData[proyectoId].diasReserva[dia];
    guardarProyecto(proyectoId);
}
function agregarDiaReserva(proyectoId) {
    const dia = prompt("Día de la reserva (Ej: Viernes):");
    const inicio = prompt("Hora de inicio (Ej: 08:30):");
    const fin = prompt("Hora de fin (Ej: 18:00):");
    if (dia && inicio && fin) {
        proyectosData[proyectoId] = proyectosData[proyectoId] || {};
        proyectosData[proyectoId].diasReserva = proyectosData[proyectoId].diasReserva || {};
        proyectosData[proyectoId].diasReserva[dia] = { rango_horas: { inicio, fin } };
        guardarProyecto(proyectoId);
    }
}
// Función para manejar la autorización de un proyecto
function autorizarProyecto(event, proyectoId) {
    event.preventDefault(); // Prevenir el envío por defecto del formulario
    fetch("{% url 'autorizar_proyecto' %}".replace('proyecto_id', proyectoId), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // CSRF para Django
        },
        body: JSON.stringify({ proyecto_id: proyectoId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Proyecto autorizado con éxito');
                document.getElementById('modalGestionReservas').dispatchEvent(new Event('show.bs.modal')); // Recargar datos del modal
            } else {
                alert('Error al autorizar el proyecto: ' + (data.error || 'Inténtalo nuevamente.'));
            }
        })
        .catch(error => console.error('Error al autorizar el proyecto:', error));
}