"""Shared application boundary for FastAPI and the offline review server."""
import uuid
from .config import settings
from .models import make_database
from .schemas import BookingCreate, TelegramAuth
from .security import ApiError, make_session, verify_init_data, verify_session
from .seed import seed
from .services import Salon


class Application:
    def __init__(self, config=settings):
        self.config = config
        self.engine, self.Session = make_database(config.database_url)
        seed(self.Session)
        self.salon = Salon(self.Session)

    def auth_result(self, user):
        return {'access_token': make_session(user['id'], self.config.session_secret), 'token_type': 'bearer', 'expires_in': 43200, 'user': user}

    def auth_telegram(self, payload):
        data = TelegramAuth.model_validate(payload)
        user = verify_init_data(data.init_data, self.config.bot_token, self.config.init_data_max_age)
        return self.auth_result(self.salon.upsert_user(**user))

    def auth_demo(self, host):
        if self.config.app_env != 'development' or not self.config.allow_demo or host not in ('127.0.0.1', '::1', 'localhost', 'testclient'):
            raise ApiError(403, 'demo_disabled', 'Tryb demonstracyjny jest dostępny tylko lokalnie.')
        return self.auth_result(self.salon.upsert_user('demo:' + uuid.uuid4().hex, 'Gość'))

    def user_id(self, authorization):
        if not authorization.startswith('Bearer '):
            raise ApiError(401, 'unauthorized', 'Otwórz aplikację w Telegramie lub uruchom lokalny podgląd.')
        user_id = verify_session(authorization[7:], self.config.session_secret)
        self.salon.user(user_id)
        return user_id

    def dispatch(self, method, path, payload=None, query=None, authorization='', host=''):
        query = query or {}
        if method == 'GET':
            if path == '/health':
                with self.engine.connect() as db:
                    from sqlalchemy import text
                    db.execute(text('SELECT 1'))
                return {'status': 'ok', 'version': '1.0.0'}, 200
            if path == '/config':
                return {'demo_available': self.config.app_env == 'development' and self.config.allow_demo and host in ('127.0.0.1', '::1', 'localhost', 'testclient'),
                    'bot_username': 'MassageServicesSystem_bot', 'timezone': 'Europe/Warsaw', 'currency': 'PLN', 'seed_data': True}, 200
            if path == '/zones':
                return self.salon.zones(), 200
            if path == '/massages':
                return self.salon.catalog(query.get('zone')), 200
            if path == '/therapists':
                return self.salon.therapists(), 200
            if path == '/availability':
                try:
                    sid, tid = int(query['service_id']), int(query['therapist_id'])
                    date = query['date']
                except (KeyError, ValueError, TypeError):
                    raise ApiError(422, 'validation_error', 'Wybierz masaż, masażystę i datę.')
                return self.salon.availability(sid, tid, date), 200
        if method == 'POST' and path == '/auth/telegram':
            return self.auth_telegram(payload), 200
        if method == 'POST' and path == '/auth/demo':
            return self.auth_demo(host), 200
        if method == 'GET' and path == '/me':
            return self.salon.user(self.user_id(authorization)), 200
        if method == 'GET' and path == '/bookings':
            return self.salon.visits(self.user_id(authorization)), 200
        if method == 'POST' and path == '/bookings':
            user_id = self.user_id(authorization)
            data = BookingCreate.model_validate(payload)
            return self.salon.book(user_id, **data.model_dump()), 201
        if method == 'POST' and path.startswith('/bookings/') and path.endswith('/cancel'):
            booking_id = path[len('/bookings/'):-len('/cancel')]
            return self.salon.cancel(self.user_id(authorization), booking_id), 200
        raise ApiError(404, 'not_found', 'Nie znaleziono żądanego zasobu.')


def error_json(error):
    return {'error': {'code': error.code, 'message': error.message, 'details': error.details}}

