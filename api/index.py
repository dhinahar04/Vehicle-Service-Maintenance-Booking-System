"""
Vercel serverless function for Django.
This handler works with Vercel's Python runtime.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
"""
Vercel serverless function for Django.
This handler works with Vercel's Python runtime.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_service.settings')

# Initialize Django
import django
django.setup()

from django.core.wsgi import get_wsgi_application

# Get Django WSGI application
django_app = get_wsgi_application()

def handler(request):
    """
    Vercel serverless function handler.
    """
    from io import BytesIO

    # Build WSGI environ dictionary
    environ = {
        'REQUEST_METHOD': request.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string or '',
        'CONTENT_TYPE': request.headers.get('Content-Type', ''),
        'CONTENT_LENGTH': str(len(request.body or b'')),
        'SERVER_NAME': request.headers.get('Host', 'localhost').split(':')[0],
        'SERVER_PORT': request.headers.get('Host', 'localhost').split(':')[1] if ':' in request.headers.get('Host', '') else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https' if request.headers.get('X-Forwarded-Proto') == 'https' else 'http',
        'wsgi.input': BytesIO(request.body or b''),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }

    # Add HTTP headers to environ
    for key, value in request.headers.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key_upper}'] = value

    # Call Django WSGI application
    response_data = []

    def start_response(status, response_headers):
        response_data.append((status, response_headers))

    # Execute Django application
    result = django_app(environ, start_response)

    # Extract response
    status, headers = response_data[0]
    status_code = int(status.split()[0])
    body = b''.join(result)

    # Return response in Vercel format
    return {
        'statusCode': status_code,
        'headers': dict(headers),
        'body': body.decode('utf-8')
    }
