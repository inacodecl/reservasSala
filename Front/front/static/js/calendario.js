document.getElementById("btn-calendario").addEventListener("click", async () => {
    const calendarioContainer = document.getElementById("calendario-container");
    calendarioContainer.innerHTML = "<p>Cargando calendario...</p>";

    try {
        const response = await fetch("obtener_proyectos");
        if (!response.ok) {
            throw new Error("Error al obtener los datos del calendario.");
        }

        const proyectos = await response.json();

        // Transformar los datos en eventos para FullCalendar
        const eventos = proyectos.flatMap(proyecto =>
            Object.entries(proyecto.diasReserva).map(([dia, rango]) => ({
                title: proyecto.nombre,
                start: `${proyecto.inicio}T${rango.rango_horas.inicio}`,
                end: `${proyecto.fin}T${rango.rango_horas.fin}`,
                allDay: false,
                backgroundColor: proyecto.autorizado ? "green" : "red"
            }))
        );

        // Renderizar FullCalendar
        calendarioContainer.innerHTML = ""; // Limpiar contenedor
        const calendarEl = document.createElement("div");
        calendarEl.id = "calendar";
        calendarioContainer.appendChild(calendarEl);

        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: "timeGridWeek",
            locale: "es",
            events: eventos,
            headerToolbar: {
                left: "prev,next today",
                center: "title",
                right: "timeGridWeek,timeGridDay"
            }
        });

        calendar.render();
    } catch (error) {
        console.error(error);
        calendarioContainer.innerHTML = "<p>Error al cargar el calendario. Inténtalo de nuevo más tarde.</p>";
    }
});
