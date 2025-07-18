
import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

load_dotenv()

# Load AWS Cognito config from environment variables
COGNITO_REGION = os.environ.get("COGNITO_REGION")
COGNITO_USERPOOL_ID = os.environ.get("COGNITO_USERPOOL_ID")
COGNITO_APP_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")
if not all([COGNITO_REGION, COGNITO_USERPOOL_ID, COGNITO_APP_CLIENT_ID]):
    raise RuntimeError("Missing Cognito configuration in environment variables. Please set COGNITO_REGION, COGNITO_USERPOOL_ID, and COGNITO_APP_CLIENT_ID in your .env file.")
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}"
COGNITO_JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_cognito_public_keys():
    resp = requests.get(COGNITO_JWKS_URL)
    resp.raise_for_status()
    return resp.json()["keys"]

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # headers = jwt.get_unverified_header(token)
        # kid = headers.get("kid")
        # if not kid:
        #    raise HTTPException(status_code=401, detail="Missing 'kid' in token header")
        # keys = get_cognito_public_keys()
        # key = next((k for k in keys if k["kid"] == kid), None)
        # if not key:
        #     raise HTTPException(status_code=401, detail="Public key not found in Cognito")
        # public_key = jwt.construct_rsa_public_key(key)
        # payload = jwt.decode(
        #     token,
        #     public_key,
        #     algorithms=[key["alg"]],
        #     audience=COGNITO_APP_CLIENT_ID,
        #     issuer=COGNITO_ISSUER
        # )
        # return payload
        payload = jwt.decode(
            token,
            key="",  # no key needed
           options={
                "verify_signature": False,  # skip signature check
                "verify_exp": False,         # skip expiration check
                "verify_aud": False  # ✅ Disable audience check
            }
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
