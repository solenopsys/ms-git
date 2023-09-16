FROM python:3.7.1-slim

RUN apt-get update && \
  apt-get install -y git --no-install-recommends \
  gcc
RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
COPY git_api.py .

RUN pip install -r requirements.txt

CMD ["python", "git_api.py"]