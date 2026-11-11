import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from projects.jpais_core.routers.judicial_research import router as judicial_router

app = FastAPI(
    title="JPAIS Sovereign Judicial Research Gateway",
    description="Offline-capable Sovereign AI Gateway serving 9-Year Official Judicial Datasets (2017–2025), Econometric Forecasts, and Legal RAG for Supreme Court Research Staff.",
    version="2.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(judicial_router)

@app.get("/")
def root():
    return {
        "system": "JPAIS Sovereign Legal AI Gateway",
        "institution": "Mahkamah Agung Republik Indonesia",
        "status": "ONLINE",
        "documentation": "/docs",
        "endpoints": [
            "POST /v1/judicial/research-query",
            "GET  /v1/judicial/stats/summary",
            "GET  /v1/judicial/indicator/{code}"
        ]
    }

if __name__ == "__main__":
    uvicorn.run("projects.jpais_core.api:app", host="127.0.0.1", port=8001, reload=False)
