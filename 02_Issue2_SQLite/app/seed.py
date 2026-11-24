from sqlalchemy import select
from .models import Service, Therapist, WorkSchedule, Zone

ZONES = [('neck', 'Kark i szyja'), ('shoulders', 'Barki'), ('back', 'Plecy'), ('arms', 'Ramiona i dłonie'), ('legs', 'Nogi'), ('feet', 'Stopy')]
SERVICES = [
    (1, 'Masaż relaksacyjny', 'Spokojny rytm, ciepły olejek i chwila tylko dla Ciebie. Pozwól napięciu odejść.', 60, 180, 'Relaks', 'lotus', ['neck', 'shoulders', 'back', 'arms', 'legs', 'feet']),
    (2, 'Masaż klasyczny', 'Uważna praca z mięśniami. Wybierz swój obszar i wróć do codziennej lekkości.', 60, 200, 'Regeneracja', 'hands', ['neck', 'shoulders', 'back', 'arms', 'legs']),
    (3, 'Masaż sportowy', 'Intensywniejszy rytuał dla aktywnych. Czas na odpoczynek po Twoim treningu.', 90, 260, 'Aktywność', 'spark', ['shoulders', 'back', 'arms', 'legs']),
    (4, 'Masaż gorącymi kamieniami', 'Otulające ciepło bazaltowych kamieni i płynne ruchy w wyjątkowo spokojnym rytmie.', 90, 280, 'Rytuał', 'stones', ['shoulders', 'back', 'legs']),
    (5, 'Masaż karku i barków', 'Przerwa od ekranu. Skupiona sesja poświęcona okolicy szyi, karku i ramion.', 30, 120, 'Uwolnienie napięcia', 'leaf', ['neck', 'shoulders']),
    (6, 'Masaż stóp', 'Mały rytuał, wielka przyjemność. Uważny masaż zmęczonych stóp i łydek.', 30, 100, 'Lekkość', 'wave', ['feet', 'legs']),
]


def seed(Session):
    with Session.begin() as db:
        for key, name in ZONES:
            if not db.get(Zone, key):
                db.add(Zone(id=key, name=name))
        db.flush()
        for sid, name, desc, duration, price, category, icon, zones in SERVICES:
            if not db.get(Service, sid):
                db.add(Service(id=sid, name=name, description=desc, duration=duration, price=price,
                    category=category, icon=icon, zones=[db.get(Zone, key) for key in zones]))
        for tid, name, specialty, initials in [(1, 'Anna Kowalska', 'Relaks i masaż klasyczny', 'AK'), (2, 'Michał Nowak', 'Masaż sportowy i regeneracja', 'MN'), (3, 'Julia Wiśniewska', 'Rytuały i gorące kamienie', 'JW')]:
            if not db.get(Therapist, tid):
                db.add(Therapist(id=tid, name=name, specialty=specialty, initials=initials))
                db.flush()
            for weekday in range(6):
                if not db.scalar(select(WorkSchedule).where(WorkSchedule.therapist_id == tid, WorkSchedule.weekday == weekday)):
                    db.add(WorkSchedule(therapist_id=tid, weekday=weekday, start_minute=600, end_minute=1080 if weekday < 5 else 960))

