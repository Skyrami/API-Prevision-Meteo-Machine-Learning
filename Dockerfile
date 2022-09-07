FROM python:3.10.4-slim

COPY ./api /home/rainproject/api
COPY ./datascience /home/rainproject/datascience
COPY main.py  /home/rainproject/
COPY README.md /home/rainproject/
COPY requirements.txt /home/rainproject/

RUN apt update && apt install curl -y
RUN pip install -r /home/rainproject/requirements.txt

WORKDIR /home/rainproject/

EXPOSE 8000

CMD uvicorn main:api --host 0.0.0.0
