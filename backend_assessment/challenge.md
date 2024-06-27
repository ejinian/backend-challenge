# Tasks and Labels
## Made with Django REST Framework

## How to run:
1. Install python3 and pip3
2. Install Django: `pip3 install Django==3.1.4`, `pip3 install djangorestframework==3.15.2`, `djangorestframework-simplejwt==5.3.1`
3. Clone repo and `cd` into `backend_assessment`
4. Run migrations: `python3 manage.py migrate`
5. Create test admin user: `python3 manage.py createsuperuser`
6. Run server: `python3 manage.py runserver`
7. (Optional) Run tests: `python3 manage.py test tests.test_models` and `python3 manage.py test tests.test_endpoints`

## Manual Testing
Open an API testing platform (e.g. Postman) and configure the following routes:

### Authentication POST (required for each route)
1. `localhost:8000/api/auth/token/` Body: `{ "username": <your_superuser_username>, "password": <your_superuser_password> }`\
Copy the response body's `access` value. This will expire after 1000 minutes (time can be changed in `settings.py`).
Ensure that your authorization headers include "Authorization" for the key and the JWT token for the value.
2. (Bonus) `localhost:8000/api/auth/token/refresh/` Body: `{ "username": <your_superuser_username>, "password": <your_superuser_password>, "refresh": <your_refresh_token> }`

### GET Requests
1. `localhost:8000/api/labels/`
2. `localhost:8000/api/tasks/`

### POST Requests
1. `localhost:8000/api/labels/` Body: `{ "name": "My Label", "owner": <your_user_id> }`
2. `localhost:8000/api/tasks/` Body: `{ "title": "My Task", "description": "Test", "is_completed": false, "owner": <your_user_id>, "labels": [<label_id>, ...] }`

### PUT Requests
1. `localhost:8000/api/labels/<label_id>/` Body: `{ "name": "My Edited Label", "owner": <your_user_id> }`
2. `localhost:8000/api/tasks/<task_id>/` Body: `{ "title": "My Edited Task", "description": "New", "is_completed": true, "owner": <your_user_id>, "labels": [<label_id>, ...] }`

### DELETE Requests
1. `localhost:8000/api/labels/<label_id>/`
2. `localhost:8000/api/tasks/<task_id>/`

*Already existing superadmin credentials:*
- Username: `ernest`
- Password: `Testing321`

Alternatively, you can navigate to `localhost:8000/admin` and log in using your superuser credentials. Navigate to the left and create `Label`, `Task`, or `User` objects for testing.
Every instance of `Label` will be shown with its name and every instance of `Task` with be shown with its title. There should already be multiple test objects, but you can delete the `db.sqlite3` file and run `python3 manage.py migrate` to recreate it.

## Design

### Database Schema
*Label Model*
- `name: char`
- `owner: fk` (one-to-many)

*Task Model*
- `title: char`
- `description: text`
- `is_completed: bool`
- `owner: fk` (one-to-many)
- `labels: fk` (many-to-many)

*Django's User Model relevant fields*
- `username: char`
- `email: char`
- `is_superuser: bool`

### Authentication/Authorization
Django's REST framework offers a library called `rest_framework_simplejwt` allowing for secure transfer of information between client/server.
Because of the database schema, an object can only be created through a user. Thus, all routes are protected/personalized and can only be accessed by the creator.
In this project, I used Django's User model from `auth` which comes with pre-built basic user attributes. Users cannot create duplicate labels.
