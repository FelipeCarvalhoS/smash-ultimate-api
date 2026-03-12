from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
R2_URL = os.getenv('R2_URL')
GITHUB_PROJECT_URL = os.getenv('GITHUB_PROJECT_URL')
