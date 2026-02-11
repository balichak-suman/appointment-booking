import uvicorn
from medical_backend.asgi import app

# Export app for uvicorn CLI compatibility
app = app

if __name__ == "__main__":
    uvicorn.run("medical_backend.asgi:app", host="0.0.0.0", port=8000, reload=True)
