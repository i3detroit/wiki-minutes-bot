FROM python:3
WORKDIR /wmb
COPY . .
RUN pip install -r requirements.txt
