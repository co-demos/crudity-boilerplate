
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

- **with uvicorn from shell** :

```sh
uvicorn main:app --reload
```
then check : [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

... or ... 

```sh
uvicorn main:app --reload --host=localhost --port=8000
```


- **with python from shell**

```sh
python main.py --host=localhost --port=8001 --autoreload=true
```

then check : [`http://localhost:8001/docs`](http://localhost:8001/docs)


- **CLI arguments**

*note* : running CRUDity with Python allows you to inject some parameters like `--port` with the command line (see the `main.py` file for the list of the CLI parameters you can use).

```
'--mode' (default='dev')         : The <mode> you need to run the app : default | dev | testing | preprod | production
'--autoreload' (default='false') : The <autoreload> mode you want the app to run on : true | false
'--auth' (default='dev')         : The <auth> mode you need to run the app : no_auth | dev | default | default_docker | server | server_docker | distant_preprod | distant_prod
'--host' (default='localhost')   : The <host> name you want the app to run on : <IP_NUMBER>
'--port' (default='8000')        : The <port> number you want the app to run on : <PORT_NUMBER>
'--esdb' (default='local')       : The <esdb> you need to run the app : disabled | local | distant | server
'--mongodb' (default='local')    : The <mongodb> you need to run the app : disabled | local | distant | server
'--docker' (default='false')     : Are you running the app with <docker> : docker_off | docker_on
'--https' (default='false')      : The <https> mode you want the app to run on : true | false
```

-----

### Run tests with pytest



```bash
source venv/bin/activate
pytest ./tests/
```

or `pytest ./tests/ -v` for verbose

or `pytest ./tests/ -s` for all outputs

or `pytest ./tests/api/api_v1/test_dataset_inputs_endpoints.py ` for test from a specific test file

or `pytest ./tests/api/api_v1/test_dataset_inputs_endpoints.py::test_get_one_dsi ` for test from a function in a specific test file

or `pytest ./tests/ -k inputs -x ` for tests from files containing 'inputs' keyword

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