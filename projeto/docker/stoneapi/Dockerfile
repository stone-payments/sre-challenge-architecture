FROM python:3
WORKDIR /opt/stoneapi

COPY ./api /opt/stoneapi

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./stone.py" ]
