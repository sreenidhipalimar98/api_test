from fastapi import FastAPI
from shared import models, schemas, db, security
from networkflow_lambda import router as networkflow_router

app = FastAPI()
app.include_router(networkflow_router)

from mangum import Mangum
handler = Mangum(app)
