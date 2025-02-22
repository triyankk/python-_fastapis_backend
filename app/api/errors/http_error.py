from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_error_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "http_error"
            }
        }
    )
