import datetime as dt
import uuid
from zoneinfo import ZoneInfo
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from .models import Booking, OccupiedSlot, Outbox, Service, Therapist, User, WorkSchedule, Zone
from .security import ApiError

WARSAW = ZoneInfo('Europe/Warsaw')


def now_local():
    return dt.datetime.now(WARSAW)


def time_label(minute):
    return f'{minute // 60:02}:{minute % 60:02}'


def service_dict(service):
    return {k: getattr(service, k) for k in ('id', 'name', 'description', 'duration', 'price', 'category', 'icon')} | {'zones': [z.id for z in service.zones]}


def booking_dict(booking):
    date = dt.date.fromisoformat(booking.date)
    start = dt.datetime.combine(date, dt.time(booking.start_minute // 60, booking.start_minute % 60), WARSAW)
    end = start + dt.timedelta(minutes=booking.duration)
    return {'id': booking.id, 'date': booking.date, 'time': time_label(booking.start_minute), 'end_time': time_label(booking.start_minute + booking.duration),
        'duration': booking.duration, 'price': booking.price, 'status': booking.status,
        'past': end <= now_local(), 'started': start <= now_local(), 'service': booking.service.name,
        'service_id': booking.service_id, 'therapist': booking.therapist.name,
        'therapist_id': booking.therapist_id, 'note': booking.note}


class Salon:
    def __init__(self, Session):
        self.Session = Session

    def upsert_user(self, telegram_id, name, username=''):
        with self.Session.begin() as db:
            user = db.scalar(select(User).where(User.telegram_id == telegram_id))
            if not user:
                user = User(telegram_id=telegram_id, name=name, username=username)
                db.add(user)
            else:
                user.name, user.username = name, username
            try:
                db.flush()
            except IntegrityError:
                # A concurrent first login can win the unique telegram_id insert.
                db.rollback()
                with self.Session() as other:
                    existing = other.scalar(select(User).where(User.telegram_id == telegram_id))
                    return {'id': existing.id, 'name': existing.name, 'demo': existing.telegram_id.startswith('demo:')}
            return {'id': user.id, 'name': user.name, 'demo': user.telegram_id.startswith('demo:')}

    def user(self, user_id):
        with self.Session() as db:
            u = db.get(User, user_id)
            if not u:
                raise ApiError(401, 'unauthorized', 'Nie znaleziono użytkownika.')
            return {'id': u.id, 'name': u.name, 'demo': u.telegram_id.startswith('demo:')}

    def catalog(self, zone=None):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def zones(self):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def therapists(self):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def parse_date(self, value):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def _slots(self, db, service, therapist_id, date):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def availability(self, service_id, therapist_id, date):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def book(self, user_id, service_id, therapist_id, date, time, note=''):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def visits(self, user_id):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

    def cancel(self, user_id, booking_id):
        raise ApiError(501, 'not_implemented', 'Ta funkcja zostanie dodana w kolejnym zadaniu.')

