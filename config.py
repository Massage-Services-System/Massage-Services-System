"""Environment-only secrets; no configuration is sent to the browser."""
import os
import secrets
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env(path=ROOT / '.env'):
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if line.strip() and not line.lstrip().startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip().strip('\"').strip("'"))


load_env()


@dataclass
class Settings:
    database_url: str = os.getenv('DATABASE_URL', f'sqlite:///{(ROOT / "data" / "massage.db").as_posix()}')
    bot_token: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    session_secret: str = os.getenv('SESSION_SECRET', '')
    app_env: str = os.getenv('APP_ENV', 'development')
    allow_demo: bool = os.getenv('ALLOW_DEMO', 'true').lower() == 'true'
    public_url: str = os.getenv('PUBLIC_APP_URL', '').rstrip('/')
    cors_origins: str = os.getenv('CORS_ORIGINS', '')
    frontend_api_base: str = os.getenv('FRONTEND_API_BASE', '').rstrip('/')
    init_data_max_age: int = 3600

    def validate(self):
        (ROOT / 'data').mkdir(exist_ok=True)
        if self.app_env == 'production':
            if self.allow_demo:
                raise RuntimeError('ALLOW_DEMO must be false in production.')
            if len(self.session_secret) < 32 or not self.bot_token or not self.public_url.startswith('https://'):
                raise RuntimeError('Production requires a bot token, HTTPS PUBLIC_APP_URL and SESSION_SECRET (32+ chars).')
        if not self.session_secret:
            self.session_secret = secrets.token_urlsafe(48)


settings = Settings()
settings.validate()

