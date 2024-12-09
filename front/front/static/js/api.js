const request = require('request');

// Definir la URL base de la API
const baseUrl = 'https://reservassala.inacode.cl/api/';

// Realizar la solicitud GET a la API de docentes
request.get({
    url: `${baseUrl}Docentes`,
    headers: {
        'Clave-De-Autenticacion': '[=kF!8QE`"&"YYQp$8,9W%n<&MCxjI;q'
    }
}, (error, response, body) => {
    if (error) {
        console.error('Error al obtener docentes:', error);
    } else if (response.statusCode !== 200) {
        console.error('Error de respuesta:', response.statusCode, body);
    } else {
        console.log('Respuesta de la API:', body);
    }
});

import axios from 'axios';

axios.get('https://reservassala.inacode.cl/api/docentes', {
    headers: {
        "Clave-De-Autenticacion": '[=kF!8QE`"&"YYQp$8,9W%n<&MCxjI;q'
    }
})
.then(response => console.log(response.data))
.catch(error => console.error("Error:", error));
