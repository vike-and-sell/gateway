FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m venv env
ENV PATH=/app/env/bin:$PATH

ENV DATA_URL=test
ENV DATA_API_KEY=testapikey
ENV JWT_SECRET_KEY=testjwtsecret
ENV SEARCH_REC_URL=${SEARCH_REC_URL}

RUN pip install -r requirements.txt

COPY ./tests/*.py ./
COPY gateway.py ./

CMD ["python3", "-u", "-m", "pytest"]