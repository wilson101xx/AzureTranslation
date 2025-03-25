from fastapi import FastAPI
from src.api.routes.translation import router as translation_router
from src.api.routes.languages import router as languages_router

app = FastAPI()

# Include API routes
app.include_router(translation_router, prefix="/translation", tags=["Translation"])
app.include_router(languages_router, prefix="/languages", tags=["Languages"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
