from fastapi import FastAPI
from routers import roster_slots


app = FastAPI()
app.include_router(roster_slots.router)


@app.get('/')
async def root():
    return {"message": "Welcome to the Super Smash Bros. Ultimate API"}
