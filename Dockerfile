FROM python:3.9.18-alpine3.18

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements_mqtt.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
