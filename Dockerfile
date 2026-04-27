FROM python:3.11-slim

LABEL maintainer="Thomas Osorio"
LABEL description="E-commerce de zapatos con Chat IA - Universidad EAFIT"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data

EXPOSE 8000

CMD ["uvicorn", "src.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
