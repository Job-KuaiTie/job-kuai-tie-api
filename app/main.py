from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .router import routers

app = FastAPI()

# Import all router
for r in routers:
    app.include_router(r)

# Allowed to make requests from different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or "*" for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
