FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY ../scripts/preprocessing.py ../scripts/
COPY ../data/model.pkl ../data/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]