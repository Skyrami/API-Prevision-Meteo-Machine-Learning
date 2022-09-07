FROM python:3.10.4-slim

RUN pip3 install requests

ADD FullTest.py /home/tester/FullTest.py

WORKDIR /home/tester/

CMD [ "python", "FullTest.py" ]

