import requests
import pandas as pd
import os

# Путь к данным
data_dir = "data"
input_path = os.path.join(data_dir, "synthetic_lead_data.csv")

# Загрузка тестовых данных
df = pd.read_csv(input_path).sample(5)  # Берём 5 случайных заявок

# Тестирование API
for _, row in df.iterrows():
    data = row.to_dict()
    response = requests.post("http://91.219.189.125:8000/predict", json=data)
    result = response.json()
    print(f"Request ID: {data['request_id']}, Text: {data['comment']}, Score: {result['score']:.4f}, Spam Flag: {result['spam_flag']}")