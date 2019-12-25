
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
- data indexing in Elastic Search
- data versionning in MongoDB


### stack

- language : [python 3.7](https://docs.python.org/3.7/)
- framework : [FastAPI](https://fastapi.tiangolo.com/)
- DB : [Elastic Search](https://www.elastic.co) and/or [MongoDB](https://www.mongodb.com/)

### dependencies

You must have `mongodb` and/or `ElasticSearch` running on your machine to use CRUDity. Check | Edit your `.env` files (see below)

-----

### Install CRUDity 

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


### run CRUDity 
```sh
uvicorn main:app --reload
```
then check : [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

... or* ... 

```sh
python main.py --port=8001
```
then check : [`http://localhost:8001/docs`](http://localhost:8001/docs)

*note : if you run CRUdity with Python instead of uvicorn the hot reload will be disabled. Also running CRUDity with Python allows you to inject some parameters like `--port` with the command line (see the `main.py` file for the list of the CLI parameters you can use).  

-----

### Run tests with pytest



```bash
source venv/bin/activate
pytest ./tests/
```

or `pytest ./tests/ -v` for verbose
or `pytest ./tests/ -s` for all outputs


-----

### doc FastAPI 
cf : https://fastapi.tiangolo.com/

### doc uvicorn
cf : https://www.uvicorn.org/deployment/

### doc Elastic search / Python 
cf : https://elasticsearch-py.readthedocs.io/en/master/


----

### (currently in development)
### Push your first datasets

You can store your dataseets in the `./_data` folder.

Use the Jupyter notebooks of your choice from the `./_notebooks` folder to push datasets from `./_data` to CRUDity...

----

### Inspirations

- Solidata (open source)
- Datasette (open source)
- CSVapi
- AirTable
- Dataiku 
- Tablo
- Forest Admin

--------

### logs

- **v.0.1 / 2019-12-11** : 
  first draft of the application. Adding models for parameters on endpoints. Discovering FastAPI. Tests with local ES db... 