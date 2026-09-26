FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /service
COPY requirements.backend.txt ./
RUN pip install --no-cache-dir -r requirements.backend.txt
COPY app/ ./app/
ENV PORT=8080
CMD ["sh", "-c", "exec uvicorn app.api:app --host 0.0.0.0 --port ${PORT:-8080}"]
