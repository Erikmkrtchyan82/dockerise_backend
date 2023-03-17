FROM python:3.9

WORKDIR /app
RUN pip3 install flask

COPY . .

EXPOSE 5000

CMD [ "python3", "app.py" ]
