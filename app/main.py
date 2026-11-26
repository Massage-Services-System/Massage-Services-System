"""Run: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"""
import logging
import json
from fastapi import Depends, FastAPI, Header, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from .api import Application, error_json
from .config import ROOT, settings
from .schemas import AuthResponse, AvailabilityView, BookingCreate, BookingView, ErrorResponse, ServiceView, TelegramAuth, TherapistView, UserView, ZoneView
from .security import ApiError

application = Application()
app = FastAPI(title='Massage Services System', version='1.0.0', description='Telegram Mini App • Black & Gold • Zespół 3',
    responses={400: {'model': ErrorResponse}, 401: {'model': ErrorResponse}, 403: {'model': ErrorResponse}, 404: {'model': ErrorResponse}, 409: {'model': ErrorResponse}, 422: {'model': ErrorResponse}})


@app.middleware('http')
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.exception_handler(ApiError)
async def api_error(request, exc):
    return JSONResponse(error_json(exc), status_code=exc.status)


@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
    return JSONResponse(error_json(ApiError(422, 'validation_error', 'Sprawdź dane formularza.', [{'field': '.'.join(map(str, e['loc'])), 'message': e['msg']} for e in exc.errors()])), status_code=422)


@app.exception_handler(HTTPException)
async def http_error(request, exc):
    return JSONResponse(error_json(ApiError(exc.status_code, 'http_error', 'Nie znaleziono zasobu.' if exc.status_code == 404 else 'Żądanie nie jest obsługiwane.')), status_code=exc.status_code)


@app.exception_handler(Exception)
async def unexpected_error(request, exc):
    logging.getLogger(__name__).error('Request failed (%s)', type(exc).__name__)
    return JSONResponse(error_json(ApiError(500, 'internal_error', 'Nie udało się wykonać operacji. Spróbuj ponownie.')), status_code=500)


def authenticated(authorization: str = Header(default='')):
    return application.user_id(authorization)


@app.get('/api/v1/health', tags=['System'])
def health():
    return application.dispatch('GET', '/health')[0]


@app.get('/api/v1/config', tags=['System'])
def config(request: Request):
    return application.dispatch('GET', '/config', host=request.client.host)[0]


@app.post('/api/v1/auth/telegram', response_model=AuthResponse, tags=['Auth'])
def telegram_login(payload: TelegramAuth):
    return application.auth_telegram(payload.model_dump())


@app.post('/api/v1/auth/demo', response_model=AuthResponse, tags=['Auth'])
def demo_login(request: Request):
    return application.auth_demo(request.client.host)


@app.get('/api/v1/me', response_model=UserView, tags=['Auth'])
def me(user_id: int = Depends(authenticated)):
    return application.salon.user(user_id)


@app.get('/api/v1/zones', response_model=list[ZoneView], tags=['Catalog'])
def zones():
    return application.salon.zones()


@app.get('/api/v1/massages', response_model=list[ServiceView], tags=['Catalog'])
def massages(zone: str | None = None):
    return application.salon.catalog(zone)


@app.get('/api/v1/therapists', response_model=list[TherapistView], tags=['Catalog'])
def therapists():
    return application.salon.therapists()


@app.get('/api/v1/availability', response_model=AvailabilityView, tags=['Bookings'])
def availability(service_id: int = Query(gt=0), therapist_id: int = Query(gt=0), date: str = Query(pattern=r'^\d{4}-\d{2}-\d{2}$')):
    return application.salon.availability(service_id, therapist_id, date)


@app.post('/api/v1/bookings', response_model=BookingView, status_code=201, tags=['Bookings'])
def create_booking(payload: BookingCreate, user_id: int = Depends(authenticated)):
    return application.salon.book(user_id, **payload.model_dump())


@app.get('/api/v1/bookings', response_model=list[BookingView], tags=['Bookings'])
def bookings(user_id: int = Depends(authenticated)):
    return application.salon.visits(user_id)


@app.post('/api/v1/bookings/{booking_id}/cancel', response_model=BookingView, tags=['Bookings'])
def cancel(booking_id: str, user_id: int = Depends(authenticated)):
    return application.salon.cancel(user_id, booking_id)


@app.get('/assets/runtime-config.js', include_in_schema=False)
def frontend_config():
    return Response('window.MASSAGE_API_BASE = ' + json.dumps(settings.frontend_api_base) + ';', media_type='application/javascript', headers={'Cache-Control': 'no-store'})


app.mount('/assets', StaticFiles(directory=ROOT / 'frontend' / 'assets'), name='assets')


@app.get('/', include_in_schema=False)
def index():
    return FileResponse(ROOT / 'frontend' / 'index.html')


@app.get('/privacy', include_in_schema=False)
def privacy():
    return FileResponse(ROOT / 'frontend' / 'privacy.html')

