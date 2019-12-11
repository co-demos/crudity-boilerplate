from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException

from models.response import ResponseBase, ResponseDataBase
from models.dataset_raw import Dsr, DsrCreate, DsrUpdate, DsrData
from models.parameters import *


router = APIRouter()


@router.get("/dsi/{dsi_uuid}")
async def read_dsi_items(
  dsi_uuid: uuid.UUID,
  dsr_uuid: list = dsr_uuid,
  commons: dict = Depends(common_parameters)
  ):
  """ get paginated DSRs from a DSI """

  time_start = datetime.now()
  query = { 
    'dsr_uuid': dsr_uuid,
    **commons
  }


  response = {"dsi_id": dsi_uuid}

  return response




@router.get("/dsi/{dsi_uuid}/dsr/{dsr_uuid}")
async def read_dsr_item(
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  ):
  """ get one DSR from a DSI """


  response =  {"dsr_uuid": dsr_uuid}
  return response


@router.post("/dsi/{dsi_uuid}/dsr")
async def create_dsr_item(
  *,
  dsi_uuid: uuid.UUID,
  item_data: DsrData
  ):
  """ post one DSR into a DSI """



  response =  {
    "dsr_uuid": dsr_uuid,
    "item_data": item_data
  }
  return response


@router.put("/dsi/{dsi_uuid}/dsr/{dsr_uuid}")
async def update_dsr_item(
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  ):
  """ update one DSR from a DSI """



  response =  {"dsr_uuid": dsr_uuid}
  return response


@router.delete("/dsi/{dsi_uuid}/dsr/{dsr_uuid}")
async def delete_dsr_item(
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  ):
  """ delete one DSR from a DSI """




  response =  {"dsr_uuid": dsr_uuid}  
  return response