const express = require('express');
const admin = require('../firebaseAdmin'); // Importamos la instancia de Firebase inicializada
const verificarAutenticacion = require('../middlewares/verificarAutenticacion'); // Importar middleware

// Inicializar la aplicación de Express
const addProyecto = express();
addProyecto.use(express.json());

// Definir la ruta para agregar docentes
addProyecto.post('/addProyecto', verificarAutenticacion,async (req, res) => {
  try {
    const newUser = req.body;
    const userRef = await admin.firestore().collection('proyectos').add(newUser);
    res.status(201).json({ id: userRef.id });
  } catch (error) {
    res.status(500).send('Error al agregar proyecto: ' + error.message);
  }
});

module.exports = addProyecto;