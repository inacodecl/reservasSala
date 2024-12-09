const express = require('express');
const admin = require('../firebaseAdmin');
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

// Inicializar la aplicación de Express
const deleteApp = express();
deleteApp.use(express.json());

// Definir la ruta para eliminar docentes
deleteApp.delete('/deleteDocente/:id', verificarAutenticacion, async (req, res) => {
  try {
    const docenteId = req.params.id;
    const docenteRef = admin.firestore().collection('docentes').doc(docenteId);
    const doc = await docenteRef.get();

    if (!doc.exists) {
      return res.status(404).send('Docente no encontrado');
    }

    await docenteRef.delete();
    res.status(200).json({ message: 'Docente eliminado correctamente' });
  } catch (error) {
    res.status(500).send('Error al eliminar el docente: ' + error.message);
  }
});

module.exports = deleteApp;