
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from shared.db import get_db
from shared.models import User, Role, Permission, RolePermission
from shared.schemas import UserCreate, UserOut, RoleCreate, RoleOut, PermissionCreate, PermissionOut, RolePermissionCreate, RolePermissionOut
from shared.security import verify_token
import uuid
from datetime import datetime

router = APIRouter()

# --- USER CRUD ---
@router.post("/user/createUser", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    tenant_id = token.get("custom:tenant_id")
    user_id = token.get("sub")
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Invalid token: tenant_id missing")
    db_user = db.query(User).filter(User.email == user.email or User.id == user_id).first()
    if db_user:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = User(**user.dict())
    new_user.id =  user_id
    new_user.is_active = True
    new_user.created_at = datetime.utcnow()
    new_user.created_by = user_id
    new_user.modified_at = None
    new_user.modified_by = None
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/getUser", response_model=UserOut)
def get_user(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    tenant_id = token.get("custom:tenant_id")
    user_id = token.get("sub")
    if not tenant_id or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: tenant_id or user_id missing")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/user/updateUser", response_model=UserOut)
def update_user(user: UserCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    tenant_id = token.get("custom:tenant_id")
    user_id = token.get("sub")
    if not tenant_id or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: tenant_id or user_id missing")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for k, v in user.dict().items():
        setattr(db_user, k, v)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/user/deleteUser", status_code=200) 
def delete_user(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    tenant_id = token.get("custom:tenant_id")
    user_id = token.get("sub")
    if not tenant_id or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: tenant_id or user_id missing")
    db_user = db.query(User).filter(User.id == user_id or User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}

@router.get("/user/all", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    tenant_id = token.get("custom:tenant_id")
    user_id = token.get("sub")
    role = token.get("role")
    if not tenant_id or not user_id or not role:
        raise HTTPException(status_code=401, detail="Invalid token: tenant_id, user_id, or role missing")
    users = db.query(User).filter(User.is_active == True).all()
    return users

# --- ROLE CRUD ---
@router.post("/role/create", response_model=RoleOut)
def create_role(role: RoleCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    tenant_id = token.get("custom:tenant_id")
    user_id = token.get("sub")
    role_name = token.get("role")
    if not tenant_id or not user_id or not role_name:
        raise HTTPException(status_code=401, detail="Invalid token: tenant_id, user_id, or role missing")
    new_role = Role(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.get("/role/{id}", response_model=RoleOut)
def get_role(id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    role = db.query(Role).filter(Role.id == id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/role/all", response_model=list[RoleOut])
def get_all_roles(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    roles = db.query(Role).filter(Role.is_active == True).all() if hasattr(Role, 'is_active') else db.query(Role).all()
    return roles

@router.put("/role/update/{id}", response_model=RoleOut)
def update_role(id: uuid.UUID, role: RoleCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    db_role = db.query(Role).filter(Role.id == id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    for k, v in role.dict().items():
        setattr(db_role, k, v)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/role/delete/{id}", status_code=204)
def delete_role(id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    db_role = db.query(Role).filter(Role.id == id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    if hasattr(db_role, 'is_active'):
        db_role.is_active = False
    else:
        db.delete(db_role)
    db.commit()
    return

# --- PERMISSION CRUD ---
@router.post("/permission/create", response_model=PermissionOut)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    new_permission = Permission(**permission.dict())
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

@router.get("/permission/{id}", response_model=PermissionOut)
def get_permission(id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    permission = db.query(Permission).filter(Permission.id == id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.get("/permission/all", response_model=list[PermissionOut])
def get_all_permissions(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    permissions = db.query(Permission).all()
    return permissions

@router.put("/permission/update/{id}", response_model=PermissionOut)
def update_permission(id: uuid.UUID, permission: PermissionCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    db_permission = db.query(Permission).filter(Permission.id == id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    for k, v in permission.dict().items():
        setattr(db_permission, k, v)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.delete("/permission/delete/{id}", status_code=204)
def delete_permission(id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    db_permission = db.query(Permission).filter(Permission.id == id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(db_permission)
    db.commit()
    return

# --- ROLEPERMISSION CRUD ---
@router.post("/role-permission/assign", response_model=RolePermissionOut)
def assign_role_permission(rp: RolePermissionCreate, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    new_rp = RolePermission(**rp.dict())
    db.add(new_rp)
    db.commit()
    db.refresh(new_rp)
    return new_rp

@router.delete("/role-permission/remove/{id}", status_code=204)
def remove_role_permission(id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    rp = db.query(RolePermission).filter(RolePermission.id == id).first()
    if not rp:
        raise HTTPException(status_code=404, detail="RolePermission not found")
    db.delete(rp)
    db.commit()
    return

@router.get("/role-permission/{role_id}", response_model=list[RolePermissionOut])
def get_role_permissions(role_id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    rps = db.query(RolePermission).filter(RolePermission.role_id == role_id).all()
    return rps
