# KaraokeOK API

## Setup instructions

To launch the api:

1. Install Docker desktop
2. Launch Docker desktop
3. Launch the stack (from the root repository: karaokeokapi)
```shell
docker-compose up -d
```
4. Launch the Postgres database migrations (from the root repository: karaokeokapi)
```shell
docker-compose exec api python manage.py migrate
```
5. Create the superuser (from the root repository: karaokeokapi)
```shell
docker-compose exec api python manage.py createsuperuser
```
