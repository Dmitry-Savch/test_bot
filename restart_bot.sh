#!/bin/bash

# Parse command line arguments
TEST_MODE_ARG=""
if [[ "$1" == "--test" ]] || [[ "$1" == "-t" ]]; then
    TEST_MODE_ARG="TEST_MODE=true"
    echo "🧪 TEST MODE АКТИВОВАНО"
    echo ""
fi

echo "🔄 Зупиняю старий бот..."
# Kill all running bot processes
pkill -f "python.*main.py" 2>/dev/null || true
sleep 1

echo "🧹 Очищую кеш..."
# Clean all Python cache files
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

echo "✅ Кеш очищено!"
echo ""
echo "🚀 Запускаю бота..."

# Start bot using venv with optional TEST_MODE
if [[ -n "$TEST_MODE_ARG" ]]; then
    env $TEST_MODE_ARG ./venv/bin/python3 main.py > bot.log 2>&1 &
else
    ./venv/bin/python3 main.py > bot.log 2>&1 &
fi
BOT_PID=$!

sleep 2

# Check if bot started successfully
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Бот успішно запущений! PID: $BOT_PID"
    if [[ -n "$TEST_MODE_ARG" ]]; then
        echo "🧪 TEST MODE: Дані автоматично заповнюються тестовими значеннями"
    fi
    echo ""
    echo "📋 Для перегляду логів:"
    echo "   tail -f bot.log"
    echo ""
    echo "🛑 Для зупинки бота:"
    echo "   kill $BOT_PID"
    echo ""
    echo "💡 Використання:"
    echo "   ./restart_bot.sh        - Звичайний режим"
    echo "   ./restart_bot.sh --test - Тестовий режим з автозаповненням"
else
    echo "❌ Помилка запуску бота! Дивіться логи:"
    cat bot.log
fi
