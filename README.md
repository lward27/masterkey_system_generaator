# Master Key System Generator API with Database

Make sure to check out **db_setup.md** before attempting to use the API. DB Connection string is currently hard coded and set up for local dev, so be sure to update in your own copy.

## To build docker image use:

```bash
docker build . -t masterkey_system_generator 
```
To run with docker use:
```bash
docker run -p 0.0.0.0:8000:8000 masterkey_system_generator
```
Access the API via `http://127.0.0.1:8000/docs`

## Without Docker
 - note: you will still need to setup the DB using docker or some other method
To run mks api, run these commands (python3.10+ required)
```bash
python3.10 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements
cd src
python3 -m pip install .
python3 masterkey_system_generator
# Exit virtual environment by typing: deactivate
```

NOTES: it's not the db that takes for ever when retrieving a large system, it's the rendering of the data on the page.