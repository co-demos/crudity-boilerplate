from log_config import log_, pformat
import inspect 

print()
log_.debug(">>> db/database_mongodb.py")

from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient

from core.config import *

log_.debug("DB_MONGODB_MODE : %s", DB_MONGODB_MODE)


""" 
TUTORIALS MONGODB

cf : https://api.mongodb.com/python/current/tutorial.html#documents

"""

### MONGODB CLIENT

def create_mongodb_client(
  debug=False,
  ):
  """Function to create an MongoDB client."""

  client = MongoClient(
    'mongodb://localhost:27017/'
  )
  
  return client


### INDEX LEVEL

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
  m_client=create_mongodb_client(),
  database=None,
  index_name=None,
  doc_type=None,
  doc_uuid=None,
  ):
  """Function to view a MongoDB document."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client[ database ]

  ### TO DO 
  res = db.find_one(
    { "_id" : doc_uuid }
  )

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



# async def search_mongodb_documents(
def search_mongodb_documents(
  m_client=create_mongodb_client(),
  database=None,
  index_name=None,
  doc_type=None,
  query={}
  ):
  """Function to make a MongoDB search query."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client[ database ]

  ### TO DO 

  # build query
  doc_query = build_mongodb_query( query )

  ### find document
  res = db.find( doc_query )

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



# async def add_mongodb_document(
def add_mongodb_document(
  m_client=create_mongodb_client(),
  database=None,
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

  db = m_client[ database ]

  ### TO DO 
  res = db.insert_one(
    doc_body
  )

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



# async def update_mongodb_document(
def update_mongodb_document(
  m_client=create_mongodb_client(),
  database=None,
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

  db = m_client[ database ]

  ### TO DO
  
  # build query
  query = {}
  doc_query = build_mongodb_query( query, doc_uuid )
  
  # find and update
  res = db.find_one_and_update(
    doc_query,
    { 
      '$set' : {

      }
    }
  ) 


  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



# async def remove_mongodb_document(
def remove_mongodb_document(
  m_client=create_mongodb_client(),
  database=None,
  index_name=None,
  doc_type=None,
  doc_uuid=None
  ):
  """Function to delete a specific document."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client[ database ]

  ### TO DO 

  # build query
  query = {}
  doc_query = build_mongodb_query( query, doc_uuid )

  # find and delete document
  res = db.delete_one( doc_query )

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



# async def remove_mongodb_many_documents(
def remove_mongodb_many_documents(
  m_client=create_mongodb_client(),
  database=None,
  index_name=None,
  doc_type=None,
  ):
  """Function to delete a list of documents."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  db = m_client[ database ]

  ### TO DO 
  # build query
  query = {}
  doc_query = build_mongodb_query( query )

  # find and delete many document
  res = db.delete_many( doc_query )

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status