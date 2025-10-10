#!/bin/bash

echo "🔄 Зупиняю старий бот..."
# Kill all running bot processes
pkill -f "python.*main.py" 2>/dev/null || true
sleep 1

echo "🧹 Очищую кеш..."
# Clean all cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Кеш очищено!"
echo ""
echo "🚀 Запускаю бота..."

# Start bot using venv
./venv/bin/python3 main.py > bot.log 2>&1 &
BOT_PID=$!

sleep 2

# Check if bot started successfully
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Бот успішно запущений! PID: $BOT_PID"
    echo ""
    echo "📋 Для перегляду логів:"
    echo "   tail -f bot.log"
    echo ""
    echo "🛑 Для зупинки бота:"
    echo "   kill $BOT_PID"
else
    echo "❌ Помилка запуску бота! Дивіться логи:"
    cat bot.log
fi
