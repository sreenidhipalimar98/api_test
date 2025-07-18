
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.db import get_db
from shared.models import Pipe, Component, Fitting, Gas, Liquid, Unit
from shared.schemas import PipeOut, ComponentOut, FittingOut, GasOut, LiquidOut, UnitOut
from shared.security import verify_token

router = APIRouter()

@router.get("/masterdata/{resource_type}")
def get_masterdata(resource_type: str, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    # Permission check can be added here
    model_map = {
        "pipe": Pipe,
        "component": Component,
        "fitting": Fitting,
        "gas": Gas,
        "liquid": Liquid,
        "unit": Unit
    }
    Model = model_map.get(resource_type.lower())
    if not Model:
        raise HTTPException(status_code=404, detail="Resource type not found")
    data = db.query(Model).all()
    if(data.__len__()> 0):
         return data
    else:
        raise HTTPException(status_code=404, detail=f"No data found for resource type '{resource_type}'")
