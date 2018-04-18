# Launching flask\_angular\_scaffold projects

## About
This is our base scaffold for applications. It's Flask with AngularJS and Bootstrap. On the Flask side we use our custom api\_base.py in order to handle most CRUD/HTTP action processing. 
NOTE: These instructions are meant for Dev Services Sandbox setups. If you are setting it up on another server, then it may be different.

## Need to keep in mind
This is meant to be an example to build off of. As you build the overall app, one of the things you will probably realize is that you will need to update and add more models. Unfortunately, if you
run
```
python database.py
```
It won't update the actual database. One way to update the mysql database is to actually run sql commands in the database. Such as adding table, or adding/changing columns.
Another option is to update your models.py, delete your all your tables in the mysql database, then run `python database.py` to create the tables. However, this approach will delete all the data in
there. Probably best practices would be to have as much of your models thought out ahead as possible, written into `models.py`, normalized, and then run `python database.py`. With any luck you
you won't have to keep delete database tables, creating them again, then adding new test data.


## Setting Up Virtual Env
```
cd ~
virtualenv --system-site-packages <app_virtual_env>
```
NOTE: Make sure you use --system-site-packages when installing the virtualenv


## Cloning Project
```
cd ~/source/
git clone <git_repo>
cd <your_app_name>
mv flask_angular_scaffold <your_app_name>
```


## Remove .egg-info
if `flask_angular_scaffold.egg-info` is present:
```
rm -rf flask_angular_scaffold.egg-info/
```


## Changing app name
NOTE: This won't change all instances of 'flask\_angular\_scaffold' in the code. You will have to verify
```
find -name "*.py" | xargs perl -pi -e 's/flask_angular_scaffold/<your_app_name>/g'
```


## Setting up git
```
rm -rf .git
git init
```


## Prepping public\_html Files:

NOTE: Files that need to be prepped are now inside: `~/source/<your_app_name>/*`

### public\_html\_files/htaccess:
Depending on your project you might have to:
-uncomment some of the lines about Shib access
-uncomment the rewrite rules if you plan on having the admin side available.

### public\_html\_files/bootstrap.cgi, public\_html\_files/bootstrap.fcgi:
Line 3, change the virtualenv to the one you created for this project.

### public\_html\_files/bootstrap.py:
Verify the following changes have been made:
Changed app name on line 25 `from flask_angular_scaffold.app` to `<your_app_name>.app`
Changed app name on line 27: `...(CleanScriptName(app,'<your_app_name>'))...`


## Moving public\_html files
```
mkdir ~/public_html/<your_app_name>
cp ~/source/<your_app_name>/public_html_files/* ~/public_html/<your_app_name>
mv ~/public_html/<your_app_name>/htaccess ~/public_html/<your_app_name>/.htaccess
```


## Updating public\_html file permissions
```
chmod 755 ~/public_html/<your_app_name>
chmod 755 ~/public_html/<your_app_name>/*
chmod 644 ~/public_html/<your_app_name>/.htaccess
```

## Changing App Files

NOTE: These files are inside `~/source/<your_app_name>/<your_app_name>/`
NOTE: It's at your discretion about commiting from here on out.

### api\_base.py
Verify lines 9,10 have been changed from `flask_angular_scaffold` to `<your_app_name>`

NOTE:
Need to uncomment:
```
if not self._check_access...
```
in various methods if checking access is required.


### api\_views.py
Verify lines 9,10 have been changed from `flask_angular_scaffold` to `<your_app_name>`
Lines 12-14 should be:
```
12 app = Flask(__name__)
13 <your_app_blueprint> = Blueprint('<your_app_name>',name)
14 api = Api(<your_app_blueprint>)
```


### app.py
Lines 11-14 should be:
```
from <your_app_name>.api_views import <your_app_blueprint>
app.register_blueprint(<your_app_blueprint>,'api/')

from <your_app_name>.views import main
```


### database.py
Verify Line 28:
```
from <your_app_name>.models import Base
```


### models.py
Verify line 17:
```
from <your_app_name>.database import Base
```
Look over Project and Contact. Contact doesn't have any routes, but it's there if you wanted to.


### /static/js/\* (all files in static/js/ and subdirectories):

Change the name of the .module on line 5 from 'fas' to the name of your angular app.
```
.module('<yourAngularAppName>')
```
NOTE: For Angular App Names, the convention is camelCase. Snake Case will break the app
NOTE: The controllers are pretty closely mapped to their http action and the filename. However, an example of the 'delete' function is in the details controller.


### /templates/index.html
Update Line 2
```
<html class="no-js" lang="en" ng-app="<yourAngularAppName>"
```


### /templates/menu.html
Update lines 15,16
```
<li><a href='/<your_app_name>/'>Home</a></li>
<li><a href='/<your_app_name>/add_project'>Add Project</a></li>

```


## Setting Up Database/Sqlalchemy
### Mysql
Log in to mysql. In sandbox this is typically done with typing:
```
mysql
```
in the command line. Then create your database inside mysql
```
create database <your_app_database_name>;
```
then log out of mysql.


### example\_flask\_angular\_scaffold.ini:
Update the sqlalchemy\_database\_uri to use your database string
```
sqlalchemy_database_uri = mysql://<username>:<password>@localhost:<port>/<your_app_database_name>?charset=utf8
```
then move it to your root directory
```
mv example_flask_angular_scaffold.ini ~/<your_app_name>.ini
```


### ~/source/\<your\_app\_name\>/\<your\_app\_name\>/config.py
In line 4, update the location of the .ini file to where you placed your app's one
This might already have been changed if you named the .ini file the same as your app name. But just verify.


## Lauch Virtual Environment
```
source <your_virtual_env>/bin/activate
which python
```
verify it's the one from `<your_virtual_env>` should read something like
```
~/<your_virtual_env>/bin/python
```


## Set Up App
```
cd ~/source/<your_app_name>/
python setup.py develop
cd ~/source/<your_app_name>/<your_app_name>
python database.py
```


## Verify App Runs
```
cd ~public_html/<your_app_name>/
run python bootstrap.py
```
You should see something that ends in the error
```
KeyError: 'SERVER_NAME'
```
then you can try in your browser to see if it will launch.
URL will be something like:
```
http://<Server_IP_Address>/<your_app_name>/
```
The url is going to your `~/public_html/<your_app_name>/bootstrap.cgi (or fcgi)`
so if you named the directory inside the public html differently then `<your_app_name>` then you will use that.


## Clean Up
You should be able to now remove the following:
```
rm -rf ~/source/<your_app_name>/public_html_files
```


## Common Errors


### Flup and/or Flask Missing
Some common errors include either flask or flup missing. In which case:
```
cd ~/source/<your_app_name>/
which python
```
Verify virtual environment is active and then install flup and/or flask
```
pip install flup
pip install flask
```

Repeat:
```
cd ~public_html/<your_app_name>/
run python bootstrap.py
```


### Angular App Not Starting
If you open the brower to your URL and all you see is a blue background. Open the console and if you see:
```
Uncaught Error: [$injector:modulerr]` Failed to instantiate module fas due to:
...
```
Somewhere in the `static/js/` there is a file that fas was not changed over.
The best way to check is to run the following inside `static/js`
```
ack "fas"
```
If still nothing, make sure you updated `templates/index.html`


If there are still errors then that will have to be addressed on individual basis


## Need to do
- Add Delete cycle
- Models explanation
- Update to python3 and using pipenv
- Add Unit Tests

