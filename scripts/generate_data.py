import pandas as pd
import random
import os

# Списки для генерации разнообразных не спам-отзывов
adjectives = ["отличный", "прекрасный", "неплохой", "хороший", "замечательный", "превосходный", "выдающийся", "потрясающий"]
nouns = ["товар", "продукт", "покупка", "заказ"]
adverbs = ["быстрая доставка", "высокое качество", "удобный сервис", "низкая цена", "отличная упаковка", "вежливый продавец", "точные сроки"]
recommendations = ["рекомендую", "очень доволен", "советую друзьям", "обязательно вернусь ещё раз", "не пожалел о покупке"]

not_spam_templates = [
    "Очень {adj} {noun}, {adv}!",
    "{adv_cap}, {recommend}.",
    "Покупаю {noun} не в первый раз — {recommend}.",
    "{adj_cap} {noun}, цена соответствует качеству.",
    "Доставили вовремя, {adv}, {recommend}."
]

# Списки для генерации разнообразных спам-отзывов
spam_actions = ["Купить", "Заказать", "Получить", "Покупай", "Зарабатывай", "Нажми", "Выиграй", "Скачай"]
spam_offers = ["здесь: example.com", "по ссылке: spam-site.ru", "в нашем приложении", "сейчас и бесплатно", "уже сегодня", "прямо сейчас"]
spam_promos = ["Бесплатные промокоды", "Скидка 90%", "Уникальная акция", "Горячее предложение", "Выиграй приз"]

spam_templates = [
    "{action} {offer}",
    "{promo} только сегодня!",
    "{action}, чтобы {promo_lower}.",
    "{promo} на сайте, {offer}.",
    "{promo} — {action} прямо сейчас!"
]

data = []
num_samples = 1000

for _ in range(num_samples):
    if random.random() > 0.3:
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        adv = random.choice(adverbs)
        recommend = random.choice(recommendations)
        template = random.choice(not_spam_templates)
        text = template.format(
            adj=adj,
            adj_cap=adj.capitalize(),
            noun=noun,
            adv=adv,
            adv_cap=adv.capitalize(),
            recommend=recommend
        )
        label = 0
    else:
        action = random.choice(spam_actions)
        offer = random.choice(spam_offers)
        promo = random.choice(spam_promos)
        template = random.choice(spam_templates)
        text = template.format(
            action=action,
            offer=offer,
            promo=promo,
            promo_lower=promo.lower()
        )
        label = 1
    data.append({"text": text, "label": label})

df = pd.DataFrame(data)

# Путь к целевой директории data, расположенной на уровень выше
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs(output_dir, exist_ok=True)  # Создаёт папку, если её нет

# Путь к файлу
output_path = os.path.join(output_dir, 'reviews.csv')

# Сохраняем CSV
df.to_csv(output_path, index=False)
print(f"Сгенерировано {num_samples} отзывов и сохранено в {output_path}")
