// Referencias a los botones y las secciones
        const btnNoEnEspera = document.getElementById("lista_proyectos_no_en_espera");
        const btnEnEspera = document.getElementById("lista_proyectos_en_espera");
        const btnAgregarUsuario = document.getElementById("AgregarUsuario");
        const btncrearreserva=document.getElementById("mostrarFormulario");
        const btncalendario=document.getElementById("btn-calendario");
        const proyectosNoEnEspera = document.getElementById("proyectos_no_en_espera");
        const proyectosEnEspera = document.getElementById("proyectos_en_espera");
        const seccionAgregarUsuario = document.getElementById("agregar_usuario");
        const seccionCrearReserva= document.getElementById("solicitar");
        const seccionCalendario= document.getElementById("calendario-semanal")
        // Función para ocultar todas las secciones
        function hideAllSections() {
            proyectosNoEnEspera.style.display = "none";
            proyectosEnEspera.style.display = "none";
            seccionAgregarUsuario.style.display = "none";
            seccionCrearReserva.style.display = "none";
            seccionCalendario.style.display="none";
        }
        
        // Función para mostrar una sección específica
        function showSection(section) {
            hideAllSections(); // Ocultar todas las secciones antes de mostrar la seleccionada
            section.style.display = "block";
            section.scrollIntoView({ behavior: "smooth" }); // Desplazar hacia la sección visible
        }
        
        // Event listeners para alternar entre secciones
        btnNoEnEspera.addEventListener("click", function (event) {
            event.preventDefault();
            showSection(proyectosNoEnEspera);
        });
        
        btnEnEspera.addEventListener("click", function (event) {
            event.preventDefault();
            showSection(proyectosEnEspera);
        });
        
        btnAgregarUsuario.addEventListener("click", function (event) {
            event.preventDefault();
            showSection(seccionAgregarUsuario);
        });

        btncrearreserva.addEventListener("click",function(event){
            event.preventDefault(); 
            showSection(seccionCrearReserva);
        }); 
        btncalendario.addEventListener("click", function(event){
            event.preventDefault();
            showSection(seccionCalendario)
        });

        // Reutilizando funciones de agregar integrantes y días
        function agregarIntegrante() {
            const container = document.getElementById("integrantes-container");
            const integrante = document.createElement("div");
            integrante.classList.add("integrante", "mb-2");
            integrante.innerHTML = `
                <input type="text" name="integrantes[][nombre]" placeholder="Nombre" class="form-control mb-1" required>
                <input type="email" name="integrantes[][correo]" placeholder="Correo" class="form-control" required>
            `;
            container.appendChild(integrante);
        }
    
        function agregarDia() {
            const container = document.getElementById("dias-container");
            const dia = document.createElement("div");
            dia.classList.add("dia", "mb-2");
            dia.innerHTML = `
                <select name="diasReserva[][dia]" class="form-select mb-1" required>
                    <option value="Lunes">Lunes</option>
                    <option value="Martes">Martes</option>
                    <option value="Miercoles">Miércoles</option>
                    <option value="Jueves">Jueves</option>
                    <option value="Viernes">Viernes</option>
                </select>
                <label for="rango" class="form-label">Rango Horario:</label>
                <input type="time" name="diasReserva[][rango_inicio]" class="form-control mb-1" required>
                <input type="time" name="diasReserva[][rango_fin]" class="form-control" required>
            `;
            container.appendChild(dia);
        }
        document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch del endpoint en Django
        const response = await fetch('/api/calendario');
        const calendario = await response.json();

        const tabla = document.getElementById('tabla-calendario');

        calendario.forEach(diaInfo => {
            const fila = document.createElement('tr');

            // Celda con el día de la semana y su fecha
            const celdaDia = document.createElement('td');
            celdaDia.textContent = diaInfo.dia;
            fila.appendChild(celdaDia);

            // Celda con los proyectos del día
            const celdaProyectos = document.createElement('td');
            if (diaInfo.proyectos.length > 0) {
                const lista = document.createElement('ul');
                diaInfo.proyectos.forEach(proyecto => {
                    const item = document.createElement('li');
                    item.innerHTML = `
                        <strong>${proyecto.nombre}</strong><br>
                        Horario: ${proyecto.horario.inicio} - ${proyecto.horario.fin}<br>
                        Integrantes: ${proyecto.integrantes.map(i => `${i.nombre} (${i.correo})`).join(', ')}
                    `;
                    lista.appendChild(item);
                });
                celdaProyectos.appendChild(lista);
            } else {
                celdaProyectos.textContent = 'Sin proyectos';
            }
            fila.appendChild(celdaProyectos);

            tabla.appendChild(fila);
        });

        // Mostrar el modal una vez que la tabla se haya llenado
        const modal = new bootstrap.Modal(document.getElementById('modalCalendario'));
        modal.show(); // Mostrar el modal

    } catch (error) {
        console.error('Error al cargar el calendario:', error);
    }
});
