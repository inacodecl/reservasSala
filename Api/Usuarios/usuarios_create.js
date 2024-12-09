const express = require('express');
const admin = require('../firebaseAdmin'); // Importamos la instancia de Firebase inicializada
const verificarAutenticacion = require('../middlewares/verificarAutenticacion'); // Importar middleware

// Inicializar la aplicación de Express
const addUser = express();
addUser.use(express.json());

// Definir la ruta para agregar docentes
addUser.post('/addUser', verificarAutenticacion,async (req, res) => {
  try {
    const newUser = req.body;
    const UserRef = await admin.firestore().collection('usuarios').add(newUser);
    res.status(201).json({ id: UserRef.id });
  } catch (error) {
    res.status(500).send('Error al agregar su User: ' + error.message);
  }
});

module.exports = addUser;