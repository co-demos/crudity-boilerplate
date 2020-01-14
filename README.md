
# CRUDo

### (currently in development)

------
### what is CRUDo for ? 

A simple CRUD Restful API, backed with ElasticSearch to have a scalable REST backend app, and MonngoDB for versionning

Two main concepts :
- **DSI** : or `DataSet Input`, a corpus of documents and its metadata (the equivalent of the informations surrouding a table/spreadsheet, its name, author, schema, ...)
- **DSR** : or `DataSet Raw`, a document part of a DSI (the equivalent of a line of a table/spreadsheet)

So to : 
- push a list of documents (DSRs) as part of a dataset (DSI)
- CRUD operations on a DSI
- CRUD operations on a DSR
- query a list of DSR of a DSI
- use pagination arguments when querying data
- data / schema agnostic
- data indexing in Elastic Search
- data versionning in MongoDB


### stack

- language : [python 3.7](https://docs.python.org/3.7/)
- framework : [FastAPI](https://fastapi.tiangolo.com/)
- tests : [Pytest](https://docs.pytest.org/en/latest/)
- databases : [Elastic Search](https://www.elastic.co) and/or [MongoDB](https://www.mongodb.com/)

### dependencies

You must have `ElasticSearch` and/or `mongodb` running on your machine to use CRUDo. Check | Edit your `.env` files (see below)

-----

### Install CRUDo

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


### run CRUDo

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

*note* : running CRUDo with Python allows you to inject some parameters like `--port` with the command line (see the `main.py` file for the list of the CLI parameters you can use).

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

### Run tests with Pytest


#### - Run all tests

- **run tests :**
  ```bash
  source venv/bin/activate
  pytest ./tests/
  ```

- **output :** 
  `pytest ./tests/ -s` for all outputs

#### - Run some of the tests


- **by file name :** 
  `pytest ./tests/api/api_v1/test_dataset_inputs_endpoints.py ` for test from a specific test file

- **by function name :** 
  `pytest ./tests/api/api_v1/test_dataset_inputs_endpoints.py::test_get_one_dsi ` for test from a function in a specific test file

- **by keyword :**
  `pytest ./tests/ -k inputs` for tests from files containing 'inputs' keyword
  or `pytest ./tests/ -k 'update and input'`

- **by marker name :** 
  `pytest ./tests/ -m delete ` for tests marked with 'delete' keyword


#### - Configuration

You will find a `pytest.ini` configuration file at the root of the repository. For more information please refer to the [Pytest documentation](https://docs.pytest.org/en/latest)


-----

### Documentations
#### doc FastAPI 
cf : https://fastapi.tiangolo.com/

#### doc Uvicorn
cf : https://www.uvicorn.org/deployment/

#### doc Elastic search / Python 
cf : https://elasticsearch-py.readthedocs.io/en/master/







----

### (currently in development)
### Push your first datasets

You can store your dataseets in the `./_data` folder.

Use the Jupyter notebooks of your choice from the `./_notebooks` folder to push datasets from `./_data` to CRUDity...

----

### Inspirations

CRUDo aims to be a generic backend for exposing data. It could be though as an alternative or a backend for apps such as : 

- Solidata (open source)
- Datasette (open source)
- CSVapi
- AirTable
- Dataiku 
- Tablo
- Forest Admin

--------

### logs

- **v.0.1.1 / 2020-01-14** : 
  adding pytests drafts and modifications on main endpoints... 

- **v.0.1 / 2019-12-11** : 
  first draft of the application. Adding models for parameters on endpoints. Discovering FastAPI. Tests with local ES db... 