import os
from django.core.wsgi import get_wsgi_application

# Establece el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inacodecl.settings')

# Obtiene la aplicación WSGI
application = get_wsgi_application()