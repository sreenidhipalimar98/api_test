
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from shared.security import verify_token
from fastapi import HTTPException, Depends
load_dotenv()


Base = declarative_base()

# Global DB URL
GLOBAL_DB_URL = f"postgresql+psycopg2://{os.getenv('dev_username')}:{os.getenv('dev_password')}@{os.getenv('dev_host')}:{os.getenv('dev_port')}/{os.getenv('dev_dbname')}"

global_engine = create_engine(GLOBAL_DB_URL, pool_pre_ping=True)
GlobalSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=global_engine)

from sqlalchemy.exc import OperationalError, ProgrammingError
from fastapi import HTTPException, status
 
def get_tenant_engine(tenant_db_name: str):
    url = f"postgresql+psycopg2://{os.getenv('dev_username')}:{os.getenv('dev_password')}@{os.getenv('dev_host')}:{os.getenv('dev_port')}/{tenant_db_name}"
    print(url)
    return create_engine(url, pool_pre_ping=True)

def get_db(token: dict = Depends(verify_token)):
    tenant_id = token.get("custom:tenant_id")
    print(tenant_id)
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID missing in token")
    
    try:
        engine = get_tenant_engine(tenant_id)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Ping DB to check if it exists
        # db.execute("SELECT 1")
    except OperationalError as e:
         raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Tenant database '{tenant_id}' is not reachable or does not exist",
        )
    except ProgrammingError as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database programming error occurred"
        )
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected database error occurred: '{str(e)}'"
        )

    try:
        yield db
    finally:
        db.close()

