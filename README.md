# subscription-management-system

please rename the .env-example file to .env
this file has been included for convinience.

# With Docker

## Build and start containers

docker-compose up --build

## Run database migrations

docker-compose exec web python manage.py migrate

## Create superuser

docker-compose exec web python manage.py createsuperuser

## Stopping everything

docker-compose down

# API Endpoints

| Method | URL                   | Description                                  |
| ------ | --------------------- | -------------------------------------------- |
| POST   | `/api/subscribe/`     | Create a new subscription                    |
| GET    | `/api/subscribtions/` | List all subscriptions (note: spelling typo) |
| POST   | `/api/cancel/`        | Cancel a subscription                        |
| GET    | `/api/exchange-rate/` | Get latest exchange rate                     |
| POST   | `/api/token/`         | Obtain JWT access and refresh tokens         |
| POST   | `/api/token/refresh/` | Refresh JWT access token                     |
| GET    | `/subscriptions/`     | subscription list show in template           |

# API Payloads with response Demo

1.  /api/token/
    payload:
    {
    "username": "hassan",
    "password": "j8019705\*e"
    }
    response:
    {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1Njk5MDg1NywiaWF0IjoxNzU0Mzk4ODU3LCJqdGkiOiI1NDk4MWZkOTM2ZDE0YTAzYWRkMmIxNWU3OWY0YzYxZSIsInVzZXJfaWQiOiIyIn0.KBEEGXil-CXyUA4njHuOWVsc5kXNEoV9NMDegia8iIU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1MDAzNjU3LCJpYXQiOjE3NTQzOTg4NTcsImp0aSI6ImUyZDZjMDQwNjJjYzQyNjRhMjQxMjE0MTE3ZDM5MzhmIiwidXNlcl9pZCI6IjIifQ.1705tYOWiNkbFMplWaGg3dfbKHlnsILR5QAUCAeta7Y"
    }
2.  /api/subscribtions/
    response:
    {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
    {
    "id": 1,
    "plan": {
    "id": 1,
    "name": "Basic",
    "price": "10.00",
    "duration_days": 20
    },
    "start_date": "2025-08-05T13:02:54.080902Z",
    "end_date": "2025-08-25T13:02:54.079880Z",
    "status": "active",
    "user": 2
    },
    {
    "id": 2,
    "plan": {
    "id": 2,
    "name": "Premium",
    "price": "50.00",
    "duration_days": 60
    },
    "start_date": "2025-08-05T13:03:24.662963Z",
    "end_date": "2025-10-04T13:03:24.661081Z",
    "status": "active",
    "user": 2
    }
    ]
    }

3.  /api/subscribe/
    payload:
    {
    "plan_id": 2
    }
    response:
    {
    "id": 2,
    "plan": {
    "id": 2,
    "name": "Premium",
    "price": "50.00",
    "duration_days": 60
    },
    "start_date": "2025-08-05T13:03:24.662963Z",
    "end_date": "2025-10-04T13:03:24.661081Z",
    "status": "active",
    "user": 2
    }
4.  /api/cancel/
    payload:
    {
    "subscription_id": 1
    }
    response:
    {
    "message": "Subscription cancelled successfully.",
    "subscription_id": 1
    }
5.  /api/exchange-rate/
    response:
    {
    "base_currency": "USD",
    "target_currency": "BDT",
    "rate": "121.7312",
    "fetched_at": "2025-08-05T13:32:00.467004Z"
    }
    \*\* All The APIs are protected by JWT token

6.  For all subsequent API requests, include the access token in the HTTP header
    Authorization: Bearer <access_token>

# Without Docker

## Create virtual environment

python -m venv venv
source venv/bin/activate

## Install dependencies

pip install -r requirements.txt

## Run migrations

python manage.py migrate

## Create admin user

python manage.py createsuperuser

## Run Redis (separate terminal)

redis-server

## Run development server

python manage.py runserver

## Celery

celery -A sms worker --loglevel=info
celery -A sms beat --loglevel=info
