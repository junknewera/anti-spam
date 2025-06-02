import pandas as pd
import re
import os

# Функции предобработки из preprocessing.py
SPAM_WORDS = ['тест', 'asdf', 'бесплатно', 'идиот', 'не звоните', 'проверка']

def contains_spam_words(text):
    text = str(text).lower()
    return int(any(word in text for word in SPAM_WORDS))

def is_valid_email(email):
    email = str(email)
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def is_valid_phone(phone):
    phone = str(phone)
    return len(phone) == 11 and phone.isdigit()

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Базовая очистка
    df["name"] = df["name"].fillna("")
    df["phone"] = df["phone"].fillna("")
    df["email"] = df["email"].fillna("")
    df["comment"] = df["comment"].fillna("")
    df["time_on_page"] = df["time_on_page"].fillna(df["time_on_page"].median())  # Заполняем медианой
    df["actions"] = df["actions"].fillna(0)

    # Признаки
    df["name_length"] = df["name"].apply(lambda x: len(str(x)))
    df["name_has_test"] = df["name"].apply(lambda x: int("тест" in str(x).lower() or "test" in str(x).lower()))

    df["phone_length"] = df["phone"].apply(lambda x: len(str(x)))
    df["phone_has_letters"] = df["phone"].apply(lambda x: int(any(c.isalpha() for c in str(x))))
    df["is_valid_phone"] = df["phone"].apply(is_valid_phone)

    df["is_valid_email"] = df["email"].apply(is_valid_email)
    df["email_domain"] = df["email"].apply(lambda x: x.split("@")[-1] if "@" in x else "unknown")

    df["comment_length"] = df["comment"].apply(lambda x: len(str(x)))
    df["comment_has_spam_words"] = df["comment"].apply(contains_spam_words)

    # Признак: "вовлечённость"
    df["engagement"] = df["time_on_page"] / (df["actions"] + 1)

    # One-hot-кодирование
    categorical_cols = ["landing_page", "browser", "email_domain"]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Удаляем оригинальные поля
    df.drop(columns=["name", "phone", "email", "comment"], inplace=True)

    return df

# Путь к данным
data_dir = "../data"
input_path = os.path.join(data_dir, "synthetic_lead_data.csv")
output_path = os.path.join(data_dir, "processed_lead_data.csv")

# Загрузка данных
df = pd.read_csv(input_path)

# Предобработка
processed_df = preprocess(df)

# Переименование spam_flag в is_spam для совместимости с последующим кодом
processed_df = processed_df.rename(columns={"spam_flag": "is_spam"})

# Сохранение обработанных данных
processed_df.to_csv(output_path, index=False)
print(f"Обработанные данные сохранены в {output_path}")