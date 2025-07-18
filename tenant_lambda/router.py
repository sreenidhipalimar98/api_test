
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from shared.db import get_db
from shared.models import Tenant
from shared.schemas import TenantOut
import boto3
import os
from sqlalchemy import create_engine, text
from datetime import datetime
import uuid


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
S3_BUCKET = os.getenv('AWS_S3_BUCKET')

router = APIRouter()

@router.post("/tenant/createTenant", response_model=TenantOut)
async def create_tenant(
    tenant_id: str = Form(...),
    company_name: str = Form(None),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if db_tenant:
        raise HTTPException(status_code=409, detail="Tenant ID in use")
    logo_url = None
    if logo:
        s3_key = f"tenant_logos/{tenant_id}_{logo.filename}"
        s3_client.upload_fileobj(logo.file, S3_BUCKET, s3_key, ExtraArgs={"ACL": "public-read"})
        logo_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
    new_tenant = Tenant(
        tenant_id=tenant_id,
        company_name=company_name,
        logo_url=logo_url,
        created_by=uuid.uuid4(),  # Assuming created_by is a UUID
        created_at=datetime.utcnow(),
        
    )
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)

    # --- Create a new database for the tenant ---
    POSTGRES_USER = os.getenv('dev_username')
    POSTGRES_PASSWORD = os.getenv('dev_password')
    POSTGRES_SERVER = os.getenv('dev_host')
    POSTGRES_PORT = os.getenv('dev_port', "5432")
    POSTGRES_DB = os.getenv('dev_dbname')
    admin_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    db_name = tenant_id.lower()
    with engine.connect() as conn:
        conn.execute(text(f'CREATE DATABASE "{db_name}"'))

    # --- Create essential tenant tables directly (not via Alembic) ---
    tenant_db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{db_name}"
    tenant_engine = create_engine(tenant_db_url)
    create_table_sql = [
        '''CREATE TABLE IF NOT EXISTS "user" (
            id UUID PRIMARY KEY,
            name VARCHAR(64),
            email VARCHAR(64) UNIQUE,
            role_id UUID,
            is_active BOOLEAN,
            created_at TIMESTAMP,
            created_by UUID,
            modified_at TIMESTAMP,
            modified_by UUID
        )''',
        '''CREATE TABLE IF NOT EXISTS role (
            id UUID PRIMARY KEY,
            name VARCHAR(64),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP,
            created_by UUID,
            modified_at TIMESTAMP,
            modified_by UUID
        )''',
        '''CREATE TABLE IF NOT EXISTS permission (
            id UUID PRIMARY KEY,
            code VARCHAR(64) UNIQUE,
            description VARCHAR(256),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP,
            created_by UUID,
            modified_at TIMESTAMP,
            modified_by UUID
        )''',
        '''CREATE TABLE IF NOT EXISTS role_permission (
            id UUID PRIMARY KEY,
            role_id UUID REFERENCES role(id),
            permission_id UUID REFERENCES permission(id),
            created_at TIMESTAMP,
            created_by UUID,
            modified_at TIMESTAMP,
            modified_by UUID
        )''',
        '''CREATE TABLE IF NOT EXISTS network_flow (
            id UUID PRIMARY KEY,
            name VARCHAR(64),
            flow_url VARCHAR(256),
            is_active BOOLEAN,
            created_at TIMESTAMP,
            created_by UUID,
            modified_at TIMESTAMP,
            modified_by UUID
        )'''
    ]
    with tenant_engine.begin() as conn:
     for stmt in create_table_sql:
        conn.execute(text(stmt))

    return new_tenant
