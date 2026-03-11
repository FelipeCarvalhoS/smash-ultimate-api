from fastapi import FastAPI
from routers import roster_slots, stages, items, fighters
from fastapi_pagination import add_pagination
from tags import TAGS_METADATA


app = FastAPI(openapi_tags=TAGS_METADATA)
add_pagination(app)
app.include_router(roster_slots.router)
app.include_router(stages.router)
app.include_router(items.router)
app.include_router(fighters.router)


@app.get('/')
async def root():
    return {"message": "Welcome to the Unofficial Super Smash Bros. Ultimate API! You can check out the documentation at /docs or /redoc."}
