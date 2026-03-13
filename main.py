from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import config
from routers import roster_slots, stages, items, fighters
from fastapi_pagination import add_pagination
from tags import TAGS_METADATA
from utils import get_snippet
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


app = FastAPI(
    title='Super Smash Bros. Ultimate API',
    summary='**' + get_snippet('summary') + '**',
    description=get_snippet('description'),
    version='Beta',
    root_path='/beta',
    openapi_tags=TAGS_METADATA,
    openapi_external_docs={'description': 'See project on GitHub', 'url': config.REPO_URL},
    docs_url=None,
    redoc_url=None,
)
app.openapi_url = app.root_path + '/openapi.json'

add_pagination(app)
app.include_router(roster_slots.router)
app.include_router(stages.router)
app.include_router(items.router)
app.include_router(fighters.router)


@app.get('', include_in_schema=False)
async def root(request: Request) -> RedirectResponse:
    return RedirectResponse(url=request.scope['root_path'] + '/redoc')


@app.get('/redoc', include_in_schema=False)
async def redoc() -> HTMLResponse:
    return get_redoc_html(openapi_url=app.openapi_url, title=app.title, redoc_favicon_url=config.FAVICON_URL)


@app.get('/docs', include_in_schema=False)
async def docs() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title, swagger_favicon_url=config.FAVICON_URL)