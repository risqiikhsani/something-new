FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN cat requirements.txt | xargs -n 1 pip install
COPY . /app