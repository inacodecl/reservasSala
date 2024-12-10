const express = require(`express`);
const verificarAutenticacion = require(`./middlewares/verificarAutenticacion`);


const app = express();
const PORT = 4110;
const ruta = "/api"


// Middleware de autenticación para todas las rutas
app.use(verificarAutenticacion);

// Rutas para APIs de docentes
app.use(`${ruta}`, require(`./Docentes/docentes_read`));
app.use(`${ruta}`, require(`./Docentes/docentes_create`));
app.use(`${ruta}`, require(`./Docentes/docentes_update`));
app.use(`${ruta}`, require(`./Docentes/docentes_delete`));

// Rutas para APIs de proyectos
app.use(`${ruta}`, require(`./proyectos/proyectos_read`));
app.use(`${ruta}`, require(`./proyectos/proyectos_create`));
app.use(`${ruta}`, require(`./proyectos/proyectos_update`));
app.use(`${ruta}`, require(`./proyectos/proyectos_delete`));

// Rutas para APIs de usuarios
app.use(`${ruta}`, require(`./Usuarios/usuarios_read`));
app.use(`${ruta}`, require(`./Usuarios/usuarios_create`));
app.use(`${ruta}`, require(`./Usuarios/usuarios_update`));
app.use(`${ruta}`, require(`./Usuarios/usuarios_delete`));

// Inicializar el servidor en el puerto 4110
app.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});
