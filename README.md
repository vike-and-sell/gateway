# gateway

Owned by the backend team, this repo holds the code, infra, and deployment for the main backend gateway layer

# Running unit tests

```
docker compose -f docker-compose-test.yml up --build
```

# Running locally

To run locally:

```
docker network create vikeandsell # you only need to do this once per device
docker compose up --build
```

TODO: add envars for data layer url and JWT secret key
