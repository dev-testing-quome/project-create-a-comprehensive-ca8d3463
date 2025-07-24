import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .routers import cases, clients, users # Add other routers as needed
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal Case Management System", openapi_url="/openapi.json", docs_url="/docs")

origins = ["http://localhost:3000", "http://localhost", "*"] # Update with your frontend URLs

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(cases.router)
app.include_router(clients.router)
app.include_router(users.router) # Add other routers here


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Exception handling
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Static file serving for frontend
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/{file_path:path}")
    async def serve_frontend(file_path: str):
        if file_path.startswith("api/") or file_path.startswith("static"):
            return None  # Let API routes and static files handle it
        static_file = os.path.join("static", file_path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
        return FileResponse("static/index.html")  # SPA routing


# Dependency injection for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
