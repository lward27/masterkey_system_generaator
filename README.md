# Master Key System Generator API with Database

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