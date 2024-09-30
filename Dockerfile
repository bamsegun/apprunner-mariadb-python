FROM python:3.11
WORKDIR /app
RUN apt update -y && apt upgrade -y
RUN apt install gcc -y
RUN apt install python3-dev -y
RUN apt install openssl -y
RUN pip install --upgrade pip --no-cache-dir
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app
EXPOSE 8000
CMD ["gunicorn" "--bind=0.0.0.0:8000" "--workers=1" "--threads=2" "--log-level=debug" "application:app"]

