from typing import List, Dict, Optional
from pydantic import ValidationError

from fastapi import APIRouter, Depends, HTTPException


from models.dataset_raw import Dsr, DsrCreate, DsrUpdate
from models.parameters import *


router = APIRouter()

# @router.get("/list")
# async def root():
#   return {"message": "Hello World"}

@router.get("/dsi/{dsi_oid}")
async def read_dsi_items(dsi_oid):
  return {"dsi_id": dsi_oid}


@router.get("/dsi/{dsi_oid}/dsr/{dsr_oid}")
async def read_item(dsi_oid, item_id):
  return {"dsr_oid": dsr_oid}

@router.post("/dsi/{dsi_oid}/dsr/{dsr_oid}")
async def create_item(dsi_oid, dsr_oid):
  return {"dsr_oid": dsr_oid}

@router.put("/dsi/{dsi_oid}/dsr/{dsr_oid}")
async def update_item(dsi_oid, dsr_oid):
  return {"dsr_oid": dsr_oid}

@router.delete("/dsi/{dsi_oid}/dsr/{dsr_oid}")
async def delete_item(dsi_oid, dsr_oid):
  return {"dsr_oid": dsr_oid}