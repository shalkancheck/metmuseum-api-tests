import logging
import requests
from pydantic import ValidationError
from models import ArtObject, SearchResults

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"


def test_get_object_by_id():
    """Тест получения объекта по ID."""
    object_id = 436121
    logger.info(f"Запрос объекта с ID: {object_id}")
    response = requests.get(f"{BASE_URL}/objects/{object_id}")

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )
    logger.info(f"Статус ответа: {response.status_code}")

    try:
        data = response.json()
        art_object = ArtObject(**data)
        logger.info(f"Получен объект: {art_object.title}")
        assert art_object.objectID == object_id
        assert art_object.title is not None
    except ValidationError as e:
        logger.error(f"Ошибка валидации: {e}")
        raise


def test_get_nonexistent_object():
    """Тест обработки несуществующего ID."""
    object_id = 999999999
    logger.info(f"Запрос несуществующего объекта с ID: {object_id}")
    response = requests.get(f"{BASE_URL}/objects/{object_id}")

    assert response.status_code == 404, (
        f"Ожидался статус 404, получен {response.status_code}"
    )
    logger.info(f"Статус ответа: {response.status_code}")


def test_search_objects():
    """Тест поиска по ключевому слову."""
    query = "Monet"
    logger.info(f"Поиск по запросу: {query}")
    response = requests.get(f"{BASE_URL}/search?q={query}")

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )
    logger.info(f"Статус ответа: {response.status_code}")

    try:
        data = response.json()
        search_results = SearchResults(**data)
        logger.info(f"Найдено объектов: {search_results.total}")
        assert search_results.total > 0
        assert len(search_results.objectIDs) > 0
    except ValidationError as e:
        logger.error(f"Ошибка валидации: {e}")
        raise


def test_search_empty_query():
    """Тест поиска с пустым запросом."""
    query = ""
    logger.info("Поиск с пустым запросом")
    response = requests.get(f"{BASE_URL}/search?q={query}")

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )
    logger.info(f"Статус ответа: {response.status_code}")

    try:
        data = response.json()
        search_results = SearchResults(**data)
        logger.info(f"Найдено объектов: {search_results.total}")
        assert search_results.total == 0
        assert search_results.objectIDs == [], "Ожидался пустой список"
    except ValidationError as e:
        logger.error(f"Ошибка валидации: {e}")
        raise


def test_search_with_department_filter():
    """Тест поиска с фильтром по департаменту."""
    query = "Monet"
    department_id = 11
    logger.info(f"Поиск по запросу '{query}' с departmentId={department_id}")
    url = f"{BASE_URL}/search?q={query}&departmentId={department_id}"
    response = requests.get(url)

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )
    logger.info(f"Статус ответа: {response.status_code}")

    try:
        data = response.json()
        search_results = SearchResults(**data)
        logger.info(f"Найдено объектов: {search_results.total}")
        assert search_results.total >= 0
        if search_results.total > 0:
            assert len(search_results.objectIDs) > 0
    except ValidationError as e:
        logger.error(f"Ошибка валидации: {e}")
        raise
