from fastapi import FastAPI
from config import GITHUB_PROJECT_URL
from routers import roster_slots, stages, items, fighters
from fastapi_pagination import add_pagination
from tags import TAGS_METADATA
from utils import get_snippet


app = FastAPI(
    title='Super Smash Bros. Ultimate API',
    summary='**' + get_snippet('summary') + '**',
    description=get_snippet('description'),
    version='Beta',
    openapi_tags=TAGS_METADATA,
    openapi_external_docs={'description': 'See project on GitHub', 'url': GITHUB_PROJECT_URL}
)
add_pagination(app)
app.include_router(roster_slots.router)
app.include_router(stages.router)
app.include_router(items.router)
app.include_router(fighters.router)


@app.get('/')
async def root():
    return {"message": "Welcome to the Unofficial Super Smash Bros. Ultimate API! You can check out the documentation at /docs or /redoc."}
