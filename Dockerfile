FROM python:3.8-slim-buster
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg && apt-get install -y --no-install-recommends git

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python3", "app.py"]