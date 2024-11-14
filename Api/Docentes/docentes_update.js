const express = require('express');
const admin = require('../firebaseAdmin');
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

const updateApp = express();
updateApp.use(express.json());

// Endpoint para actualizar los datos generales de un docente (existente)
updateApp.put('/updateDocente/:id', verificarAutenticacion,async (req, res) => {
  try {
    const clienteId = req.params.id;
    const updatedData = req.body;

    const clienteRef = admin.firestore().collection('docentes').doc(clienteId);
    const doc = await clienteRef.get();

    if (!doc.exists) {
      return res.status(404).send('Cliente no encontrado');
    }

    await clienteRef.update(updatedData);
    res.status(200).json({ message: 'Cliente actualizado correctamente' });
  } catch (error) {
    res.status(500).send('Error al actualizar el cliente: ' + error.message);
  }
});

// Nuevo endpoint para deshabilitar un docente (cambiar status a 0)
updateApp.put('/deshabilitarDocente/:id', verificarAutenticacion, async (req, res) => {
  try {
    const docenteId = req.params.id;

    // Referencia al documento del docente
    const docenteRef = admin.firestore().collection('docentes').doc(docenteId);
    const doc = await docenteRef.get();

    if (!doc.exists) {
      return res.status(404).json({ message: 'Docente no encontrado' });
    }

    // Actualiza solo el campo "status" a 0 para deshabilitar
    await docenteRef.update({ status: 0 });

    res.status(200).json({ message: 'Docente deshabilitado correctamente' });
  } catch (error) {
    res.status(500).send('Error al deshabilitar el docente: ' + error.message);
  }
});

// Nuevo endpoint para deshabilitar un docente (cambiar status a 0)
updateApp.put('/habilitarDocente/:id', verificarAutenticacion, async (req, res) => {
  try {
    const docenteId = req.params.id;

    // Referencia al documento del docente
    const docenteRef = admin.firestore().collection('docentes').doc(docenteId);
    const doc = await docenteRef.get();

    if (!doc.exists) {
      return res.status(404).json({ message: 'Docente no encontrado' });
    }

    // Actualiza solo el campo "status" a 1 para habilitar
    await docenteRef.update({ status: 1 });

    res.status(200).json({ message: 'Docente habilitado correctamente' });
  } catch (error) {
    res.status(500).send('Error al deshabilitar el docente: ' + error.message);
  }
});

module.exports = updateApp;