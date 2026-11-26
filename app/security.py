import base64
import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl


class ApiError(Exception):
    def __init__(self, status, code, message, details=None):
        self.status, self.code, self.message, self.details = status, code, message, details


def verify_init_data(init_data, token, max_age=3600, now=None):
    if not token:
        raise ApiError(503, 'telegram_unconfigured', 'Logowanie Telegram jest chwilowo niedostępne.')
    if not isinstance(init_data, str) or len(init_data) > 16384:
        raise ApiError(401, 'invalid_init_data', 'Nieprawidłowe dane Telegram.')
    pairs = parse_qsl(init_data, keep_blank_values=True)
    if len({key for key, _ in pairs}) != len(pairs):
        raise ApiError(401, 'invalid_init_data', 'Powtórzone pola Telegram.')
    fields = dict(pairs)
    supplied_hash = fields.pop('hash', '')
    if len(supplied_hash) != 64 or any(c not in '0123456789abcdef' for c in supplied_hash):
        raise ApiError(401, 'invalid_init_data', 'Nieprawidłowy podpis Telegram.')
    # signature remains in the HMAC data-check-string; only hash is excluded.
    secret = hmac.new(b'WebAppData', token.encode(), hashlib.sha256).digest()
    data = '\n'.join(f'{key}={value}' for key, value in sorted(fields.items()))
    expected = hmac.new(secret, data.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, supplied_hash):
        raise ApiError(401, 'invalid_init_data', 'Nie udało się potwierdzić tożsamości Telegram.')
    try:
        auth_date = int(fields['auth_date'])
        age = int(now if now is not None else time.time()) - auth_date
        if age < -30 or age > max_age:
            raise ValueError('expired')
        user = json.loads(fields['user'])
        if type(user['id']) is not int or user['id'] <= 0 or not isinstance(user['first_name'], str) or not user['first_name'].strip():
            raise ValueError('user')
        return {'telegram_id': str(user['id']), 'name': user['first_name'][:100], 'username': str(user.get('username', ''))[:100]}
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        raise ApiError(401, 'expired_init_data', 'Sesja Telegram wygasła. Otwórz aplikację ponownie.')


def make_session(user_id, secret, now=None):
    body = f'{user_id}:{int(now if now is not None else time.time())}'
    encoded = base64.urlsafe_b64encode(body.encode()).decode().rstrip('=')
    digest = hmac.new(secret.encode(), encoded.encode(), hashlib.sha256).hexdigest()
    return f'{encoded}.{digest}'


def verify_session(token, secret, now=None):
    try:
        encoded, supplied = token.split('.')
        expected = hmac.new(secret.encode(), encoded.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, supplied):
            raise ValueError()
        user_id, issued = base64.urlsafe_b64decode(encoded + '=' * (-len(encoded) % 4)).decode().split(':')
        age = int(now if now is not None else time.time()) - int(issued)
        if age < -30 or age > 43200:
            raise ValueError()
        return int(user_id)
    except (ValueError, TypeError, UnicodeError):
        raise ApiError(401, 'unauthorized', 'Zaloguj się ponownie, aby zarządzać wizytami.')

