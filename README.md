# Web App & REST API

## Running for development

1. Clone the repo `git clone 'https://github.com/juliansparks/CEN-4010'`
2. Change to the repo's directory `cd CEN-4010`
3. Check out the branch `git checkout flask_app`
4. Create a virtual environment `python3.6 -m venv venv`
5. Activate the virtual environment `source venv/bin/activate`
   * There is a `.env` file if you are using `autoenv` that will
     activate the virtual environment for you
6. Upgrade pip `pip install --upgrade pip`
7. Install dependencies 
   * `pip install -r requirements/production.txt`
   * `pip install -r requirements/testing.txt`
8. Set enviroment variables `export FLASK_APP=fapi.py`
9. Run the development server `flask run --host='0.0.0.0'`

## Running tests
* All test can be run with `flask test`
* To autoformat and lint run `flask test lint`

## Generating the documnetation

Once you've follwed the install instructions, you can generate the documentation using:
* `flask docs build` to build the documentation
* `flask docs serve` to serve the documentation

