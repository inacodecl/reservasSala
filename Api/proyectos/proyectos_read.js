const express = require('express');
const admin = require('../firebaseAdmin'); // Importamos la instancia de Firebase inicializada
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

const proyectosApp = express();
proyectosApp.use(express.json());

// Ruta para obtener todos los proyectos
proyectosApp.get('/proyectos', verificarAutenticacion, async (req, res) => {
  try {
    const usersSnapshot = await admin.firestore().collection('proyectos').get();
    const users = [];
    usersSnapshot.forEach(doc => {
      users.push({ id: doc.id, ...doc.data() });
    });
    res.status(200).json(users);
  } catch (error) {
    res.status(500).send('Error al obtener los proyectos: ' + error.message);
  }
});

// Nueva ruta para buscar un proyecto por el nombre
proyectosApp.get('/proyectos/:id', verificarAutenticacion, async (req, res) => {
  const { id } = req.params;

  try {
    // Obtener el documento directamente por su ID
    const proyectoDoc = await admin.firestore().collection('proyectos').doc(id).get();

    if (!proyectoDoc.exists) {
      return res.status(404).json({ message: 'Proyecto no encontrado' });
    }

    // Devolver los datos del proyecto
    const proyectoData = { id: proyectoDoc.id, ...proyectoDoc.data() };
    res.status(200).json(proyectoData);
  } catch (error) {
    res.status(500).send('Error al buscar el proyecto: ' + error.message);
  }
});

module.exports = proyectosApp;
