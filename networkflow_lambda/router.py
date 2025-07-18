
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from shared.db import get_db
from shared.models import NetworkFlow
from shared.schemas import NetworkFlowCreate, NetworkFlowOut
from shared.security import verify_token
import boto3
import os
import uuid

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)
S3_BUCKET = os.getenv('AWS_S3_BUCKET')

router = APIRouter()

@router.post("/network-flow/create", response_model=NetworkFlowOut)
async def create_network_flow(
    name: str = Form(...),
    flow_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    user_id = token.get("user_id")
    s3_key = f"network_flows/{user_id}_{flow_file.filename}"
    s3_client.upload_fileobj(flow_file.file, S3_BUCKET, s3_key, ExtraArgs={"ACL": "public-read"})
    flow_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
    new_flow = NetworkFlow(
        name=name,
        flow_url=flow_url,
        is_active=True
    )
    db.add(new_flow)
    db.commit()
    db.refresh(new_flow)
    return new_flow

@router.get("/network-flow/{id}", response_model=NetworkFlowOut)
def get_network_flow(id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    flow = db.query(NetworkFlow).filter(NetworkFlow.id == id).first()
    if not flow:
        raise HTTPException(status_code=404, detail="NetworkFlow not found")
    return flow

@router.put("/network-flow/update/{id}", response_model=NetworkFlowOut)
def update_network_flow(id: uuid.UUID, flow: NetworkFlowCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    db_flow = db.query(NetworkFlow).filter(NetworkFlow.id == id).first()
    if not db_flow:
        raise HTTPException(status_code=404, detail="NetworkFlow not found")
    for k, v in flow.dict().items():
        setattr(db_flow, k, v)
    db.commit()
    db.refresh(db_flow)
    return db_flow

@router.delete("/network-flow/delete/{id}", status_code=204)
def delete_network_flow(id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    db_flow = db.query(NetworkFlow).filter(NetworkFlow.id == id).first()
    if not db_flow:
        raise HTTPException(status_code=404, detail="NetworkFlow not found")
    db.delete(db_flow)
    db.commit()
    return

@router.get("/network-flow/all", response_model=list[NetworkFlowOut])
def get_all_network_flows(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    flows = db.query(NetworkFlow).filter(NetworkFlow.is_active == True).all()
    return flows
