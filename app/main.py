from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse   # ← ADD THIS LINE

from app.routes import auth_routes

app = FastAPI(title="SecureShort Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:*",
        "http://127.0.0.1:*",
        "*"                 # ← safe for local dev only
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")