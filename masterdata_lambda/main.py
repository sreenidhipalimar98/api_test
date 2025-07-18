from fastapi import FastAPI
from shared import models, schemas, db, security
from masterdata_lambda.router import router as masterdata_router

app = FastAPI()
app.include_router(masterdata_router)

from mangum import Mangum
handler = Mangum(app)
