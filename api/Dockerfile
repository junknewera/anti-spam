FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY ./preprocessing.py ./scripts
COPY ./model.pkl ./data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]