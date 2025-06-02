FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY preprocessing.py .
COPY spam_model.pkl .
COPY processed_lead_data.csv .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]