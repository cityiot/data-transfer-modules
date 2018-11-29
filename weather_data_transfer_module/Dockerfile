FROM python:2.7

WORKDIR /usr/local/bin

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]