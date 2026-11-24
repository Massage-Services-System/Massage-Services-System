"""Offline review adapter when FastAPI cannot be installed. Same application/domain.
Never use as production deployment. Flask is an optional, preinstalled review dependency.
"""
import logging
import json
from flask import Flask, jsonify, request, send_from_directory
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from .api import Application, error_json
from .config import ROOT, settings
from .security import ApiError


def create_preview(application=None):
    if settings.app_env != 'development':
        raise RuntimeError('Offline preview is restricted to development.')
    application = application or Application()
    app = Flask(__name__, static_folder=None)
    app.config['MAX_CONTENT_LENGTH'] = 32768

    @app.route('/api/v1/<path:path>', methods=['GET', 'POST'])
    def api(path):
        payload = request.get_json(silent=True) if request.method == 'POST' else None
        result, status = application.dispatch(request.method, '/' + path, payload, request.args,
            request.headers.get('Authorization', ''), request.remote_addr)
        return jsonify(result), status

    @app.get('/')
    def index():
        return send_from_directory(ROOT / 'frontend', 'index.html')

    @app.get('/privacy')
    def privacy():
        return send_from_directory(ROOT / 'frontend', 'privacy.html')

    @app.get('/assets/<path:filename>')
    def asset(filename):
        if filename == 'runtime-config.js':
            return app.response_class('window.MASSAGE_API_BASE = ' + json.dumps(settings.frontend_api_base) + ';', mimetype='application/javascript')
        return send_from_directory(ROOT / 'frontend' / 'assets', filename)

    @app.errorhandler(ApiError)
    def api_error(error):
        return jsonify(error_json(error)), error.status

    @app.errorhandler(ValidationError)
    def validation(error):
        return jsonify(error_json(ApiError(422, 'validation_error', 'Sprawdź dane formularza.', [{'field': '.'.join(map(str, e['loc'])), 'message': e['msg']} for e in error.errors()]))), 422

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error_json(ApiError(error.code, 'http_error', 'Nie udało się obsłużyć żądania.'))), error.code

    @app.errorhandler(Exception)
    def unexpected(error):
        logging.getLogger(__name__).error('Preview request failed (%s)', type(error).__name__)
        return jsonify(error_json(ApiError(500, 'internal_error', 'Spróbuj ponownie.'))), 500

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        if request.path.startswith('/api/'):
            response.headers['Cache-Control'] = 'no-store'
        return response

    return app


if __name__ == '__main__':
    create_preview().run(host='127.0.0.1', port=8000, debug=False, use_reloader=False)

