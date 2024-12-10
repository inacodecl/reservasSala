const express = require('express');
const admin = require('../firebaseAdmin');
const verificarAutenticacion = require('../middlewares/verificarAutenticacion'); // Importar middleware

const addDocentesApp = express();
addDocentesApp.use(express.json());

// Ruta protegida para agregar docentes
addDocentesApp.post('/addDocentes', verificarAutenticacion, async (req, res) => {
  try {
    const newUser = req.body;
    const userRef = await admin.firestore().collection('docentes').add(newUser);
    res.status(201).json({ id: userRef.id });
  } catch (error) {
    res.status(500).send('Error al agregar Docente: ' + error.message);
  }
});

module.exports = addDocentesApp;