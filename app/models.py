from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, UniqueConstraint, create_engine, event
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
service_zones = Table('service_zones', Base.metadata,
    Column('service_id', ForeignKey('services.id'), primary_key=True),
    Column('zone_id', ForeignKey('zones.id'), primary_key=True))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String)


class Zone(Base):
    __tablename__ = 'zones'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    zones = relationship(Zone, secondary=service_zones)


class Therapist(Base):
    __tablename__ = 'therapists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    initials = Column(String, nullable=False)


class WorkSchedule(Base):
    __tablename__ = 'work_schedules'
    __table_args__ = (UniqueConstraint('therapist_id', 'weekday'),)
    id = Column(Integer, primary_key=True)
    therapist_id = Column(Integer, ForeignKey('therapists.id'), nullable=False)
    weekday = Column(Integer, nullable=False)
    start_minute = Column(Integer, nullable=False)
    end_minute = Column(Integer, nullable=False)


class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    therapist_id = Column(Integer, ForeignKey('therapists.id'), nullable=False, index=True)
    date = Column(String, nullable=False, index=True)
    start_minute = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default='confirmed')
    note = Column(String, nullable=False, default='')
    created_at = Column(String, nullable=False)
    service = relationship(Service)
    therapist = relationship(Therapist)


class OccupiedSlot(Base):
    """One row per 30 min. PK prevents overlapping bookings, including unequal durations."""
    __tablename__ = 'occupied_slots'
    therapist_id = Column(Integer, ForeignKey('therapists.id'), primary_key=True)
    date = Column(String, primary_key=True)
    minute = Column(Integer, primary_key=True)
    booking_id = Column(String, ForeignKey('bookings.id'), nullable=False, index=True)


class Outbox(Base):
    __tablename__ = 'notification_outbox'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    sent = Column(Boolean, nullable=False, default=False)


class BotState(Base):
    __tablename__ = 'bot_state'
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


def make_database(url):
    engine = create_engine(url, connect_args={'check_same_thread': False, 'timeout': 20} if url.startswith('sqlite') else {})
    if url.startswith('sqlite'):
        @event.listens_for(engine, 'connect')
        def sqlite_settings(connection, _):
            connection.execute('PRAGMA foreign_keys=ON')
            connection.execute('PRAGMA busy_timeout=20000')
            connection.execute('PRAGMA journal_mode=WAL')
    Base.metadata.create_all(engine)
    return engine, sessionmaker(engine, expire_on_commit=False)

