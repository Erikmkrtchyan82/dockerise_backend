FROM python:3.9-alpine

WORKDIR /app
RUN pip3 install flask psycopg2-binary redis

COPY . .

VOLUME [ "/app/data" ]

EXPOSE 5000

CMD [ "python3", "app.py" ]
