// firebaseAdmin.js
const admin = require('firebase-admin');

// Si Firebase ya está inicializado, no lo inicializamos nuevamente
if (!admin.apps.length) {
  const serviceAccount = require('./serviceAccountKey.json');
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: 'https://controlpaniol.firebaseio.com'
  });
}

module.exports = admin;