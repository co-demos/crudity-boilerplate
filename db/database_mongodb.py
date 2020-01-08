from log_config import log_, pformat
import inspect 

print()
log_.debug(">>> db/database_mongodb.py")

from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient, errors

from core.config import *

log_.debug("DB_MONGODB_MODE : %s", DB_MONGODB_MODE)


""" 
TUTORIALS MONGODB

cf : https://api.mongodb.com/python/current/tutorial.html#documents

"""

### MONGODB CLIENT

def create_mongodb_client(
  debug=False,
  mongodb_uri=MONGO_LOCAL_URI
  ):
  """Function to create an MongoDB client."""

  client = MongoClient(
    mongodb_uri
  )
  
  return client


def get_mongodb_database(
  mongodb=create_mongodb_client(),
  db_name=MONGO_DBNAME,  
  ) :
  mongodb_db = mongodb[ db_name ]
  return mongodb_db


def create_mongodb_collections(
  mongodb_db=get_mongodb_database(),
  collections=[
    MONGO_COLL_USERS,
    MONGO_COLL_DATASETS_INPUTS,
    MONGO_COLL_DATASETS_RAWS,
    MONGO_COLL_DATAMODELS_FIELDS,
    MONGO_COLL_DATAMODELS_TEMPLATES,
  ]
  ):
  """ create mongodb collection in database """

  collections_dict = {}

  for coll in collections :
    m_coll = mongodb_db[ coll ]
    collections_dict[ coll ] = m_coll

  return collections_dict





### INDEX / COLLECTION LEVEL

def create_mongodb_index(
  m_client=create_mongodb_client(),
  index_name=None
  ):
  """Functionality to create index."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  ### TO DO 
  res = {}

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status


def delete_mongodb_index(
  m_client=create_mongodb_client(),
  index_name=None
  ):
  """Delete an index by specifying the index name"""
  
  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  ### TO DO 
  res = {}
  
  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status






### UTILS

def build_mongodb_query( 
  query={},
  doc_uuid=None
  ):
  """Function to build a MONGODB search query."""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  ### TO DO ...
  search_query = {
  }

  return search_query



### DOCS LEVEL REQUESTS

# async def view_mongodb_document(
def view_mongodb_document(
  m_client_db=get_mongodb_database(),
  collection=None,
  index_name=None,
  doc_type=None,
  doc_uuid=None,
  ):
  """Function to view a MongoDB document."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client_db[ collection ]

  ### TO DO 
  res = db.find_one(
    { "_id" : doc_uuid },
    { "_id": 0 } ### projection fields
  )
  log_.debug( "res : \n%s", pformat(res))
  res_list = list(res)

  log_.debug( "res_list : \n%s", pformat(res_list))
  print()
  return res_list, status



# async def search_mongodb_documents(
def search_mongodb_documents(
  m_client_db=get_mongodb_database(),
  collection=None,
  index_name=None,
  doc_type=None,
  query={}
  ):
  """Function to make a MongoDB search query."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client_db[ collection ]

  ### TO DO 

  # build query
  doc_query = build_mongodb_query( query )
  
  per_page = query['per_page'].value
  from_item = ( query['page_n'] * per_page ) - per_page
  log_.debug( "from_item : %s", from_item )

  ### find document
  res = db.find( 
    doc_query,
    { "_id": 0 } ### projection fields
  )
  log_.debug( "res : \n%s", pformat(res))
  res_list = list(res)

  log_.debug( "res_list : \n%s", pformat(res_list))
  print()
  return res_list, status



# async def add_mongodb_document(
def add_mongodb_document(
  m_client_db=get_mongodb_database(),
  collection=None,
  index_name=None,
  doc_type=None,
  doc_uuid=None,
  doc_body=None
  ):
  """
  Funtion to add a MongoDB document by providing index_name,
  document type, document contents as doc and document id.
  """

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client_db[ collection ]

  ### TO DO 
  try : 
    res = db.insert_one(
      doc_body,
    )
    res_add = { 
      'item_id' : str(res.inserted_id),
      'operation' : "item added" 
    }
  except : 
    res = {}
    res_add = { 
      'item_id' : None,
      'operation' : 'not added...' 
    }
    status = {
      'status_code' : 500,
      'error' : "",
      'info' : ""
    }
  # log_.debug( "res : \n%s", pformat(res.__dict__))
  log_.debug( "res_add : \n%s", pformat(res_add))
  print()
  return res_add, status



# async def update_mongodb_document(
def update_mongodb_document(
  m_client_db=get_mongodb_database(),
  collection=None,
  index_name=None,
  doc_type=None,
  doc_uuid=None,
  doc_body=None,
  new=None
  ):
  """Function to edit a document either updating existing fields or adding a new field."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client_db[ collection ]

  ### TO DO
  
  # build query
  query = {}
  doc_query = build_mongodb_query( query, doc_uuid )
  
  # find and update
  try : 
    res = db.find_one_and_update(
      doc_query,
      { 
        '$set' : {

        }
      }
    ) 
    log_.debug( "res : \n%s", pformat(res))
    res_list = list(res)
  except : 
    res = {}
    status = {
      'status_code' : 500,
      'error' : "",
      'info' : "",
    }

  log_.debug( "res_list : \n%s", pformat(res_list))
  print()
  return res_list, status



# async def remove_mongodb_document(
def remove_mongodb_document(
  m_client_db=get_mongodb_database(),
  collection=None,
  index_name=None,
  doc_type=None,
  doc_uuid=None
  ):
  """Function to delete a specific document."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client_db[ collection ]

  ### TO DO 

  # build query
  # doc_query = build_mongodb_query( query, doc_uuid )
  doc_query = {
    f"{index_name}_uuid" : doc_uuid
  }
  log_.debug( "doc_query : \n%s", pformat( doc_query ))

  # find and delete document
  try :
    res = db.delete_one( 
      doc_query 
    )

  except : 
    res = {}
    status = {
      'status_code' : 500,
      'error' : "",
      'info' : "",
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



# async def remove_mongodb_many_documents(
def remove_mongodb_many_documents(
  m_client_db=get_mongodb_database(),
  collection=None,
  index_name=None,
  doc_type=None,
  ):
  """Function to delete a list of documents."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client_db[ collection ]

  ### TO DO 
  # build query
  query = {}
  doc_query = build_mongodb_query( query )

  # find and delete many document
  try :
    res = db.delete_many( doc_query )
  except :
    res = None
    status = {
      'status_code' : 500,
      'error' : "",
      'info' : "",
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status