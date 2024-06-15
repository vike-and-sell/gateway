FROM python:3.12-slim

WORKDIR /app

COPY flask/requirements.txt ./
RUN python3 -m venv env
ENV PATH=/app/env/bin:$PATH

ENV DATA_URL=test
ENV DATA_API_KEY=testapikey
ENV JWT_SECRET_KEY=testjwtsecret

RUN pip install -r requirements.txt
RUN pip install mockito pytest

COPY ./tests ./
COPY gateway.py ./

CMD ["python3", "-u", "-m", "pytest"]