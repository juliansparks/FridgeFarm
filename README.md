# Web App & REST API

## Running for development

1. Clone the repo `git clone 'https://github.com/juliansparks/CEN-4010'`
2. Change to the repo's directory `cd CEN-4010`
3. Check out the branch `git checkout flask_app`
4. Create a virtual environment `python3.6 -m venv venv`
5. Activate the virtual environment `source venv/bin/activate`
6. Upgrade pip `pip install --upgrade pip`
7. Install dependencies `pip install -r requirements.txt`
8. Set enviroment variables `export FLASK_APP=fapi.py`
9. Run the development server `flask run --host='0.0.0.0'`

## Generating the documnetation

1. Clone the repo `git clone 'https://github.com/juliansparks/CEN-4010'`
2. Change directory to the repo `cd CEN-4010`
3. Check out the branch `git checkout flask_app`
4. Change directory to the docs directory `cd docs/`
5. Make HTML documentation `make html`

The resulting HTML will be in `docs/build/html`. You can use python’s `http.server` to host this directory locally by typing the following.
```
cd docs/build/html
python -m http.server 5000
```
