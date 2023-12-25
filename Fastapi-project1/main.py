from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.app import app

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")