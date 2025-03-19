import io
import base64
import requests

from fastapi import HTTPException
from rdkit import Chem
from rdkit.Chem import Draw
from app.core.constants import VALIDATOR_API_KEY


def get_smiles(product_name):
    
    if product_name:
        product_name = product_name.replace("'", "").replace('"', "")
    else:
        raise HTTPException(status_code=400, detail="Product name is required")
    
    try:
        url = f"https://8vzqr9wt22.execute-api.us-east-1.amazonaws.com/dev/smiles/{product_name}"
        headers = {"x-api-key": VALIDATOR_API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("smiles")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
