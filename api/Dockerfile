FROM python:3.9-slim

WORKDIR /app

# Копируем файлы (если они есть)
COPY requirements.txt .
COPY main.py .
COPY preprocessing.py .
COPY spam_model.pkl .
COPY processed_lead_data.csv .

# Установка зависимостей
RUN pip install --no-cache-dir fastapi uvicorn pandas requests lightautoml
RUN pip install --no-cache-dir torch==2.3.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]