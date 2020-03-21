FROM python:3-alpine
WORKDIR /dtc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD flask run -h 0.0.0.0