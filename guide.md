# Installation

Install the environment:

REQUIREMENTS:

- Python3
- Pref. Linux (Virtual, WSL, ...)
- Download the .env file of Google Drive and put it in root folder (where this file is)


```sh
#In project root dir use
source ./scripts/setup.sh
```

After that, you need to activate the environment:
```sh
source ./.env/bin/activate
```
<br>
And then migrate the db and run for first time the server:

```sh
#To migrate the db:
python manage.py migrate

#To run the server:
python manage.py runserver
```


If all work correctly just go to:

http://127.0.0.1:800

# Use

You need to activate the environment and then run the server:

```sh
source ./.env/bin/activate

#after that you will see something like:
(.env) bagansio@Bagansio: 

----

python manage.py runserver

#If you want to deactivate the environment, just use:
deactivate
```



