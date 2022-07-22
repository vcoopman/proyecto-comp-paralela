FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000 
CMD [ "gunicorn", "app:app", "-b 0.0.0.0:5000", "--workers", "9", "--access-logfile", "/dev/stdout" ]
