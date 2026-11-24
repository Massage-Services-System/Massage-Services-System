from .config import settings
from .security import ApiError

class PendingSalon:
    def __getattr__(self, name):
        def pending(*args, **kwargs):
            raise ApiError(501, 'not_implemented', 'Kontrakt API jest gotowy; ta funkcja jest w kolejnym zadaniu.')
        return pending


class Application:
    def __init__(self, config=settings):
        self.config = config
        self.salon = PendingSalon()

    def auth_telegram(self, payload):
        raise ApiError(501, 'not_implemented', 'Uwierzytelnianie jest w zadaniu #3.')

    def auth_demo(self, host):
        raise ApiError(501, 'not_implemented', 'Uwierzytelnianie jest w zadaniu #3.')

    def user_id(self, authorization):
        raise ApiError(501, 'not_implemented', 'Uwierzytelnianie jest w zadaniu #3.')

    def dispatch(self, method, path, payload=None, query=None, authorization='', host=''):
        if method == 'GET' and path == '/health':
            return {'status': 'ok', 'version': '1.0.0'}, 200
        if method == 'GET' and path == '/config':
            return {'demo_available': False, 'timezone': 'Europe/Warsaw', 'currency': 'PLN'}, 200
        if path in ('/massages', '/zones', '/therapists', '/availability', '/bookings', '/me', '/auth/telegram', '/auth/demo'):
            raise ApiError(501, 'not_implemented', 'Kontrakt API jest gotowy; funkcja dojdzie w kolejnych zadaniach.')
        raise ApiError(404, 'not_found', 'Nie znaleziono zasobu.')


def error_json(error):
    return {'error': {'code': error.code, 'message': error.message, 'details': error.details}}
