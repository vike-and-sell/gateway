FROM python:3.12-slim

WORKDIR /app

COPY flask/requirements.txt ./
RUN python3 -m venv env
ENV PATH=/app/env/bin:$PATH

# ENV DATA_URL="seng499-datalayer-playground-datalayer-1V:8089"
# ENV DATA_API_KEY="apikey123"
# ENV JWT_SECRET_KEY="secret123"

RUN pip install -r requirements.txt

COPY ./flask ./
COPY gateway.py ./

CMD ["python3", "-u", "wsgi.py"]