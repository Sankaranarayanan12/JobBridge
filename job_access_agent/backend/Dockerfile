FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONUNBUFFERED=1
ENV GOOGLE_API_KEY=""
ENV ADZUNA_APP_ID=""
ENV ADZUNA_API_KEY=""


EXPOSE 8080

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080"]