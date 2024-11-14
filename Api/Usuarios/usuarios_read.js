const express = require('express');
const admin = require('../firebaseAdmin'); // Importamos la instancia de Firebase inicializada
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

const appReadUser = express();
appReadUser.use(express.json());

// Ruta para obtener todos los Users
appReadUser.get('/Users', verificarAutenticacion, async (req, res) => {
  try {
    const UserSnapshot = await admin.firestore().collection('usuarios').get();
    const User = [];
    UserSnapshot.forEach(doc => {
      User.push({ id: doc.id, ...doc.data() });
    });
    res.status(200).json(User);
  } catch (error) {
    res.status(500).send('Error al obtener los Users: ' + error.message);
  }
});

// Nueva ruta para buscar un User por el nombre
appReadUser.get('/buscarUser/:nombre', verificarAutenticacion, async (req, res) => {
  const { nombre } = req.params;

  try {
    const UserSnapshot = await admin.firestore().collection('usuarios')
      .where('nombre', '==', nombre)
      .get();

    if (UserSnapshot.empty) {
      return res.status(404).json({ message: 'User no encontrado' });
    }

    const User = [];
    UserSnapshot.forEach(doc => {
      User.push({ id: doc.id, ...doc.data() });
    });

    res.status(200).json(User[0]); // Suponiendo que RUT es único y retornamos el primer resultado
  } catch (error) {
    res.status(500).send('Error al buscar el User: ' + error.message);
  }
});

module.exports = appReadUser;
