# ATTENTION 
# CHANGE CREDS BEFORE DEPLOY

**Install postgres, python3, virtualenv**
**Create and start venv**
```
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
sudo pip3 install virtualenv

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

**Setup postgres database**
```
sudo -i -u postgres psql

CREATE USER boardadmin WITH PASSWORD 'password';
ALTER ROLE boardadmin SET client_encoding TO 'utf8';
ALTER ROLE boardadmin SET default_transaction_isolation TO 'read committed';
CREATE DATABASE boardproject;
GRANT ALL PRIVILEGES ON DATABASE boardproject to boardadmin;
```

**To start server**
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

python3 manage.py runserver 127.0.0.1:8000
```