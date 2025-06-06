[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/HannaAA17/flask_celery_template)

## Run the app
* `$ redis-server`
* `$ python -m celery -A app worker --loglevel=info`

## Zip the last files committed
* `$ zip modified-files.zip $(git diff --name-only HEAD^)`

## Kill the redis server
* `$ lsof -i:8080`
* `$ kill pid`
