const express = require('express');
const admin = require('../firebaseAdmin');
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

const docentesApp = express()
docentesApp.use(express.json())


// Ruta para obtener todos los docentes
docentesApp.get('/docentes', verificarAutenticacion, async (req, res) => {
  try {
    const usersSnapshot = await admin.firestore().collection('docentes').get();
    const users = [];
    usersSnapshot.forEach(doc => {
      users.push({ id: doc.id, ...doc.data() });
    });
    res.status(200).json(users);
  } catch (error) {
    res.status(500).send('Error al obtener los docentes: ' + error.message);
  }
});

// Nueva ruta para buscar un docente por el RUT
docentesApp.get('/docentes/:rut', verificarAutenticacion, async (req, res) => {
  const { rut } = req.params;

  try {
    const usersSnapshot = await admin.firestore().collection('docentes')
      .where('rut', '==', rut)
      .get();

    if (usersSnapshot.empty) {
      return res.status(404).json({ message: 'Docente no encontrado' });
    }

    const users = [];
    usersSnapshot.forEach(doc => {
      users.push({ id: doc.id, ...doc.data() });
    });

    res.status(200).json(users[0]); // Suponiendo que RUT es único y retornamos el primer resultado
  } catch (error) {
    res.status(500).send('Error al buscar el docente: ' + error.message);
  }
});

module.exports = docentesApp;