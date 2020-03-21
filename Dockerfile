FROM python:3-alpine
WORKDIR /dtc
RUN apk add gcc libc-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install uwsgi
COPY . .
RUN chmod +x ./starttpw.sh
CMD ./starttpw.sh