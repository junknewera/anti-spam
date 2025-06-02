import requests

# Тестовые заявки
test_leads = [
    {
        "request_id": 1,
        "name": "Ivan Ivanov",
        "phone": "+71234567890",
        "email": "ivan@mail.ru",
        "comment": "Хочу купить автомобиль",
        "landing_page": "Акция BMW",
        "time_on_page": 120.0,
        "actions": 5.0,
        "browser": "Chrome",
        "device": "mobile",
        "timezone": "Europe/Moscow",
        "region": "Москва",
        "domain": "rolf-cars.ru"
    },
    {
        "request_id": 2,
        "name": "Test User",
        "phone": "abc123",
        "email": "нет данных",
        "comment": "тест спам",
        "landing_page": "Скидки на Audi",
        "time_on_page": 10.0,
        "actions": 1.0,
        "browser": "Firefox",
        "device": "desktop",
        "timezone": "Asia/Yekaterinburg",
        "region": "Екатеринбург",
        "domain": "rolf-sale.ru"
    }
]

# Тестирование API
for data in test_leads:
    response = requests.post("http://91.219.189.125:8000/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    try:
        result = response.json()
        print(f"Request ID: {data['request_id']}, Text: {data['comment']}, Score: {result['score']:.4f}, Spam Flag: {result['spam_flag']}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")