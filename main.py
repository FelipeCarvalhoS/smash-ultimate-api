from fastapi import FastAPI
from fastapi.responses import RedirectResponse
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
    root_path='/beta',
    openapi_tags=TAGS_METADATA,
    openapi_external_docs={'description': 'See project on GitHub', 'url': GITHUB_PROJECT_URL}
)
add_pagination(app)
app.include_router(roster_slots.router)
app.include_router(stages.router)
app.include_router(items.router)
app.include_router(fighters.router)


@app.get('/', include_in_schema=False, response_class=RedirectResponse)
async def root():
    return RedirectResponse('/redoc')
