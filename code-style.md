Code style
---
Этот codestyle призван сделать следующее: облегчить жизнь за счет автоформатирования, быть простым, без каких-либо скрытых путей или инструментов. Это руководство по достижению хорошего качества кода, предназначенное для «ленивых» (в хорошем смысле) разработчиков, которые не хотят утруждать себя. Кстати: если в наших правилах чего-то нет, оно уже есть в ruff и нам нет нужды это писать.

Настройка
-----
1. `pip install ruff`
1. Добавьте кусок конфигурации в `pyproject.toml`:
    ```toml
    [tool.ruff]
    fix = true
    unsafe-fixes = true
    line-length = 120

    [tool.ruff.format]
    docstring-code-format = true

    [tool.ruff.lint]
    select = ["ALL"]
    ignore = ["EM", "FBT", "TRY003", "D1", "D203", "D213", "G004", "FA", "COM812", "ISC001"]

    [tool.ruff.lint.isort]
    no-lines-before = ["standard-library", "local-folder"]
    known-third-party = []
    known-local-folder = []
    lines-after-imports = 2

    [tool.ruff.lint.extend-per-file-ignores]
    "tests/*.py" = ["S101", "S311"]

    [tool.coverage.report]
    exclude_also = ["if typing.TYPE_CHECKING:"]
    ```

Правила
-----
1. Длина строки 120 символов
1. Правила импортов:
    1. Все встроенные библиотеки нужно импортировать целиком: `import os`, `import typing`
    1. Все модули в которых более 2 импортов нужно импортировать целиком: `from my_module import SomeModule, AnotherModule, HelloOne` ==> `import my_module`
1. Покрывайте 100% кода аннотациями типов: переменные, константы, атрибуты, аргументы, всё без исключений. Аннотации позволяют находить как банальные ошибки, так и вещи вроде нарушения принципа подстановки Барбары Лисков. Аннотации — это не «ну у нас же не джава», а наш друг и большое достижение python, они дают классный компромисс между статический и динамической типизацией, позволяя нам жить с плюсами динамической типизацией, получая часть плюсов статической.
    1. Подключайте mypy (пока всё ещё его)
    1. Не пишите скалярные типы, их выведет mypy сам. Т.е.:
        ```python
        some_var: str = 'something going on'
        another_var: int = 5
        ```
        Пишите (типы выведутся сами, да ещё и с более узким типом `typing.Literal`):
        ```python
        some_var = 'something going on'
        another_var = 5
        ```
1. Сужайте эксепшены
    1. Не пишите `except Exception`, пишите максимально конкретный класс ошибки, иначе это приведёт к проблемам. Используйте `except Exception` в исключительных случаях
    1. Сужайте эксепшены до 1 строчки. Когда не получается можно зацепить ещё несколько
1. Любые обращения по индексу (`item[0]`) или ключу (`item["something"]`) могут и будут «падать». Всегда обрабатывайте их через `try-except`. Помните иерархию и используйте разных случаях:
    ```
    LookupError
    ├── IndexError
    └── KeyError
    ```
    Так же при использовании словаря вы можете воспользоваться методом get — `item.get("something")`, он не падает, а возвращает `None`, в некоторых сценариях это может быть уместно.
1. Пишите самодокументируемый код:
    1. Имена всех переменных и функций должны иметь длину не менее 8 символов. Имена типа `a`, `b` запрещены
    1. Используйте осмысленные названия переменных, вкладывайте в их названия семантику (т.е. смысл). Переменная вроде `data` или `user`, например, смысла не несут, т.к. слишком общие. Используйте конкретику — `public_user`, например
    1. Все функции должны называться глаголами, т.к. функции что-то делают. Использование существительных запрещено, кроме использования с `@property`
    1. Не стоит писать комментарии никогда. Большинство комментариев — это самоочевидные и не полезные строки кода, которые осложняют поддержку кодовой базы. Пишите комментарий только тогда, когда вам есть что сказать (очень сложное неявное поведение, например), в остальных случаях не пишите и не испытывайте угрызений совести на этот счёт
    1. Не стоит использовать префикс get для имен функций. Get не несёт смысла, все операции в разработке это либо get, либо set. Так же его смысл прочно связан с понятием «геттер», что обычно не то, что вам нужно. Используйте get когда вы получаете что-то из оперативной памяти. Примеры:
        ```python
        class Something:
            ...

            # это приемлимо
            def get_very_important_thing(self):
                return self._one_thing * self._another_thing + self._GIGA_CONST


        class HttpFetcher:
            # плохо, не отражает семантику
            def get_http_result(self):
                self._http_connection.get(...)

        class HttpFetcher:
            # лучше, функция fetch известна на фронте + все +- знают,
            # что fetch процесс, протяженный во времени
            def fetch_http_result(self):
                self._http_connection.get(...)

        class SomethingWithCache:
            # плохо
            def get_cache_key(self, user_id):
                return self._cache_key + str(user_id)

        class SomethingWithCache:
            # нормально
            def build_cache_key(self, user_id):
                return self._cache_key + str(user_id)
        ```
        Используйте разные слова. Fetch, retrieve, download, parse, build, create, make, prepare и так далее. Слов много, и многие из них лучше отражают смысл происходящего. А если вы хотите увидеть, что происходит, когда слово get не ограничено, то сходите в исходники django, там префикс имеет гигантское распостранение и это делает код менее понятным
1. Все переменные имеет смысл аннотировать `typing.Final` (встроенный модуль импортируется целиком). Часто ошибки допускают во время изменения переменных (во время чтения их допустить сложно), поэтому неизменяемость помогает нам автоматом «отсекать» многие ошибки ещё статическом этапе, то есть, до запуска кода. Для упрощения этого у нас есть [отдельный пакет](https://github.com/vrslev/auto-typing-final).<br>
    Например, вместо:
    ```python
    some_cool_var = 10

    def do_some_important_thing(hello: str) -> None:
        hello_guys = f'{hello}{some_cool_var}'
        print(hello_guys)
    ```
    Можно сделать вот это:
    ```python
    # полный тип выведется сам и будет typing.Final[typing.Literal[10]]
    some_cool_var: typing.Final = 10

    def do_some_important_thing(hello: str) -> None:
        # полный тип выведется сам и будет typing.Final[str]
        hello_guys: typing.Final = f'{hello}{some_cool_var}'
        print(hello_guys)
    ```
1. PEP'ы, которым мы следуем:
    1. https://www.python.org/dev/peps/pep-0008/
    1. https://www.python.org/dev/peps/pep-0257/
    1. https://www.python.org/dev/peps/pep-0526/
    1. https://www.python.org/dev/peps/pep-0484/
    1. https://www.python.org/dev/peps/pep-0518/
    1. https://www.python.org/dev/peps/pep-0585/
