#!/bin/bash

echo "[INFO] Создание виртуального окружения..."
python3 -m venv venv || { echo "[ERROR] Не удалось создать виртуальное окружение."; exit 1; }

echo "[INFO] Активация виртуального окружения..."
source venv/bin/activate || { echo "[ERROR] Не удалось активировать окружение."; exit 1; }

echo "[INFO] Установка зависимостей (скрытый режим)..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Ошибка при установке зависимостей."
    deactivate
    exit 1
fi

echo "[INFO] Запуск программы..."
python simple_analysis.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Программа завершилась с ошибкой."
fi

echo "[INFO] Деактивация виртуального окружения..."
deactivate


read -n1 -r -p "[SUCCESS] Нажмите любую клавишу для выхода..."
echo
