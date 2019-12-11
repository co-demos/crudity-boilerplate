
# CRUDity

### (currently in development)

------
### what is Crudity for ? 

A simple CRUD Restful API, backed with Elastic Search to have a scalable REST backend app

Two main concepts :
- DSI : DataSet Input, a corpus of documents and its metadata (the equivalent of the informations surrouding a table, its name, author, schema, ...)
- DSR : DataSet Raw, a document part of a DSI (the equivalent of a line of a table)

So to : 
- push a list of documents (DSRs) as part of a dataset (DSI)
- CRUD operations on a DSR
- CRUD operations on a DSI
- query a list of DSR of a DSI
- use pagination arguments when querying data
- data / schema agnostic

### stack

- language : python 3.7
- framework : FastAPI
- DB : Elastic Search and/or MongoDB

-----
### install app 

Go to your destination folder and type : 

```sh
git clone https://github.com/co-demos/crudity-boilerplate.git
python3 -m venv ven
source venv/bin/activate
pip install -r requirements.txt
```

Then copy and rename the `.example.env` files to create real `.env` files:

```bash
cp env-backend.example.env env-backend.env
cp env-elasticsearch.example.env env-elasticsearch.env
cp env-mongodb.example.env env-mongodb.env
```
You can edit those `.env` files and add real credentials inside. 


### notes

You must have `mongodb` and/or `ElasticSearch`running on your machine to use CRUDity

### run app 
```sh
uvicorn main:app --reload
```
then check : `http://127.0.0.1:8000/docs`

or 

```sh
python main.py --port=8001
```
then check : `http://localhost:8001/docs`

-----

### doc FastAPI 
cf : https://fastapi.tiangolo.com/

### doc uvicorn
cf : https://www.uvicorn.org/deployment/

### Doc Elastic search / Python 
cf : https://elasticsearch-py.readthedocs.io/en/master/


----

### Inspirations

- Solidata (open source)
- Dataiku 
- Tablo
- Forest Admin

--------

### logs

- **v.0.1 / 2019-12-11** : 
  first draft of the application. Tests with local ES db