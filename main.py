from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import config
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
    openapi_external_docs={'description': 'See project on GitHub', 'url': config.REPO_URL}
)
add_pagination(app)
app.include_router(roster_slots.router)
app.include_router(stages.router)
app.include_router(items.router)
app.include_router(fighters.router)


@app.get('/', include_in_schema=False, response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse(url=request.scope['root_path'] + '/redoc')
