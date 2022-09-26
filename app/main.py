import logging
import time
import uuid
from urllib.request import Request

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import app.urlunshortener as unshortener

# Logging related
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

# Middlewares
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]
app = FastAPI(middleware=middleware)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    uid = uuid.uuid4()
    logger.info(f"request_id={uid} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"request_id={uid} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


class URL(BaseModel):
    url: str


@app.get("/health-check")
async def health_check():
    logger.info("App is up and running")
    return {"message": "Working"}


@app.post("/unshorten")
async def unshorten_url(url: URL):
    unshortened_url = ""
    sanitized_url = ""
    status, unshortened_url = unshortener.unshorten_url(url.url)
    if status:
        status, sanitized_url = unshortener.sanitize_url(unshortened_url)
    return {"success": status, "unshortened_url": unshortened_url, "sanitized_url": sanitized_url}
