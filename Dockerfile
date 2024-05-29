FROM python:3.10-alpine
LABEL authors="zwickvitaly"

ENV PYTHONUNBUFFERED=1

WORKDIR /bot
RUN touch ${API_NAME}.session
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY bot/ .

ENTRYPOINT python3 main.py