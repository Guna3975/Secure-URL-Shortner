# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.routes.auth_routes import router as auth_router
from app.routes.url_routes import router as url_router

app = FastAPI(title="SecureShort Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(url_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

print("✅ All routes registered successfully!") 