"""HOMEBANKING — Backend FastAPI · Banca Internet Banco Andino.

Portal del CLIENTE. Proyecto separado del core bancario; se conecta a PostgreSQL.

Local:
    uvicorn main:app --reload --port 8002

Render:
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cfg_config import settings
from app.routes import route_auth, route_creditos, route_cuentas, route_operaciones

app = FastAPI(
    title="Banca Internet Banco Andino — Homebanking API",
    description=(
        "Portal del cliente de Banca Internet Banco Andino. "
        "Solo consultas y operaciones del cliente del portal "
        "(dcliente / usuarios_homebanking)."
    ),
    version="1.0.0",
)

# CORS para consumir el backend desde Vercel y desde desarrollo local.
# Render no tiene un botón para esto: se configura en el backend.
DEFAULT_CORS_ORIGINS = [
    "https://alfin-homebanking.vercel.app",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
]


def build_cors_origins() -> list[str]:
    origins = list(DEFAULT_CORS_ORIGINS)
    for origin in settings.cors_origins_list:
        if origin and origin not in origins:
            origins.append(origin)
    return origins


cors_origins = build_cors_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    # Permite también previews de Vercel, por ejemplo:
    # https://alfin-homebanking-git-main-usuario.vercel.app
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route_auth.router)
app.include_router(route_cuentas.router)
app.include_router(route_operaciones.router)
app.include_router(route_creditos.router)


@app.get("/", tags=["root"])
def raiz():
    return {
        "servicio": "Banca Internet Banco Andino — Homebanking API",
        "version": "1.0.0",
        "estado": "ok",
        "docs": "/docs",
        "puerto": settings.PORT,
        "cors_origins": cors_origins,
    }
