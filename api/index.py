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

_django_app = None

def _init_django():
    """Initialize Django and return the WSGI application (cached)."""
    global _django_app
    if _django_app is not None:
        return _django_app
    import django
    django.setup()
    from django.core.wsgi import get_wsgi_application
    _django_app = get_wsgi_application()
    return _django_app


def handler(request):
    """Vercel serverless function handler.

    Fast health-check: return 200 for /health without initializing Django so
    platform probes can succeed even if Django setup would fail.
    """
    # Lightweight health-check route that avoids loading Django
    if request.path in ("/health", "/api/health"):
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'OK'
        }
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

    # Ensure Django is initialized (lazy)
    django_app = _init_django()

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
