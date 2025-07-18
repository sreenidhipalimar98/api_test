from fastapi import FastAPI
from shared import models, schemas, db, security
from tenant_lambda.router import router as tenant_router


app = FastAPI()
app.include_router(tenant_router)

from mangum import Mangum
handler = Mangum(app)
