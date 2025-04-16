FROM python:3.12.2


RUN apt-get update
RUN apt-get install unzip python3 pip -y
RUN pip install boto3
RUN python3 -m pip install playwright 
RUN python3 -m playwright install 
RUN playwright install-deps 



WORKDIR /app

COPY london.py .

CMD ["python3", "london.py"]