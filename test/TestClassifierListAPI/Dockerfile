FROM python:3.10.4-slim

RUN pip3 install requests

ADD test.py /home/tester/test.py

WORKDIR /home/tester/

CMD [ "python", "test.py" ]