#dockerfile for backend

FROM python:3.11-slim

WORKDIR /api


COPY requirements.txt .
RUN pip install --upgrade pip setuptools


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "backend_app.py"]

