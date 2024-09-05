from fastapi import FastAPI
from routes.file_route import router as files

def init_routes(app: FastAPI) -> None:
	app.include_router(files)
