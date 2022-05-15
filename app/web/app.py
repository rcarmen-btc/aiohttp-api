from typing import Optional

from aiohttp.web import AiohttpApplication, run_app as aiohttp_run_app, View as AiohttpView, Request as AiohttpRequest
from app.web.routes import setup_routes
from store import setup_accessors
from store.crm.accessor import CrmAccessor


app = AiohttpApplication()


class Application(AiohttpApplication):
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = None


class Request(AiohttpRequest):
    @property
    def app(self) -> "Application":
        return super().app


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request
    

def run_app():
    setup_routes(app)
    setup_accessors(app)
    aiohttp_run_app(app)