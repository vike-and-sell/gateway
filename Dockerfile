FROM python:3.12-slim

WORKDIR /app

COPY flask/requirements.txt ./
RUN python3 -m venv env
ENV PATH=/app/env/bin:$PATH

RUN pip install -r requirements.txt

COPY ./flask ./
COPY gateway.py ./

CMD ["python3", "wsgi.py"]