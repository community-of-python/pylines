# Tests Guide

Источник: community-of-python/pylines/tests.md

## 1. AAA паттерн

Arrange → Act → Assert:

```python
def test_should_create_user_successfully() -> None:
    # Arrange
    client: typing.Final = TestClient(app=create_application())
    user_payload: typing.Final = {"email": fake.email(), "password": "securepass123"}

    # Act
    response: typing.Final = client.post("/api/users", json=user_payload)

    # Assert
    assert response.status_code == 201
```

## 2. Интеграционные > юнит тесты

Юнит тесты требуют колоссальной поддержки. Тестируй через сервис в сборе или через ручку:

```python
# ❌ Юнит тест отдельного метода
def test_should_validate_email_format() -> None:
    validator: typing.Final = EmailValidator()
    assert validator.is_valid_email("test@example.com")

# ✅ Интеграционный тест через API
def test_should_reject_invalid_email_via_api() -> None:
    client: typing.Final = TestClient(app=create_application())
    response: typing.Final = client.post("/api/users", json={"email": "invalid-email", "password": "pass123"})
    assert response.status_code == 422
```

## 3. Генерация данных

Не пиши статические скаляры. Используй **faker** и **hypothesis**:

```python
fake: typing.Final = Faker()

# faker
def test_create_user() -> None:
    user_email: typing.Final = fake.email()
    user_age: typing.Final = fake.random_int(min=18, max=99)
    ...

# hypothesis (property-based testing)
@given(email=st.emails(), age=st.integers(min_value=18, max_value=99))
def test_accept_valid_data(email: str, age: int) -> None:
    ...
```

## 4. Параметризация

```python
@pytest.mark.parametrize(
    ("password", "expected_status"),
    [
        ("123", 422),
        ("validpass123", 201),
        ("a" * 1000, 422),
        ("", 422),
    ],
)
def test_validate_password(password: str, expected_status: int) -> None:
    ...
```

## 5. Параллельный запуск

Всегда: `pytest-xdist -n auto`. С самого начала проекта.

## Стек тестирования

pytest, pytest-xdist, hypothesis, schemathesis, polyfactory, faker
