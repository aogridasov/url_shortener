# URL-shortener

### Temporarily deployed project here, just in case: http://154.194.53.244:8000/sh/api/shortened_urls/

## Setting up
**Pyton 3.11 is required**

All dependencies can be found in **requirements.txt** and can be installed with Pip.

### Setup .env file in root repository (optional).
Example:
```
HOST=127.0.0.1:8000
LOGS_ROOT='logs'
```
HOST is used to form short URLS. If it is not set, it will be extracted from request headers. If not present it would be equal to 'localhost'.

If LOGS_ROOT is not set, log files will be created in projects root folder. 

*All commands are executed from project's root folder*
### Create and populate DB with django command:
```
python src/manage.py migrate
``` 

### If you want to use django admin panel, create superuser
```
python src/manage.py createsuperuser
```
### Run development server
```
python src/manage.py runserver
```

## How to use
### API
Project contains simple API to work with URLs.
CRUD operations with shortened URLs are performed at:
```
http://127.0.0.1:8000/sh/api/shortened_urls
```
To use shortened url for redirection use:
```
http://127.0.0.1:8000/sh/{SHORT URL CODE}
```

## Proper documentation of API endpoints can be found here:
```
Server must be running to access!
http://127.0.0.1:8000/sh/api/schema/swagger-ui/
```

### Admin page
If you created superuser (mentioned above) you can enter the django admin page.
You can see the contents of DB there and interact with the instances of URLs (creation is not implemented).
```
http://127.0.0.1:8000/admin/
```
### Tests
Tests can be ran with:
```
python src/manage.py test src
```
### Logs
All user's HTTP requests and other usefull info are logged in url_shortner.log
