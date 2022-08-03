# URL SHORTENER REST API 
* This is a simple  REST API created with Python==3.6.x, Django Rest Framework, PostgreSQL(Or you can use sqlite3 for local)

## Getting Ready

Create a virtual environment in order to keep the repo dependencies separated from your local machine
and activate it 

```
virtualenv venv
venv\Scripts\activate
```

Make sure to install the dependencies of the project through the requirements.txt file.

```
pip install -r requirements.txt
```

Once you have installed necessary packages, go to the cloned repo directory update your settings.py file for postgresql database or run below command to use sqlite3 db

```
export DJANGO_SETTINGS_MODULE=config.settings_local
```

After deciding database run below commands 

```
python manage.py makemigrations
```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command

```
python manage.py migrate
```

 We just need to start the server now and then we can start using our simple todo App. Start the server by following command

```
python manage.py runserver
```

* NOTE

Default runserver command will run the app in 8000 port. If you want to change port you also need to change
```
API_URL
```
variable to match ports

## Schema

* UrlShortener
  * original_url
  * shortened_url
  * counter
  * created_at
  * updated_at

## API


**/create-url/**

* post

**/list-all-urls/**

* get

**/{shortened_url}/**

* get

**Example payload and response**

Payload:
```json
{
    "original_url":"https://www.yemeksepeti.com/"
}
```

response:
```json
{
    "result":"localhost:8000/jhLxdEsQ49"
}
```
