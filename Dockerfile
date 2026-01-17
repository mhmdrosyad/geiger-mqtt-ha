FROM python:3.9-slim
RUN pip install --no-cache-dir pyserial paho-mqtt pygmc
WORKDIR /app
COPY ./app /app
# L'opzione -u forza Python a scrivere i log immediatamente
CMD ["python", "-u", "main.py"]