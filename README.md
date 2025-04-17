# Автотесты для API Метрополитен

Набор автотестов для проверки API Музея Метрополитен (https://metmuseum.github.io).
Использованы Python, Pytest, Pydantic.

## Установка
1. Клонируйте репозиторий.
2. Создайте виртуальное окружение: `python -m venv venv`.
3. Активируйте: `.\venv\Scripts\activate` (Windows).
4. Установите зависимости: `pip install -r requirements.txt`.
5. Запустите тесты: `pytest test_api.py -v`.

## Файлы
- `models.py`: Pydantic-модели для валидации данных.
- `test_api.py`: Тесты для API.
- `requirements.txt`: Зависимости.