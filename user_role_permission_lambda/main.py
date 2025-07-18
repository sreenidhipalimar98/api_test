from fastapi import FastAPI
from shared import models, schemas, db, security
from user_role_permission_lambda.router import router as user_router

app = FastAPI()
app.include_router(user_router)

# AWS Lambda handler
from mangum import Mangum
handler = Mangum(app)
