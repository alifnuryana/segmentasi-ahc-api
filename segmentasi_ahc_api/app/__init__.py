from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.gzip import GZipMiddleware

from segmentasi_ahc_api.app.database import create_db_and_tables
from segmentasi_ahc_api.app.features.upload_csv.routes import upload_csv_router
from segmentasi_ahc_api.app.templates import TemplateDep


def create_app() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        from segmentasi_ahc_api.app.models.clusters import Cluster
        from segmentasi_ahc_api.app.models.customers import Customer
        from segmentasi_ahc_api.app.models.products import Product
        from segmentasi_ahc_api.app.models.segmentations import Segmentation
        from segmentasi_ahc_api.app.models.transactions import Transaction, TransactionItem

        create_db_and_tables()

    app.add_middleware(GZipMiddleware)

    @app.get("/", response_class=HTMLResponse)
    async def index(
            request: Request,
            template: TemplateDep
    ):
        return template.TemplateResponse(
            request=request, name="index.html", context={"title": "Segmentasi Pelanggan Menggunakan AHC"}
        )

    app.mount('/static', StaticFiles(directory="static"), name='static')

    app.include_router(upload_csv_router)

    return app
