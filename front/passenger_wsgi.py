import os
import sys

# Establece la ruta base del proyecto
base_path = '/home/inacodec/SalasReservas'
virtualenv_path = os.path.join(base_path, 'entorno')

# Añade el proyecto y sus dependencias al sys.path
sys.path.insert(0, base_path)
sys.path.insert(1, os.path.join(virtualenv_path, 'Lib', 'site-packages'))

# Establece las variables de entorno necesarias
os.environ['DJANGO_SETTINGS_MODULE'] = 'inacodecl.settings'

# Importa la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
