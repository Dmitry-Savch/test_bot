#!/bin/bash

# Перехід до директорії проекту
cd /Users/dmitrosavcuk/Desktop/test_bot

# Зупинка старого процесу бота
echo "Зупиняю бота..."
ps aux | grep "python.*main.py" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null

# Пауза перед запуском
sleep 1

# Запуск бота
echo "Запускаю бота..."
venv/bin/python main.py &

echo "Бот перезапущено! PID: $!"
