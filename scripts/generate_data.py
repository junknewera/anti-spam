import pandas as pd
import numpy as np
import random
import string
import os

# 1. Настройки
np.random.seed(42)
random.seed(42)
n_samples = 100000

# 2. request_id
request_ids = np.arange(1, n_samples + 1)

# 3. Синтетические имена
def random_name():
    first_names = ["Ivan", "Anna", "Dmitry", "Elena", "Sergey", "Olga", "Mikhail", "Marina", "Alexey", "Natalia"]
    last_names = ["Ivanov", "Petrova", "Sidorov", "Smirnova", "Kuznetsov", "Popova", "Lebedev", "Sokolova", "Kovalev", "Novikova"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

names = [random_name() for _ in range(n_samples)]

# 4. Телефоны
def random_phone(valid=True):
    if valid:
        return "+7" + "".join(random.choices(string.digits, k=10))
    else:
        length = random.choice([5, 8, 12])
        pool = string.ascii_letters + string.digits
        return "".join(random.choices(pool, k=length))

valid_flags = np.random.choice([True, False], size=n_samples, p=[0.7, 0.3])
phones = [random_phone(valid=v) for v in valid_flags]

# 5. Email
def random_email(valid=True):
    domains = ["mail.ru", "yandex.ru", "gmail.com", "inbox.ru"]
    if valid:
        user = "".join(random.choices(string.ascii_lowercase, k=7))
        return f"{user}@{random.choice(domains)}"
    else:
        return "нет данных"

email_flags = np.random.choice([True, False], size=n_samples, p=[0.8, 0.2])
emails = [random_email(valid=e) for e in email_flags]

# 6. Комментарии
def random_comment(spam=False):
    spam_keywords = ["тест", "спам", "buy now", "click", "offer"]
    if spam:
        return " ".join(random.choices(spam_keywords, k=random.randint(1, 3)))
    else:
        words = ["Хочу", "купить", "автомобиль", "информацию", "цена", "доставка", "звоните"]
        return " ".join(random.choices(words, k=random.randint(3, 7)))

# 7. Остальные признаки
landing_pages = ["Акция BMW", "Рассрочка KIA", "Скидки на Audi", "Новый Volvo", "Сервис ROLF"]
lp_choices = np.random.choice(landing_pages, size=n_samples)

time_on_page = np.random.exponential(scale=100, size=n_samples)
missing_indices_time = np.random.choice(n_samples, size=int(0.05 * n_samples), replace=False)
time_on_page[missing_indices_time] = np.nan

actions = np.random.poisson(lam=5, size=n_samples).astype(float)
missing_indices_actions = np.random.choice(n_samples, size=int(0.05 * n_samples), replace=False)
actions[missing_indices_actions] = np.nan

browsers = ["Chrome", "Firefox", "Safari", "Edge", "Opera", "Internet Explorer"]
devices = ["mobile", "desktop"]
browser_choices = np.random.choice(browsers, size=n_samples, p=[0.6, 0.1, 0.1, 0.1, 0.05, 0.05])
device_choices = np.random.choice(devices, size=n_samples, p=[0.5, 0.5])

timezones = ["Europe/Moscow", "Europe/Helsinki", "Asia/Yekaterinburg", "Asia/Krasnoyarsk"]
regions = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
timezone_choices = np.random.choice(timezones, size=n_samples)
region_choices = np.random.choice(regions, size=n_samples)

domains = ["rolf-cars.ru", "rolf-service.ru", "rolf-sale.ru"]
domain_choices = np.random.choice(domains, size=n_samples)

spam_flags = np.random.choice([1, 0], size=n_samples, p=[0.3, 0.7])
comments = [random_comment(spam=bool(sf)) for sf in spam_flags]

# 8. Сборка датафрейма
data = pd.DataFrame({
    "request_id": request_ids,
    "name": names,
    "phone": phones,
    "email": emails,
    "comment": comments,
    "landing_page": lp_choices,
    "time_on_page": time_on_page,
    "actions": actions,
    "browser": browser_choices,
    "device": device_choices,
    "timezone": timezone_choices,
    "region": region_choices,
    "domain": domain_choices,
    "spam_flag": spam_flags
})

# 9. Сохранение
output_dir = "/home/junknewera/workspace/machine-learning/projects/digital-economics-league/anti-spam/data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "synthetic_lead_data.csv")
data.to_csv(output_path, index=False, encoding="utf-8")

print(f"Данные успешно сохранены в {output_path}")
