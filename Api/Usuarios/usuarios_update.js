const express = require('express');
const admin = require('../firebaseAdmin');
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

const appUpdateUser = express();
appUpdateUser.use(express.json());

// Endpoint para actualizar el User existente
appUpdateUser.put('/updateUser/:id', verificarAutenticacion, async (req, res) => {
  try {
    const UserId = req.params.id;
    const updatedData = req.body;

    const UserRef = admin.firestore().collection('usuarios').doc(UserId);
    const doc = await UserRef.get();

    if (!doc.exists) {
      return res.status(404).send('User no encontrado');
    }

    await UserRef.update(updatedData);
    res.status(200).json({ message: 'User actualizado correctamente' });
  } catch (error) {
    res.status(500).send('Error al actualizar el User: ' + error.message);
  }
});

// Nuevo endpoint para deshabilitar un User (cambiar status a 0)
appUpdateUser.put('/deshabilitarUser/:id', verificarAutenticacion, async (req, res) => {
  try {
    const UserId = req.params.id;

    // Referencia al documento del User
    const UserRef = admin.firestore().collection('usuarios').doc(UserId);
    const doc = await UserRef.get();

    if (!doc.exists) {
      return res.status(404).json({ message: 'User no encontrado' });
    }

    // Actualiza solo el campo "status" a 0 para deshabilitar
    await UserRef.update({ status: "Desaprobado" });

    res.status(200).json({ message: 'User deshabilitado correctamente' });
  } catch (error) {
    res.status(500).send('Error al deshabilitar User: ' + error.message);
  }
});

// Nuevo endpoint para deshabilitar un User (cambiar status a 0)
appUpdateUser.put('/habilitarUser/:id', verificarAutenticacion, async (req, res) => {
  try {
    const UserId = req.params.id;

    // Referencia al documento del User
    const UserRef = admin.firestore().collection('usuarios').doc(UserId);
    const doc = await UserRef.get();

    if (!doc.exists) {
      return res.status(404).json({ message: 'User no encontrado' });
    }

    // Actualiza solo el campo "status" a 1 para habilitar
    await UserRef.update({ status: "Aprobado" });

    res.status(200).json({ message: 'User habilitado correctamente' });
  } catch (error) {
    res.status(500).send('Error al habilitar User: ' + error.message);
  }
});

module.exports = appUpdateUser;