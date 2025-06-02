from fastapi import FastAPI
import pandas as pd
import pickle
import os
from pydantic import BaseModel

# Импорт функций предобработки из preprocessing.py
from preprocessing import preprocess

app = FastAPI()

# Путь к модели
model_path = "spam_model.pkl"

# Загрузка модели
with open(model_path, "rb") as f:
    model = pickle.load(f)

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
    # Преобразование входных данных в словарь
    data = request.dict()

    # Преобработка данных
    df = preprocess(data)

    # Предсказание
    score = model.predict(df).data[0, 0]  # Вероятность спама
    spam_flag = 1 if score > 0.5 else 0  # Порог 0.5

    return {"score": float(score), "spam_flag": spam_flag}