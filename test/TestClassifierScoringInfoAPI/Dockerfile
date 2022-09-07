FROM python:3.10.4-slim

RUN pip3 install requests

ADD ScoringTest.py /home/tester/ScoringTest.py

WORKDIR /home/tester/

CMD [ "python", "ScoringTest.py" ]