@echo off
chcp 65001 >nul
title SimpleAnalysis - Запуск

echo [INFO] Создание виртуального окружения...
python -m venv venv || goto error

echo [INFO] Активация окружения...
call venv\Scripts\activate.bat || goto error

echo [INFO] Установка зависимостей (может занять немного времени)...
pip install -r requirements.txt >nul 2>&1

echo [INFO] Запуск Python-скрипта...
python simple_analysis.py || goto error

echo [INFO] Деактивация окружения...
call venv\Scripts\deactivate.bat

goto end

:error
echo [ERROR] Произошла ошибка при выполнении скрипта.

:end
echo.
echo [SUCCESS] Нажмите любую клавишу для выхода...
pause >nul
