# Car wash APIs

## Steps to develop APIs
1. Define APIs functionality of a car wash appointment.
    - Reserve
    - Get detail
    - Cancel
2. Design Data model and create ER diagram.
3. Implementing APIs with Django.
4. Testing APIs (Unit test, Postman).
5. Dockerize Django app with Dockerfile and docker-compose.yaml.
6. Create CI/CD pipeline to build, test and deploy Django code.

---

## Set up and Run project locally, Choose 1 method.

### 1. Python
- 1.1 Create virtual environment. \
`python -m venv env` \
`source env/bin/activate`

- 1.2 Install dependencies. \
`pip install -r requirements.txt`

- 1.3 Migrate Database. \
`python manage.py migrate`

- 1.4 Start django server. \
`python manage.py runserver`

- 1.5 Go to [http://localhost:8000/swagger](http://localhost:8000/swagger) to start using APIs.

### 2. Docker 
- 2.1 Use below command then wait until container db and api_app are running. \
`docker compose up -d`

- 2.2 Go to [http://localhost:8000/swagger](http://localhost:8000/swagger) to start using APIs.