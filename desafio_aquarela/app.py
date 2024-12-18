from fastapi import FastAPI

from .routes import leader_route, position_route, user_route

app = FastAPI()

app.include_router(user_route.router)
app.include_router(leader_route.router)
app.include_router(position_route.router)
