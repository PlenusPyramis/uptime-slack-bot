FROM python:3.7-slim
RUN adduser app --gecos GECOS --shell /bin/bash --disabled-password --home /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY main.py /app
USER app
ENTRYPOINT ["/app/main.py"]
