import base64
from typing import Any

from aiohttp.web_response import Response
from aiohttp.web import json_response as aiohttp_json_response
from pyparsing import Optional


def json_response(data: Any = None, status: str = 'OK') -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            'status': status,
            'data': data,
        }
    )


def error_json_response(http_status: int, status: str = 'error', message: str = None, data: dict = None):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": str(message),
            "data": data,
        })


def chech_basic_auth(raw_credentials: str, username: str, password: str) -> bool:
    credentials = base64.b64decode(raw_credentials).decode()        
    parts = credentials.split(':')
    if len(parts) != 2:
        return False
    return parts[0] == username and parts[1] == password 

