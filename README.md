# SMILE SALES order microservice

The SMILE SALES Order Microservice is a critical component of the SMILE SALES e-commerce, which is dedicated to handling order and payment processes. It provides robust functionalities for managing orders from creation to completion, including payment processing, order tracking, and returns.

# Key Features

## Order Management:

- Checkout: Facilitates the creation of new orders.
- Cancellation: Allows users to cancel orders before shipment.
- Returns: Enables customers to initiate returns for purchased items.
- Tracking: Provides real-time order tracking information.
- Archiving/Unarchiving: Enables the management of order history.
- Filtering: Offers advanced filtering options based on dates and order status.
## Payment Processing:
- PayPal Integration: Supports secure payments via PayPal.
- Refund Management: Handles and processes refund requests according to approval status.


# Techology Stack
### Programming Languages
[![python](https://img.shields.io/badge/Python-3.11.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
### Frameworks
![Static Badge](https://img.shields.io/badge/Django-5.0.2-white?logo=django&labelColor=%23092E20)
![Static Badge](https://img.shields.io/badge/Django_Rest_Framework-3.14.0-black?labelColor=%23C20000)
### Testing Framework
![Static Badge](https://img.shields.io/badge/Unittest-(Python_3.11.9)-blue)
### Databases
![Static Badge](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql&logoColor=white&labelColor=black)
![Static Badge](https://img.shields.io/badge/Redis-8.0-%23FF4438?logo=redis&labelColor=black)
### Email notifications
![Static Badge](https://img.shields.io/badge/Gmail-%23FFFFFF?logo=gmail)
### Other libraries
![Static Badge](https://img.shields.io/badge/Dramatiq-1.16.0-black)
![Static Badge](https://img.shields.io/badge/Django_Rest_Framework_Simple_JWT-5.2.2-blue?labelColor=white)
![Static Badge](https://img.shields.io/badge/factory--boy-3.3.0-white?labelColor=black)
![Static Badge](https://img.shields.io/badge/Faker-25.1.0-black?labelColor=blue)
![Static Badge](https://img.shields.io/badge/Gunicorn-23.0.0-white?labelColor=%23328B32)
![Static Badge](https://img.shields.io/badge/AMPQ-5.1.1-white?labelColor=orange)


# Setup
### 1. Clone repository with:
```bash
git clone https://github.com/GhostMEn20034/SMILE_SALES_ORDER_MICROSERVICE.git
```
### 2. Go to directory with project
### 3. Create .env file:
on Windows (PowerShell), run:
```powershell
New-Item -Path ".env" -ItemType "File"
```
on Unix or MacOS, run:
```bash
touch .env
```
### 4. Open any editor and paste your env variables:
```sh
SUPER_USER_PWD=some_pwd # Password of the Postgres user
SECRET_KEY=124555asdadas # Django's secret key
JWT_SIGNING_KEY=some_key # Signing key for JWT Tokens (Use the same value as in User microservice)
DEBUG=0_or_1 # Determines whether the debug mode turned on (1 - on, 0 - off)
ALLOWED_HOSTS=localhost,127.0.0.1,[::1] # Your allowed hosts
FRONTEND_BASE_URL=http://localhost:3000 # Base URL of the main frontend webserver
SQL_ENGINE=django.db.backends.postgresql # DB Engine
SQL_DATABASE=smile_sales_orders # Database Name
SQL_USER=smile_sales_orders_usr # Database Owner
SQL_PASSWORD=xxxx4444 # DB user's password
SQL_HOST=db # Database host
SQL_PORT=5432 # Database Port
SQL_CONN_MAX_AGE=60 # Maximum Connection's age
AMPQ_CONNECTION_URL=url_rabbit_mq # Message broker URL
PRODUCT_CRUD_EXCHANGE_TOPIC_NAME=product_replication # Just copy that
USERS_DATA_CRUD_EXCHANGE_TOPIC_NAME=users_data_replication # Just copy that
ORDER_PROCESSING_EXCHANGE_TOPIC_NAME=order_processing_replication # Just copy that
PAYPAL_API_BASE_URL=https://api-m.sandbox.paypal.com # BASE URL of the PayPal API
PAYPAL_CLIENT_ID=afdfd2324323 # Client ID of PayPal account
PAYPAL_SECRET=aasfdsf53123123121 # Secret key for PayPal API
DRAMATIQ_BROKER_URL=# Redis url for dramatiq broker
CHECK_ABANDONED_ORDERS_EVERY_MINUTES=5 # How often to check for abandoned orders and delete them (In minutes)
EMAIL_HOST=some.smtp.com # SMTP Host for sending email
EMAIL_PORT=your_port
EMAIL_HOST_USER=some_usr@gmail.com # the email from which you want to send emails
EMAIL_HOST_PASSWORD=some_pwd # The password of the Gmail (Or other provider) app
```


# Running The app
If you want to run this app you have two options:
 - Run it using `docker-compose`
 - Run it using `k8s`

### 1. Running using `docker-compose`
#### 1.1 Add permission to execute the `init-database.sh` file inside the docker-compose's Postgres service:
```bash
chmod +x init-database.sh
```
#### 1.2 Enter the command below to run the app with `docker-compose`:
```bash
docker compose up -d --build
```
#### 1.3 Go to localhost:8003 or 127.0.0.1:8003 and use the API.

#### Running `docker-compose` in production
If you want to do that, you need to use the file `docker-compose-prod.yml` and the of the file with env variables should be `.env.prod`.<br>
This option assumes that you have already run db in AWS or any other providers.<br>
Also you need to use different command to run the app:
```bash
docker compose -f docker-compose-prod.yml --env-file=.env.prod up -d
```
Now, you can go to localhost or 127.0.0.1 and use the API.

### 2. Running using Kubernetes resources
**Note: If you want to run this API using Kubernetes, you need to start and expose Postgres and Redis servers manually**
#### 2.1 Create a kubernetes namespace:
```bash
kubectl create namespace smile-sales-users
```
#### 2.2 Create an object with type secret from `.env` file:
```bash
kubectl create secret generic web-secrets --from-env-file=.env
```
#### 2.3 Go to the directory with k8s resources:
```bash
cd k8s
```
#### 2.4 Apply config maps:
```bash
kubectl apply -f config-maps/
```
#### 2.5 Apply persistent volumes:
```bash
kubectl apply -f persistent-volumes/
```
#### 2.6 Apply persistent volume claims:
```bash
kubectl apply -f persistent-volume-claims/
```
#### 2.7 Run jobs to complete migrations and collect static files:
```bash
kubectl apply -f jobs/
```
#### 2.8 Wait until jobs are completed, you can check whether they are completed with the command:
```bash
kubectl get jobs
```
#### 2.9 Apply services:
```bash
kubectl apply -f services/
```
#### 2.10 Apply deployments:
```bash
kubectl apply -f deployments/
```

# Run Tests
**Caution: make sure you're in the default directory**<br><br>
To run tests you need to complete 3 steps:
1. Run the test app with another `docker-compose` file:
```bash
docker compose -f docker-compose-test-env.yaml up -d
```
2. Run the command below:
```bash
docker compose exec web python manage.py test -v 2
```
3. Shutdown `docker-compose` services:
```bash
docker compose -f docker-compose-test-env.yaml down
```