from fastapi import FastAPI
from .router import routers

app = FastAPI()

# Import all router
for r in routers:
    app.include_router(r)
