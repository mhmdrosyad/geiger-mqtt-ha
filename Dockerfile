FROM python:3.9-slim
RUN pip install --no-cache-dir pyserial paho-mqtt pygmc
WORKDIR /app
COPY ./app /app
CMD ["sh", "-c", "python discovery.py && python main.py"]