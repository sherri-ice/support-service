# InnowiseTask
## About
REST API for ticket-support application with DRF. 


## Used tools
Testing with django rest test framework. Async tasks uses Celery + Redis. Deploying to docker with docker-compose.

# Run the app

Application is deployed to docker, `Dockerfile` for the DRF app and `docker-compose.yaml` files are configured using PostgreSQL database to run the app using docker
    
#### Run docker containers
###### Build all the containers and run them the containers in background
    docker-compose up --build -d
###### Make migrations for the database
    docker-compose exec web python manage.py migrate
###### Create superuser for the app
    docker-compose exec web python manage.py createsuperuser

# Api Overview

## Users

User response structure: 
```
{
    "id": 1,
    "username": "test",
    "email": "test@test.com",
    "password": "pbkdf2_sha256$320000$bseVfzJXUntdbI6z1pdM6w$Yayz+JgnlvfhqcchB6uL5hdZsc8BMfpcBXxCsVBr7xI="
}
```

| Api method          | Description             | Requires                        | Response |
| -----------         | -----------             | -----------                     | ----------- |
| POST /api/register       | Registers new user       | `username`, `email`, `password` | Information about registered user
| POST /api/login          | Login point              | `username`, `password`          | Access and refresh tokens
| GET /api/users/         | Admin only. List of all users            |           | List of all users
| GET /api/users/me/         | Returns user who made request           |           | User information

## Tickets

Ticket response structure: 
```
{
    "id": 1,
    "title": "Test!",
    "body_text": "test",
    "owner": 1,
    "status": "CL",
    "messages": [
        {
            "id": 1,
            "text": "test"
        }
    ]
 }
```

Message response structure:
```
{
  'id': 1,
  'text': "test"
}
```
Ticket has field `status` which may be only one of this: `AC` (active), `FR` (frozen), `CL` (closed).

| Api method          | Description             | Requires                        | Response |
| -----------         | -----------             | -----------                     | ----------- |
| GET /api/tickets/       | For admin: returns all tickets. For user: return list of his tickets.       |  | List of tickets.
| GET /api/tickets/<pk:id>/         | Get ticket by id              |           | Instance of Ticket
| PUT(PATCH) /api/tickets/<pk:id>/        | Admin only. Edit ticket. Actually, can change only status field.           |  `status`        | Patched instanse of Ticket
| POST /api/tickets/add/        | Create new ticket. Status is set to active.       |     `title`, `body_text`     | Instance of ticket
| POST /api/tickets/<pk:id>/new_message/        | Add new message to selected ticket.       |     `text`, `body_text`     | Instance of Message

## Celery + Redis and Emails

When user crreates new ticket, notification email is sent. User is automaticly subscribed to his tickets' updates. Emails are sent when ticket status is changed by support user or support user left a new message for the ticket.
