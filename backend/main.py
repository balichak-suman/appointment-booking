import uvicorn
from medical_backend.asgi import app

# Export app for uvicorn CLI compatibility
app = app

if __name__ == "__main__":
    uvicorn.run("medical_backend.asgi:app", host="127.0.0.1", port=8001, reload=True)
