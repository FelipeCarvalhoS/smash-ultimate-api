from pathlib import Path
from dotenv import load_dotenv
import os
import sentry_sdk


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
R2_URL = os.getenv('R2_URL')
REPO_URL = os.getenv('REPO_URL')
FAVICON_URL = R2_URL + 'favicon.png'


sentry_sdk.init(
    environment=os.getenv('ENVIRONMENT'),
    dsn=os.getenv('SENTRY_DSN'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # To collect profiles for all profile sessions,
    # set `profile_session_sample_rate` to 1.0.
    profile_session_sample_rate=1.0,
    # Profiles will be automatically collected while
    # there is an active span.
    profile_lifecycle='trace',
    # Enable logs to be sent to Sentry
    enable_logs=True,
)
