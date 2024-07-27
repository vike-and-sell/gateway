[![AWS CDK deploy](https://github.com/vike-and-sell/gateway/actions/workflows/cdk-deploy.yml/badge.svg)](https://github.com/vike-and-sell/gateway/actions/workflows/cdk-deploy.yml)

# gateway

Owned by the backend team, this repo holds the code, infra, and deployment for the main backend gateway layer

# structure

This application has 3 main directories and a single file for all business logic
## gateway.py
This file contains all business logic and its functions are called by the lambda functions or the flask API
## lambda
This directory contains all the logic to interace with AWS' Lambda serverless API. The endpoints in the lambda directory will call their respective business logic funtions in gateway.py
## flask
This directory contains a Flask API that allows the api to be run locally. This application mimics the behaviour of the lambda endpoints and calls the business logic in gateway.py. This Flask app also allows the business logic to be tested and calls the business logic in the unit tests.
## tests
This directory contains unit tests for the business logic of the application. Mockito is used to mock data layer queries and test for specific inputs and responses. At least one happy and one unhappy test was implemented for each enpoint. 

# Running Application
## Create env file
create a `.env` file in the root directory that follows the same structure as `.env.dist`. Here is the expected structure:
```
DATA_URL: use dl_flask_api:4000 if running with local data layer.
DATA_API_KEY: create any key here. This key is used to authenticate to the data layer and the same key will have to be placed in the data layer.
JWT_SECRET_KEY: create any key here. This key is used to encode and decode the jwt, and should always be kept secret.
MAPS_API_KEY= create an azure maps key by following these instructions: https://learn.microsoft.com/en-us/azure/azure-maps/how-to-manage-account-keys.
```
## Running unit tests

```
docker compose -f docker-compose-test.yml up --build
```

## Running locally

To run locally:

```
docker network create vikeandsell # you only need to do this once per device
docker compose up --build
```
## Output
To test the functionality of the application, query localhost:8080/<endpoint>. This will query the flask app, and trigger the business logic. Please note that many users and listings endpoints will not work without a valid azure maps key.
