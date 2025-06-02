from fastapi import FastAPI
import pandas as pd
import pickle
import os
from pydantic import BaseModel
from fastapi.responses import JSONResponse

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
    raise Exception(f"Failed to load model: {str(e)}")

# Загрузка обучающего набора для получения ожидаемых столбцов
try:
    train_df = pd.read_csv(train_data_path)
    expected_columns = train_df.drop(columns=["is_spam"]).columns.tolist()
except Exception as e:
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

        # Преобработка данных
        df = preprocess(data)

        # Выравнивание столбцов с обучающим набором
        # Добавляем отсутствующие столбцы с нулями
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0

        # Удаляем лишние столбцы, которых нет в обучающем наборе
        df = df[expected_columns]

        # Предсказание
        score = model.predict(df).data[0, 0]  # Вероятность спама
        spam_flag = 1 if score > 0.5 else 0  # Порог 0.5

        return {"score": float(score), "spam_flag": spam_flag}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})