# Как писать тесты

1. Паттерн большинства тестов, обычно, это AAA: arrange (подготовили), act (что-то поделали), assert (проверили)

   ```python
   import typing

   import pytest
   from litestar.testing import TestClient

   from myapp import create_application
   from myapp.services import UserService


   def test_should_create_user_successfully() -> None:
       # Arrange (подготовка)
       client: typing.Final = TestClient(app=create_application())
       user_email: typing.Final = "test@example.com"
       user_payload: typing.Final = {"email": user_email, "password": "securepass123"}

       # Act (действие)
       response: typing.Final = client.post("/api/users", json=user_payload)

       # Assert (проверка)
       assert response.status_code == 201
       assert response.json()["email"] == user_email
   ```

2. Стоит меньше писать юнит тестов и больше «интеграционных» (некоторые их называют sociable). Т.е. если можно потестировать ваш код через сервис в сборе или через ручку, лучше тестировать через них, чем тестировать отдельный метод или функцию. Мотивация здесь простая: юнит тесты требуют колоссальный объем поддержки. Как только вы меняете часть вашего кода, приходится переписывать большие пачки юнит тестов. В случае с интеграционными тестами это работает не так. Иногда даже не требуется ничего переписывать

   ```python
   import typing

   from litestar.testing import TestClient

   from myapp import create_application


   # ❌ Плохо: юнит тест отдельного метода
   def test_should_validate_email_format() -> None:
       from myapp.validators import EmailValidator

       validator: typing.Final = EmailValidator()
       assert validator.is_valid_email("test@example.com")


   # ✅ Хорошо: интеграционный тест через API
   def test_should_reject_invalid_email_via_api() -> None:
       client: typing.Final = TestClient(app=create_application())
       invalid_payload: typing.Final = {"email": "invalid-email", "password": "pass123"}

       response: typing.Final = client.post("/api/users", json=invalid_payload)

       assert response.status_code == 422
       assert "email" in response.json()["detail"]
   ```

3. Стоит использовать генерацию данных, не писать статические скаляры (вроде строк или чисел). Используйте везде, где возможно, faker. Так же, если возможно, стоит применять на ключевые кейсы [hypothesis](https://github.com/HypothesisWorks/hypothesis). Он делает ваши тесты значительно более надежными

   ```python
   import typing

   import hypothesis.strategies as st
   from faker import Faker
   from hypothesis import given
   from litestar.testing import TestClient

   from myapp import create_application

   fake: typing.Final = Faker()


   # ❌ Плохо: статические данные
   def test_should_create_user_with_static_data() -> None:
       client: typing.Final = TestClient(app=create_application())
       response: typing.Final = client.post("/api/users", json={"email": "test@test.com", "age": 25})
       assert response.status_code == 201


   # ✅ Хорошо: использование faker
   def test_should_create_user_with_faker() -> None:
       client: typing.Final = TestClient(app=create_application())
       user_email: typing.Final = fake.email()
       user_age: typing.Final = fake.random_int(min=18, max=99)

       response: typing.Final = client.post("/api/users", json={"email": user_email, "age": user_age})

       assert response.status_code == 201


   # ✅ Отлично: использование hypothesis для property-based testing
   @given(email=st.emails(), age=st.integers(min_value=18, max_value=99))
   def test_should_accept_any_valid_user_data(email: str, age: int) -> None:
       client: typing.Final = TestClient(app=create_application())

       response: typing.Final = client.post("/api/users", json={"email": email, "age": age})

       assert response.status_code in {201, 409}  # Created или уже существует
   ```

4. Стоит использовать параметризацию. Лучшие тесты — те, которые проходят код по многу раз, поэтому старайтесь зайти в одни и те же места в несколько прогонов

   ```python
   import typing

   import pytest
   from litestar.testing import TestClient

   from myapp import create_application


   # ❌ Плохо: отдельный тест для каждого случая
   def test_should_reject_short_password() -> None:
       client: typing.Final = TestClient(app=create_application())
       response: typing.Final = client.post("/api/users", json={"email": "test@test.com", "password": "123"})
       assert response.status_code == 422


   def test_should_reject_long_password() -> None:
       client: typing.Final = TestClient(app=create_application())
       response: typing.Final = client.post("/api/users", json={"email": "test@test.com", "password": "a" * 1000})
       assert response.status_code == 422


   # ✅ Хорошо: параметризованный тест
   @pytest.mark.parametrize(
       ("password", "expected_status"),
       [
           ("123", 422),  # Слишком короткий
           ("validpass123", 201),  # Валидный
           ("a" * 1000, 422),  # Слишком длинный
           ("", 422),  # Пустой
           ("   ", 422),  # Пробелы
       ],
   )
   def test_should_validate_password_length(password: str, expected_status: int) -> None:
       client: typing.Final = TestClient(app=create_application())

       response: typing.Final = client.post("/api/users", json={"email": "test@example.com", "password": password})

       assert response.status_code == expected_status
   ```

5. По-умолчанию все тесты всегда должны запускаться параллельно, даже если их немного. Это позволяет всегда достигать параллелизируемости тестов с самого старта и защищаться от состояния когда ваши тесты могут работать только в один поток. Для этого используйте `pytest-xdist` с опцией `-n auto`

6. Для тестирования кода, который выполняет HTTP-запросы с помощью httpx, используйте [RESPX](https://lundberg.github.io/respx/). Это мощная библиотека для мокирования HTTPX запросов с гибкими паттернами запросов и побочными эффектами ответов.

```python
import httpx
import respx
import pytest
from unittest import mock


# ❌ Плохо: monkeypatching внутренней функции fetch_users
def test_with_monkeypatching(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "myservice.external.users_api.fetch_users", mock.AsyncMock(return_value=[{"id": 1, "name": "John"}])
    )

    do_something_that_uses_fetch_users()


# ✅ Хорошо: использование RESPX для тестирования настоящей интеграции
@respx.mock
def test_with_respx_integration():
    respx.get("https://api.example.com/users/").mock(return_value=httpx.Response(200, json=[{"id": 1, "name": "John"}]))

    do_something_that_uses_fetch_users()
```
