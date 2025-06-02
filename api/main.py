from fastapi import FastAPI
import pandas as pd
import pickle
import os
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging

# Настройка логирования
logging.basicConfig(
    filename='/app/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Импорт функций предобработки из preprocessing.py
from preprocessing import preprocess

app = FastAPI()

# Путь к модели и данным
model_path = "spam_model.pkl"
train_data_path = "processed_lead_data.csv"

# Загрузка модели
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    logging.error(f"Failed to load model: {str(e)}")
    raise Exception(f"Failed to load model: {str(e)}")

# Загрузка обучающего набора для получения ожидаемых столбцов
try:
    train_df = pd.read_csv(train_data_path)
    expected_columns = train_df.drop(columns=["is_spam"]).columns.tolist()
except Exception as e:
    logging.error(f"Failed to load training data: {str(e)}")
    raise Exception(f"Failed to load training data: {str(e)}")

# Модель для валидации входных данных
class LeadRequest(BaseModel):
    request_id: int
    name: str
    phone: str
    email: str
    comment: str
    landing_page: str
    time_on_page: float
    actions: float
    browser: str
    device: str
    timezone: str
    region: str
    domain: str

@app.post("/predict")
async def predict(request: LeadRequest):
    try:
        # Преобразование входных данных в словарь
        data = request.dict()
        logging.info(f"Received request: {data['request_id']}, comment: {data['comment']}")

        # Преобработка данных
        df = preprocess(data)

        # Выравнивание столбцов с обучающим набором
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_columns]

        # Предсказание
        score = model.predict(df).data[0, 0]
        spam_flag = 1 if score > 0.5 else 0
        logging.info(f"Prediction for request {data['request_id']}: score={score}, spam_flag={spam_flag}")

        return {"score": float(score), "spam_flag": spam_flag}
    except Exception as e:
        logging.error(f"Error processing request {data.get('request_id', 'unknown')}: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})