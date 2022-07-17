[tutorial](https://flask.palletsprojects.com/en/2.1.x/tutorial/layout/)

## installation
```sh
pip3 install virtualenv

# create virtual env
virtualenv env

# activate virtual env
source env/bin/activate

#init db
flask init-db

#install project
pip install -e .

#test converage
pip install pytest coverage
```

## Run
```sh
# before run
export FLASK_APP=flaskr
export FLASK_ENV=development

# run
flask run

#check port run at 5000 mac
lsof -P -i :5000
```
## class vs object
class is template for objects,
A class also describes object behavior. 
An object is a member or an "instance" of a class.

