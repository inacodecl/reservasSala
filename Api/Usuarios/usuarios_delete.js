const express = require('express');
const admin = require('../firebaseAdmin');
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

// Inicializar la aplicación de Express
const appDeleteUser = express();
appDeleteUser.use(express.json());

// Definir la ruta para eliminar Users
appDeleteUser.delete('/deleteUser/:id', verificarAutenticacion, async (req, res) => {
  try {
    const UserId = req.params.id;
    const UserRef = admin.firestore().collection('usuarios').doc(UserId);
    const doc = await UserRef.get();

    if (!doc.exists) {
      return res.status(404).send('User no encontrada');
    }

    await UserRef.delete();
    res.status(200).json({ message: 'User eliminado correctamente' });
  } catch (error) {
    res.status(500).send('Error al eliminar la User: ' + error.message);
  }
});

module.exports = appDeleteUser;