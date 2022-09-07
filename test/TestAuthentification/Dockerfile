FROM python:3.10.4-slim

RUN pip3 install requests

ADD AuthenTest.py /home/tester/AuthenTest.py

WORKDIR /home/tester/

CMD [ "python", "AuthenTest.py" ]