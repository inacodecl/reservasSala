
const express = require('express');
const admin = require('../firebaseAdmin'); // Importamos la instancia de Firebase inicializada
const verificarAutenticacion = require('../middlewares/verificarAutenticacion'); 

// Inicializar la aplicación de Express
const deleteApp = express();
deleteApp.use(express.json());

// Definir la ruta para eliminar proyectos
deleteApp.delete('/deleteproyecto/:id', verificarAutenticacion, async (req, res) => {
  try {
    const clienteId = req.params.id;

    const clienteRef = admin.firestore().collection('proyectos').doc(clienteId);
    const doc = await clienteRef.get();

    if (!doc.exists) {
      return res.status(404).send('Cliente no encontrado');
    }

    await clienteRef.delete();
    res.status(200).json({ message: 'Proyecto eliminado correctamente' });
  } catch (error) {
    res.status(500).send('Error al eliminar el cliente: ' + error.message);
  }
});

module.exports = deleteApp;