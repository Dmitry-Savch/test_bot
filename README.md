# SAT Form Telegram Bot

Telegram бот для нанесення тексту на скріншот SAT (податкова Сальвадору).

## Структура проєкту

```
project/
├── utils/                    # Утиліти для роботи з зображеннями
│   ├── text_draw.py
│   ├── text_draw_centered.py
│   ├── text_image_horizontal.py
│   └── image_overlay.py
├── modifiers/               # Модифікатори
│   └── sat_form_modifier.py
├── bot/                     # Рівень бота
│   ├── keyboards.py
│   ├── states.py
│   └── handlers.py
├── templates/              # Шаблони
│   └── sat_form.png        # Базовий скріншот форми
├── output/                 # Папка для результатів
├── main.py                 # Точка входу
├── config.py              # Конфігурація
└── requirements.txt
```

## Встановлення

1. Встановіть залежності:
```bash
pip install -r requirements.txt
```

2. Створіть файл `.env` і додайте токен бота:
```
BOT_TOKEN=your_telegram_bot_token_here
```

3. Додайте шаблон форми SAT у папку `templates/sat_form.png`

## Запуск

```bash
python main.py
```

## Використання

1. Надішліть `/start` боту
2. Оберіть режим введення:
   - **Одним повідомленням**: всі дані в одному рядку через `|`
   - **По черзі**: бот буде питати кожен параметр окремо

3. Натисніть "Створити скріншот"
4. Введіть дані:
   - NOMBRE DEL BENEFICIARIO
   - NUMERO DE CUENTA
   - IMPORTE DEL IMPUESTO
   - VALOR ENVIADO

### Формат вводу одним повідомленням:
```
Beneficiario | NumCuenta | Importe | Valor
```

Приклад:
```
Juan Perez | 1234567890 | 150.50 | 150.50
```

## Налаштування координат

Координати для нанесення тексту знаходяться у файлі `modifiers/sat_form_modifier.py`.
Поточні координати є приблизними і можуть потребувати уточнення.
