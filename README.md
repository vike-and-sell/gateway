# gateway

Owned by the backend team, this repo holds the code, infra, and deployment for the main backend gateway layer

# Running locally

To run locally:

```
cd gateway
docker build --tag "tag-name" -f flask/Dockerfile .
docker run --detach -p 8080:8080 tag-name
```

TODO: add envars for data layer url and JWT secret key
