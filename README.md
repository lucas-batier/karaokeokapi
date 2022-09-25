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

## Features

### Proposal

When a user submit a proposal, the youtube video is analysed and Genius lyrics are fetched if it is possible. Then, a 
mail is sent to all the user who have the permission 'can_receive_proposal'.

### Feedback

Feedback is only available on beta versions.

When a feedback is submitted, a mail is sent to all the user who have the permission 'can_receive_feedback'.
