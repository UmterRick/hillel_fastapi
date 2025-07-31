from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from databases.sqlalchemy import engine  # імпортуй звідти, де у тебе створений engine

# Ініціалізація інспектора
inspector = inspect(engine)

# Отримати список усіх таблиць
all_tables = inspector.get_table_names()

# Список таблиць, які шукаємо
target_tables = ['baskets', 'basket_lines', 'orders', 'order_lines']

# Перевірка
for table in target_tables:
    if table in all_tables:
        print(f"✅ Таблиця {table} існує.")
    else:
        print(f"❌ Таблиця {table} НЕ знайдена.")