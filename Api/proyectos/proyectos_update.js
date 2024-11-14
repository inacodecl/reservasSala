const express = require('express');
const admin = require('../firebaseAdmin');
const verificarAutenticacion = require('../middlewares/verificarAutenticacion');

const updateApp = express();
updateApp.use(express.json());

// Endpoint para actualizar el proyecto existente
updateApp.put('/updateProyecto/:id', verificarAutenticacion, async (req, res) => {
  try {
    const clienteId = req.params.id;
    const updatedData = req.body;

    const clienteRef = admin.firestore().collection('proyectos').doc(clienteId);
    const doc = await clienteRef.get();

    if (!doc.exists) {
      return res.status(404).send('Proyecto no encontrado');
    }

    await clienteRef.update(updatedData);
    res.status(200).json({ message: 'Proyecto actualizado correctamente' });
  } catch (error) {
    res.status(500).send('Error al actualizar el proyecto: ' + error.message);
  }
});

// Nuevo endpoint para deshabilitar un Proyecto (cambiar status a 0)
updateApp.put('/deshabilitarProyecto/:id', verificarAutenticacion, async (req, res) => {
  try {
    const proyectoId = req.params.id;

    // Referencia al documento del proyecto
    const proyectoRef = admin.firestore().collection('proyectos').doc(proyectoId);
    const doc = await proyectoRef.get();

    if (!doc.exists) {
      return res.status(404).json({ message: 'proyecto no encontrado' });
    }

    // Actualiza los campos "autorizado" y "estado"
    await proyectoRef.update({ 
      autorizado: 0,
      estado: 'Terminado' 
    });

    res.status(200).json({ message: 'proyecto deshabilitado correctamente' });
  } catch (error) {
    res.status(500).send('Error al deshabilitar el proyecto: ' + error.message);
  }
});


// Nuevo endpoint para deshabilitar un proyecto (cambiar status a 0)
updateApp.put('/habilitarproyecto/:id', verificarAutenticacion, async (req, res) => {
  try {
    const proyectoId = req.params.id;

    // Referencia al documento del proyecto
    const proyectoRef = admin.firestore().collection('proyectos').doc(proyectoId);
    const doc = await proyectoRef.get();

    if (!doc.exists) {
      return res.status(404).json({ message: 'proyecto no encontrado' });
    }

    // Actualiza los campos "autorizado" y "estado"
    await proyectoRef.update({ 
      autorizado: 1,
      estado: 'reservado' 
    });

    res.status(200).json({ message: 'proyecto habilitado correctamente' });
  } catch (error) {
    res.status(500).send('Error al habilitar el proyecto: ' + error.message);
  }
});

module.exports = updateApp;