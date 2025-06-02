FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn pandas requests lightautoml
RUN pip install --no-cache-dir torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

COPY main.py .
COPY preprocessing.py .
COPY spam_model.pkl .
COPY processed_lead_data.csv .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]