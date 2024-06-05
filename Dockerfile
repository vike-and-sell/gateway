FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m venv env
ENV PATH=/app/env/bin:$PATH

RUN pip install -r requirements.txt

COPY . ./

CMD ["python3", "wsgi.py"]