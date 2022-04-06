# flask-json-vue
flask json api and vue

## Setup

### Clone repo
```shell script
git clone https://github.com/raphiniert/flask-json-vue.git
cd flask-json-vue
```

### Setup virtual environment and install dependencies

```shell script
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Create flask config

Add the instance/config.py including relevant settings such as:
```python
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'db connection string'  # e. g. postgresql://user:@localhost/statistics or "sqlite:///flask-json-vue.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'change your super secret key'  # seriously, change it!
TIMEZONE = "Europe/Vienna"
```

### Enable pre-commit

```shell script
pre-commit run --all-files
```

## Run

Simply type ```flask run``` on your command line and you are good to go.
```shell script
flask run
 * Serving Flask app 'flaskjsonvue' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 985-756-099
```

### Commands

#### Initialize database

Drops all tables and recreates them.

```shell script
flask init-db [--auto-import]
```

## Test

```shell script
coverage run -m pytest
```
