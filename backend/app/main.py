from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_sweets import router as sweets_router
from app.db.mongo import lifespan

app = FastAPI(title="Sweet Shop API", lifespan=lifespan)

origins = [o.strip() for o in settings.allowed_origins_csv.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(sweets_router)


@app.get("/")
async def root():
	return {"status": "ok"}
