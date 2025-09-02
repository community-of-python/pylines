# Гайд по SOLID

> ⚠️ **Warning:** Этот гайд в процессе написания и ОЧЕНЬ СЫРОЙ, поэтому может быть всякое страшное, используйте аккуратно :)

- [Гайд по SOLID](#гайд-по-solid)
    - [Что такое SOLID?](#что-такое-solid)
    - [Почему SOLID?](#почему-solid)
    - [Почему собственный гайд? Ведь уже есть много других](#почему-собственный-гайд-ведь-уже-есть-много-других)
    - [Классические проблемы SOLID или ситуация «да, но»](#классические-проблемы-solid-или-ситуация-да-но)
    - [Важные примечания](#важные-примечания)
- [Принципы](#принципы)
  - [Принцип единой ответственности (Single Responsibility Principle, SRP)](#принцип-единой-ответственности-single-responsibility-principle-srp)
  - [Принцип открытости/закрытости (Open/Closed Principle, OCP)](#принцип-открытостизакрытости-openclosed-principle-ocp)
      - [Пример](#пример)
      - [Итоги](#итоги)
  - [Принцип подстановки Лисков (Liskov Substitution Principle, LSP)](#принцип-подстановки-лисков-liskov-substitution-principle-lsp)
  - [Принцип разделения интерфейсов (Interface Segregation Principle, ISP)](#принцип-разделения-интерфейсов-interface-segregation-principle-isp)
  - [Принцип инверсии зависимостей (Dependency Inversion Principle, DIP)](#принцип-инверсии-зависимостей-dependency-inversion-principle-dip)
    - [Об инъекции (Dependency Injection, DI)](#об-инъекции-dependency-injection-di)
    - [Пример без использования принципа инверсии зависимостей, но с инъекцией](#пример-без-использования-принципа-инверсии-зависимостей-но-с-инъекцией)

Этот гайд поможет разработчикам понимать принципы SOLID и применять их в реальных проектах. Разберём примеры кода, покажем, какие проблемы могут возникнуть при нарушении этих принципов, и предложим способы их устранения.

### Что такое SOLID?

SOLID — это набор принципов от Роберта Мартина. Роберт Мартин — консультант по написанию программного обеспечения, а не разработчик, поэтому его книги не очень просто читать разработчикам, однако они считаются очень авторитетными многими людьми из индустрии. Так же существует мнение, что Роберт Мартин — «инфобизнесмен». Мы не делаем выводов на его счёт, однако считаем его принципы SOLID полезными.

### Почему SOLID?

Принципы SOLID на нашей практике показывают себя хорошо (т.е. мы для себя это обосновали эмпирически — мы их применяли и, на наш взгляд, они показали пользу):
* код проще изучать  
* код проще тестировать  
* легче онбордиться в команде

Из некоторых минусов можно отметить то, что код становится чуть более многословным и его становится чуть больше.

### Почему собственный гайд? Ведь уже есть много других

Большинство гайдов в интернете страдает от нескольких вещей:

* сухое изложение принципов без объяснения сути  
* копирование одной и той же информации из раза в раз без добавления новой информации  
* игнорирование оригинальных текстов, неточное их цитирование  
* при прочтении гайда нет понимания как практически это применять

Поэтому, принципы SOLID так сложно применять в жизни и почти все на вопрос о принципах SOLID отвечают что-то размытое.  
Мы пишем свой гайд для того, чтобы у читающих была возможность его действительно практически применять.

### Классические проблемы SOLID или ситуация «да, но»

Почти все разговоры на собеседованиях или в целом о SOLID часто сводятся к следующему утверждению: «SOLID — это хорошо/отлично/здорово/надо применять/нужно всем/база».  
Следующий вопрос, который мы обычно задаем: «а как вы внедряли SOLID». И вот тут рождаются фразы, которые каждый наш интервьюер слышал много раз:

* «я SOLID чувствую интуитивно»  
* «SOLID сам собой получается от здравого смысла»  
* «SOLID это очевидно»

По факту, сами принципы SOLID изложены в книге Agile software patterns, principles and development 2003 года и занимают около 30 страниц текста и сложны в такой степени, что без осмысления и рефлексии их применять невозможно, тем более «интуитивно» (вы не родились с ощущением SOLID). Откуда появляется эта «интуитивность» мы попробуем рассказать далее.  
Кстати говоря, оригинальная публикация почти всеми гайдами игнорируется и зачастую даже ссылок на неё получить в этих гайдах невозможно, поэтому почти всегда вопрос «а откуда вы знаете о SOLID» к ней не приводит.  
В нашем же гайде мы полагаемся на первоисточник и стараемся это дополнять нашим же опытом.

### Важные примечания

* применять SOLID стоит осознанно, никакого «самостоятельного», «интуитивного» пути нет  
* необходимо использовать mypy (или red_knot, когда его сделают) и покрывать весь код 100% аннотациями типов (кроме тех случаев, когда mypy сам выводит типы)  
* интерфейс — это либо набор публичных методов (без подчеркиваний), либо abc, либо typing.Protocol
* мы трактуем, что SOLID — это про ООП, и применяем его для ООП (но не отрицаем, что какие-то из принципов применимы и за рамками ООП)

# Принципы
Здесь и далее изложена наша трактовка SOLID принципов. В качестве первоисточника мы используем [Agile software patterns, principles and development](https://dl.ebooksworld.ir/motoman/Pearson.Agile.Software.Development.Principles.Patterns.and.Practices.www.EBooksWorld.ir.pdf) от [Роберта Мартина](https://www.google.com/search?q=robert+martin+in+the+bathrobe&sca_esv=e98085266670db2f&rlz=1C5GCEM_enRU1156RU1162&udm=2&biw=1728&bih=958&sxsrf=AE3TifPGpbG0VjeuheuWgJOeImA0eGKkmw%3A1751981495217&ei=tx1taM-EDZK4wPAP6eyc2Q0&ved=0ahUKEwiPvLPVr62OAxUSHBAIHWk2J9sQ4dUDCBA&uact=5&oq=robert+martin+in+the+bathrobe&gs_lp=EgNpbWciHXJvYmVydCBtYXJ0aW4gaW4gdGhlIGJhdGhyb2JlSKVmUI0OWLVlcAp4AJABAZgBlwOgAfEbqgEIMzcuMS40LTG4AQPIAQD4AQGYAgygAuIGwgIGEAAYBxgewgIIEAAYBxgKGB7CAggQABgHGAgYHsICBxAjGCcYyQLCAgUQABiABMICBxAAGIAEGBPCAgoQABiABBgTGMcDwgIGEAAYExgewgIIEAAYExgIGB6YAwCIBgGSBwIxMqAHlDyyBwIxMLgH4AbCBwUyLjcuM8gHGw&sclient=img#vhid=ZrTVGSeCQAXVKM&vssid=mosaic).

## Принцип единой ответственности (Single Responsibility Principle, SRP)

> A class should have only one reason to change

Если переводить с английского, то приблизительный смысл может звучать так: «класс имеет одну причину для изменений». Что такое причина? Слово «причина» (reason) вызвало непонимание длинной в множество лет, поэтому в 2014 году Мартин [написал статью, которая разъясняет это слово](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html). Проблема в том, что даже эта статья даёт нам лишь приблизительные ориентиры. А мы с вами пишем конкретный код. Собирая всё вместе, сформулируем идеи, к которым мы пришли в процессе применения принципа:

* в корне SRP принципа лежит идея разделения ответственности. Стоит помнить о ней при написании кода. Т.е. код лучше разделять на куски, каждый из которых реализует очень конкретный и маленький кусок логики  
* слово «причина» которая лежит в основе SRP — это ваша командная договоренность. Вы внутри команды должны договориться о том, что является причиной для изменений. Аргументом почему это нужно делать является код, иллюстрирующий работу с модемом \[вставить сюда код с модемом\]. У нас есть 4 метода и программисты бьются на несколько групп. Кто-то считает, что ответственность едина — мы, ведь, работаем с модемом. Работа с модемом — это ответственность, и причина изменений. Кто-то считает, что работа с каналом связи — это одна причина для изменений, а работа с передачей данных — другая. Если мы с вами будем пытаться решить кто из них прав, то сойдем с ума. А нам платят не за философию, поэтому мы предлагаем вам выбрать (и выбирать в будущем) ваши причины и ответственности внутри команды самостоятельно (кстати, на мой вкус, один класс модема — это вполне SRP).

Возникает вопрос — «а как нам договориться внутри команды о трактовке слова причина?». Подход довольно прост — мы можем это уточнять в процессе ревью. А изначально можно выбирать исходя из вашего чувства прекрасного или обратившись в сообщество за примерами.  
Кстати, этот принцип претендует на первое место среди двух принципов, благодаря которым программисты «интуитивно чувствуют SOLID». Из-за его обманчивой простоты появляется это ложное чувство. Как мы проиллюстрировали, это очень непростой принцип с неоднозначной трактовкой. И всего лишь из-за слова «причина».

Пример кода, который нарушает SRP принцип:

```python
@dataclasses.dataclass  
class UserService:  
    database_host: str  
    database_port: str  
    kafka_topic: str  
    kafka_host: str  
   
    async def create_user(self, user_data: UserData) -> None:  
        database_connection = asyncpg.connect(self.database_host, self.database_port)  
        await database_connection.execute("INSERT INTO users ...")  
   
        kafka_connection = aiokafka.connect(self.kafka_host)  
        await kafka_connection.send(user_data, self.kafka_topic)  
   
    async def delete_user(self, user_id: str) -> None:  
        database_connection = asyncpg.connect(self.database_host, self.database_port)  
        await database_connection.execute("DELETE FROM users WHERE ...")  
        ...
        kafka_connection = aiokafka.connect(self.kafka_host)  
        await kafka_connection.send(user_data, self.kafka_topic)
```

Данный класс отвечает не только за работу с пользователями, но ещё в себе содержит подключение к kafka, postgres. Получается, что он несет ответственность за подключения к этим компонентам инфраструктуры, хотя его основная задача работать с пользователями (мы делаем этот вывод по семантике кода). Минусы заключаются в том, что такой код хрупкий и его сложно тестировать, потому что придётся заводить множество моков, а в частности патчить. Это плохо, потому что вместо проверки нашего кода на нужное нам поведение (создание и удаление пользователей), мы будем вынуждены в тестах как-то патчить соединения с кафкой и постгресом, а это магические действия с неизвестными последствиями. Мы потеряли чистоту кодовой базы сразу в двух местах, получили «магические» действия и повысили хрупкость кода (любые изменения в библиотеках, механизмах патчинга — и вы получите ошибки, которые никак не связаны с тем, что делает UserService).  
В данном случае может показаться, что «а чего такого? ну запатчу», и это резонный комментарий, в данном маленьком примере, конечно, ничего страшного не произойдет. Код будет похуже, более хрупкий, но все это не кажется критическим. Дело в том, что этот пример выглядит плохо на масштабе. Когда в вашей кодовой базе это становится основным подходом, то все начинает быть хрупким и неустойчивым.  
Что можно здесь улучшить? Отказаться от инстанцирования подключений внутри и передавать их в качестве аргументов классу.
Итого, мы бы написали что-то такое, чтобы соблюсти SRP:

```python
import dataclasses
import asyncpg
import aiokafka

@dataclasses.dataclass
class UserService:
    database_connection: asyncpg.Connection
    kafka_producer: aiokafka.AIOKafkaProducer
    kafka_topic: str

    async def create_user(self, user_data: "UserData") -> None:
        await self.database_connection.execute("INSERT INTO users ...", user_data)
        await self.kafka_producer.send_and_wait(self.kafka_topic, user_data)

    async def delete_user(self, user_id: str) -> None:
        await self.database_connection.execute("DELETE FROM users WHERE id = $1", user_id)
        ...
        await self.kafka_producer.send(user_data, self.kafka_topic)
```

## Принцип открытости/закрытости (Open/Closed Principle, OCP)

> Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification

Второй «тот самый принцип», из-за которого формируется ложное ощущение «интуитивности» SOLID (помните, мы говорили об этом в начале статьи). Этот принцип сформулирован сложнее SRP, но его суть гораздо ближе к базовым идеям, которым учат каждого программиста. Поэтому, он тоже может «обмануть» человека, который впервые ознакамливается с SOLID.  
Переводя принцип на русский получим что-то вроде «программные сущности (классы, модули, функции и так далее) должны быть открыты для расширения, но закрыты для модификации». Проблема формулировки здесь в том, что непонятно что такое «расширение» и что такое «модификация». И даже после чтения книги намного понятнее не становится.

Поэтому вот наша трактовка.  
Принцип, по сути, описывает следующую идею: пишите код так, чтобы вы могли вносить в него новую функциональность без переписывания старого, а путем написания нового. Т.е. если вы пишете код, который вам понадобится уже в следующем пуллреквесте «рефакторить» (читай удалять), то принцип OCP вы скорее всего нарушаете  
Сама идея практически понятна для всех программистов. По сути, нас с самого начала учат, что когда нам надо написать функцию, которая складывает 2 \+ 3, мы пишем sum_two_numbers = lambda a,b: a \+ b, sum_two_numbers(2, 3), а не просто «2 \+ 3» в коде. Это базовое умение программиста — обобщать задачи. По сути, OCP очень близко к этой идее, мы здесь достаточным образом обобщаем функциональность, думаем о будущем и позволяем будущим нам или нашим коллегам не переписывая нашего кода добавлять новые функции в наш продукт  
Однако, все это становится куда менее понятным, когда мы практикуем этот принцип в «развесистом» ооп коде, который нам приходится писать. Понятно ли как написать класс, который будет расширяться, но не переписываться? Какие функции бизнес захочет завтра? Как сделать так, чтобы модуль, который мы пишем для сегодняшней задачи, нам не понадобилось уже завтра переименовывать и переписывать? На эти вопросы, на самом деле, нет прямых ответов. И, возвращаясь к предыдущему, нам платят не за философию, поэтому превратим это в практическое руководство к действию:

* наша задача продумать возможность расширения ооп кода таким образом, чтобы не понадобилось этот код переписывать завтра  
* т.к. это сложно, вы можете отслеживать нарушение принципа — если вы видите, что вы или ваш коллега часто переписывает один и тот же код, считайте что у вас проблема с OCP  
* если у вас есть проблема с OCP — ваша задача переписать этот код так, чтобы в следующий раз вам не понадобилось его переписывать вновь  
* нет нужды следовать принципу фанатично. Т.е. если вы столкнулись переписыванием одного и того же кода, устранили проблему, но иногда небольшими (определите внутри что такое «небольшими», на мой взгляд 1-5 строк, может 10\)  кусками продолжаете его изменять, то в этом, вероятно, нет большой проблемы  
* лучше не изнурять себя неукоснительным соблюдением принципа потому, что вы можете развить в себе невроз, так и не достигнув сто процентного соблюдения OCP

#### Пример
Мы пишем код, где `run_command` исполняет команду по имени, это входная точка логики CLI:

```python
def run_command(command_name, **options):
    if command_name == "list-pods":
        return list_pods(**options)
    elif command_name == "scale":
        return scale(**options)
    elif command_name == "--help":
        print("Available commands: list-pods, scale")
        return
    raise SystemExit(f"Unknown command: {command_name}")
```

Добавим новую команду `delete-pod`:

```python
def run_command(command_name, **options):
    if command_name == "list-pods":
        return list_pods(**options)
    elif command_name == "scale":
        return scale(**options)
    elif command_name == "delete-pod":
        return delete_pod(**options)
    elif command_name == "--help":
        print("Available commands: list-pods, scale, delete-pod")
        return
    raise SystemExit(f"Ты чего, '{command_name}' — это вообще кто такой?")
```

При добавлении новых команд можно случайно повлиять на работоспособность других команд и забыть изменить `--help`. Чтобы это исправить, стоит сделать код более общим. Можно использовать маппинг названия команды к хэндлеру:

```python
AVAILABLE_COMMANDS = {
    "list-pods": list_pods,
    "scale": scale,
    "delete-pod": delete_pod,  # если есть — добавляй сюда
}

def run_command(command_name, **options):
    if command_name == "--help":
        print(f"Available commands: {', '.join(AVAILABLE_COMMANDS)}")
        return

    if command_handler := AVAILABLE_COMMANDS.get(command_name):
        return command_handler(**options)

    raise SystemExit(f"Ты чё творишь, [NAME]? Такой команды нет: '{command_name}'")
```

Теперь для добавления новой команды достаточно изменить `AVAILABLE_COMMANDS`:

```python
AVAILABLE_COMMANDS = {
    "list-pods": list_pods,
    "scale": scale,
    "delete-pod": delete_pod,
}
```

В какой-то момент развития функция `run_command` может стать слишком сложной, и мы захотим протестировать логику выполнения команды отдельно от самих команд.  Тогда можно создать класс `CommandRunner`, который будет принимать доступные команды при инициализации:

```python
class CommandRunner:
    def __init__(self, available_commands):
        self.available_commands = available_commands

    def run_command(self, command_name, **options):
        if command_name == "--help":
            print(f"Available commands: {', '.join(self.available_commands)}")
            return

        if command_handler := self.available_commands.get(command_name):
            return command_handler(**options)

        raise SystemExit(f"Ты чё, '{command_name}' — не в списке, [ИМЯ].")
```

При проектировании стоит стремиться к тому, чтобы в будущем приходилось как можно реже рефакторить существующий код, и вместо этого можно было добавлять новый.

#### Итоги
Попробуем сформулировать правила для поиска нарушений OCP:
* искать претенденты для обобщения — однообразный код и цепочки if-ов
* смотреть на ваши пуллреквесты, если в них удаляется код так же часто как добавляется — это тревожный признак. Особенно, если вы удаляете старый код при добавлении новой функциональности, это уже подсвечивает проблему — вы нарушаете OCP принцип

## Принцип подстановки Лисков (Liskov Substitution Principle, LSP)

> Subtypes must be substitutable for their base types

Как иногда говорят на собеседованиях «в питоне нет типов», что обычно воспринимается как некорректный ответ. Однако, всегда понятно откуда в данном случае «растут корни» — типизация в питоне работает в рантайме и разработчику не очень-то заметна. Разработчику на питоне нет нужды думать о типах большую часть времени, поэтому для некоторых разработчиков этих самых типов как будто «нет». Всё ещё запутывают аннотации типов, которые часто называют типизацией. И добивает это всё наличие статически типизированных, компилируемых языков.  
Поэтому, когда мы читаем оригинальную трактовку LSP принципа, то возникает вопрос — «а применимо ли это к питону?». Здесь я бы вспомнил, что SOLID — в первую очередь про ООП (в нашей трактовке). Поэтому, мы у себя слово «типы» заменяем на «классы». И получается, что принцип (не очень точный перевод на русский) «типы должны заменяться на подтипы без нарушения работы программы» мы можем перефразировать как «классы должны заменяться на подклассы без нарушения работы программы» для Python.  
Наш подход к этому принципу такой: чтобы достичь LSP, в первую очередь нам необходимо покрывать код аннотациями типов полностью. К сожалению даже так, **не все** кейсы закрываются аннотациями, но, тем не менее, большая часть всё таки закрывается.

Чтобы вас не мучать сразу приведём пример случая, который не покрывается mypy:

```python  
class ParentShape:  
    ...

class Circle(ParentShape):  
    def draw_shape(self) -> None:  
        ...

class Rectangle(ParentShape):  
    def draw_shape(self) -> None:  
        ...

# аннотация ParentShape — источник нарушения LSP  
def draw_some_shape(one_shape: ParentShape) -> None:  
    # нарушение принципа OCP  
    if isinstance(one_shape, Circle) or isinstance(one_shape, Rectangle):  
        one_shape.draw_shape()  
```

Это нарушение и LSP и OCP принципов сразу. OCP нарушается потому, что каждый раз, когда мы захотим добавить новую фигуру, нам надо будет менять код \`draw_some_shape\`. LSP нарушается потому, что в предке ParentShape нет метода draw_shape. А это означает, что если мы хотим в программе ParentShape заменить на Circle, например, то LSP принцип будет нарушен, т.к. невозможно это сделать без нарушения функционирования программы. При этом, мы понимаем, что код с isinstance плохой, но это не каждому разработчику очевидно, этот код здесь довольно «натянутый». Есть сложность и с ParentShape. Мы с вами понимаем, что это некий «базовый» класс, чей прямой инстанс по коду мы, скорее всего, не встретим. Однако, знание, что это нарушает LSP, нас здесь толкает либо к тому, чтобы отказаться от ParentShape в пользу Protocol, добавить к нему метод draw_shape, указывать union типов Circle | Rectangle или воспользоваться (не стоит) Any. Я бы выбрал Protocol, тогда из проблем в коде останется только нарушение OCP принципа. Конечно, реальные программисты так редко пишут, но это всё таки случается.  
Важный дополнительный вывод: нарушение LSP появляется не когда мы пишем классы, а когда их применяем.

А теперь рассмотрим более очевидный пример. Он показывает как сломается программа, если мы заменим класс Animal на класс Dog по всему нашему коду:

```python  
class Animal:  
    def make_sound(self):  
        return "generic sound"

class Dog(Animal):  
    def make_sound(self):  
        return ["гав", "гав"]

def listen(animal: Animal):  
    print(animal.make_sound().upper())


listen(Animal())  
listen(Dog()) # Ошибка: 'list' object has no attribute 'upper'  
```

Нарушение LSP принципа произошло в том, что мы написали класс Dog и метод make_sound в нём таким образом, что возвращаемый тип полностью отличен от предка. Если мы добавим сюда аннотации типов, то mypy не даст нам совершить такую ошибку.

Вот и ещё пример нарушения LSP:

```python  
class Bird:  
   def fly(self):  
       ...

class Penguin(Bird):  
   def fly(self):  
       raise NotImplementedError("...")  
```  
Такое нарушение mypy так же не сможет «поймать», хотя здесь мы нарушаем сразу и LSP и ISP принципы. Нарушение LSP происходит потому, что если мы заменим в программе Bird на Penguin, то вызовы метода fly совсем не будут ожидать ошибки. ISP же мы нарушаем, т.к. «потребителю» Penguin не нужен метод fly, но он его получает. Совершенно очевидно, что в таком случае Penguin не должен быть «потомком» Bird, тогда и наши проблемы исчезнут. Данный пример очень «картонный», а в реальной жизни обычно такие случаи устроены сложнее, однако на этом примере легко иллюстрировать проблемы.

Как мы видим, LSP принцип легко соблюдать, но при этом легко нарушать, указав неправильные типы и даже неправильно организовав наследование. Во многом вам здесь помогает mypy, но иногда даже он не может понять есть ли нарушение и здесь вам стоит полагаться на свою внимательность и процесс код ревью.

Аргументы в пользу соблюдения LSP:  
— помогает устойчиво работать с полиморфизмом  
— помогает достигать более чистого ООП дизайна, т.е. код становится более читаемым  
— позволяет достигать большей безопасности вашего кода. Т.к. при расширении кодовой базы мы с меньшей вероятностью сломаем код  
— позволяет достигать расширяемости кода, потому, что LSP — это enabler для OCP

## Принцип разделения интерфейсов (Interface Segregation Principle, ISP)

> Clients should not be forced to depend on methods that they do not use.

Наша трактовка этого принципа адаптирована для python: интерфейсы (здесь референс к началу ^) не должны содержать методов, которыми не будут пользоваться клиенты; стоит делать раздельные маленькие интерфейсы для разных клиентов, исходя из их потребностей.  
Иными словами, если вы пишите интерфейс для того, чтобы его использовали в какой-то части кода и там нужно три метода, то пишите три метода, не стоит писать 10 или 15 методов «про запас». В оригинальной трактовке сформулирована идея, что клиент не должен зависеть от методов, которыми не пользуется. Но в питоне, благодаря duck typing, не похоже чтобы мы «зависели» напрямую от методов, которыми не пользуемся. Рассмотрим такой кейс:

```python
import typing

class SmartHomeDevice(typing.Protocol):
    def turn_on(self) -> None: ...
    def turn_off(self) -> None: ...
    def set_temperature(self, value: float) -> None: ...
    def play_music(self, track: str) -> None: ...

class SmartLight:
    def turn_on(self) -> None:
        print("Light on")
    def turn_off(self) -> None:
        print("Light off")
    # Лампочка не умеет регулировать температуру и проигрывать музыку,
    # но типизатор требует реализовать все методы:
    def set_temperature(self, value: float) -> None:
        raise NotImplementedError("Light can't set temperature")
    def play_music(self, track: str) -> None:
        raise NotImplementedError("Light can't play music")

def activate(device: SmartHomeDevice):
    device.turn_on()


lamp = SmartLight()
activate(lamp)
```

Лампочка вынуждена реализовать методы для температуры и музыки, которые ей не нужны.
Если добавить новое действие (например, "открыть шторы"), все классы должны будут добавить ещё одну заглушку.
mypy будет ругаться, если методы не реализованы, но в рантайме ошибки NotImplementedError могут всплыть неожиданно.
Принцип разделения интерфейсов:
Интерфейс должен содержать только те методы, которые нужны конкретному клиенту, — выделяем отдельные интерфейсы для разных функций.

Давайте рассмотрим ещё один пример. Девайс 3-в-1, который может печатать, сканировать и отправлять факс:

```python
class AllInOneDevice:
    def print(self, document: Document) -> None:
        print(f"printing {document}")

    def scan(self) -> Document:
        print("scanning")
        return Document("scanned content")

    def fax(self, document: Document) -> None:
        print(f"faxing {document}")

def make_a_copy(device: AllInOneDevice) -> None:
    scanned_document = device.scan()
    device.print(scanned_document)

make_a_copy(device=AllInOneDevice())
```

Функция `make_a_copy` зависит от девайса с методом `fax`, который не использует, а ещё она ожидает, что один девайс будет и сканировать, и печатать документ. Разделим интерфейсы:

```python
import typing

class CanPrint(typing.Protocol):
    def print(self, document: Document) -> None:
        ...

class CanScan(typing.Protocol):
    def scan(self) -> Document:
        ...

class CanFax(typing.Protocol):
    def fax(self, document: Document) -> None:
        ...

def make_a_copy(scanner: CanScan, printer: CanPrint) -> None:
    scanned_document = scanner.scan()
    printer.print(scanned_document)
```

Теперь мы можем использовать разные девайсы для сканирования и печати, и для использования `make_a_copy` не придётся имплементировать `Fax`:

```python
class Printer:
    def print(self, document: Document) -> None:
        print(f"printing {document}")

class Scanner:
    def scan(self) -> Document:
        print("scanning")
        return Document("scanned content")


make_a_copy(scanner=Scanner(), printer=Printer())
```

Почему так лучше:

- Клиентская функция `make_a_copy` зависит только от необходимых интерфейсов — **снижение [связности](https://ru.wikipedia.org/wiki/Зацепление_\(программирование\))**.  
- Сканирование и печать могут быть реализованы разными девайсами — **гибкость и расширяемость**.

## Принцип инверсии зависимостей (Dependency Inversion Principle, DIP)

> a. High-level modules should not depend on low-level modules. Both should depend on abstractions.  
> b. Abstractions should not depend on details. Details should depend on abstractions.

Высокоуровневые модули должны зависеть от абстракций, а не завязываться на конкретных реализациях — так звучит принцип в вольном переводе на русский язык. Можно перефразировать: «в качестве зависимостей полагайтесь на абстракции, а не конкретную реализацию». Здесь возникают вопросы. Для начала, что такое абстракция (термин из ооп, абстрактный класс, протокол, просто какой-то класс)? Под абстракцией конкретно мы (впрочем, Мартин идёт туда же) понимаем «интерфейс» (определение в начале статьи). А что такое зависимость? С этим чуть сложнее, но мы предполагаем, что если какой-то части кода нужна другая часть кода для выполнения своих задач, то мы считаем, что последняя часть является зависимостью для первой. Например: если есть класс A и метод get_some, а в нём для работы нам понадобится класс B и его метод get_another, то получается, что класс A зависит от класса B.

И вот мы подходим к DI паттерну. Это тема, которая отличается от DIP принципа. Давайте для начала разберемся, что такое DI паттерн. Вот наглядный пример DI паттерна:

```python  
# Плохо:  
class CrmClient:  
   def fetch_user_balance_from_crm(self, user_uuid: str) -> decimal.Decimal:  
       httpx_connection: httpx.Client = httpx.Client(...)  
       ...

# «Ручной» DI, мы ожидаем зависимость снаружи:  
class CrmClient:  
   def fetch_user_balance_from_crm(self, httpx_connection: httpx.Client, user_uuid: str) -> decimal.Decimal:  
       ...

# «Ручной» DI можно сделать лучше:  
@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)  # избавляет от бойлерплейта, уменьшает количество ошибок \+ память  
class CrmClient:  
   # теперь можно CrmClient разместить в DI фреймворке и получать httpx.Client снаружи  
   # а можно просто создавать его руками, если вы не хотите брать DI фреймворк  
   httpx_connection: httpx.Client

   def fetch_user_balance_from_crm(self, user_uuid: str) -> decimal.Decimal:  
       …  
```

DI паттерн — это наш повседневный инструмент и мы верим в то, что он позволяет делать код проще и чище, удобнее для тестирования. Однако, как он связан с принципом DIP (возвращаясь к SOLID)? Прямой зависимости между ними нет, однако мы верим, что DI паттерн — это подход, помогающий воплощать DIP в жизнь. Однако, полностью его внедрив, DIP мы не достигнем. Потому что в определении сказано, что мы должны полагаться на абстракции, а не конкретную реализацию. Тогда как в DI мы часто используем конкретные реализации. Но, вспоминая утиную типизацию в python, мы можем быть уверены, что в тестах эти конкретные реализации мы можем подменять на моки, которые реализуют только нужные нам методы. Почему, вдруг, мы пишем про это? На наш взгляд, Мартин как раз исходя из потребностей тестируемости рекомендует завязываться на абстракции. Питон «исправляет» это своей гибкой природой. Поэтому, выходит, что мы вроде бы, внедряя DI, DIP не достигаем, а вроде бы, учитывая утиную типизацию, достигаем. Можно ли сказать, что мы однозначно правы? Наверное, нет, но мы предпочитаем считать, что формула «DI \+ утиная типизация = DIP» верна.

Следующий этап — это когда DI паттерн объединяем с DI фреймворком и где-то на горизонте начинает маячить термин IoC — inversion of control. Что ужасного в этом термине? Во-первых, он спутывается с термином DIP. Во-вторых, по нему нет консенсуса — что это такое, а в ряде русскоязычных телеграм чатов вас вообще перетрут в пыль, если вы поднимите вопрос IoC. Мы понимаем под IoC использование DI-«контейнеров» (мы их ещё называем IoC контейнерами), это когда нужные зависимости собираются в объект или объекты, где они определены в виде декларативных атрибутов, которые ссылаются друг на друга, этакий декларативный граф зависимостей вашего приложения. Вот пример:  
```python
from that_depends import providers

class Container(BaseContainer):
    my_local_config = providers.Singleton(Config)
    db_session = providers.Factory(create_db_session, config=my_local_config.db) 
    user_repository = providers.Factory(
        UserRepository,
        my_local_config.users,
        session=db_session
    )
```

Тут, наверное, возникает философский вопрос — как нам различать что должно попадать в DI-контейнер, а что должно оставаться простым импортом. Здесь можно исходить из правила, что если это (не все признаки, но большая часть):  
— объект (класс)  
— он зависит от других объектов или является их зависимостью  
— используется в нескольких местах  
— его нужно регулярно инстанцировать

То тогда такую «штуку» имеет смысл размещать в DI-контейнере. Классический пример — соединение с базой данных.

`OrderProcessor` использует `MailNotifier` для отправки писем о заказах:

```python
class MailNotifier:
    def __init__(self, login: str, password: str) -> None:
        pass

    def notify(self, message: str) -> None:
        print("sending an email...")

class OrderProcessor:
    def __init__(self, notifier: MailNotifier) -> None:
        self.notifier = notifier

    def process_order(self, items: list[Item]) -> None:
        order = Order(items=items)
        self.notifier.notify(f"Your order {order.id} will be shipped soon!")


notifier = MailNotifier(settings.email_login, settings.email_password)
processor = OrderProcessor(notifier=notifier)
processor.process_order(items=...)
```

Предположим, требования изменились, и теперь мы хотим отправлять смс вместо писем. Для этого заменим `MailNotifier` на `SMSNotifier`::

```python
class Notifier:
    def notify(self, message: str) -> None:
        ...

class MailNotifier(Notifier):
    def __init__(self, login: str, password: str) -> None:
        pass

    def notify(self, message: str) -> None:
        print("sending an email...")

class SMSNotifier(Notifier):
    def __init__(self, api_key: str) -> None:
        pass

    def notify(self, message: str) -> None:
        print("sending an SMS...")

class OrderProcessor:
    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier

    def process_order(self, items: list[Item]) -> None:
        order = Order(items=items)
        self.notifier.notify(f"Your order {order.id} will be shipped soon!")


notifier = SMSNotifier(settings.sms_api_key)
processor = OrderProcessor(notifier=notifier)
processor.process_order(items=...)
```

Чтобы не было необходимости менять `OrderProcessor` каждый раз, когда меняется способ нотификации, стоит создать интерфейс `Notifier`, и передавать в `OrderProcessor.__init__` объект, соответствующий этому интерфейсу:

```python
import typing

class Notifier(typing.Protocol):
    def notify(self, message: str) -> None: ...

class OrderProcessor:
    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier

    def process_order(self, items: list[Item]) -> None:
        order = Order(items=items)
        self.notifier.notify(f"Your order {order.id} will be shipped soon!")

class EmailNotifier(Notifier):
    def __init__(self, login: str, password: str) -> None:
        pass

    def notify(self, message: str) -> None:
        print("sending an email...")

class SMSNotifier(Notifier):
    def __init__(self, sms_service_api_key: str) -> None:
        pass

    def notify(self, message: str) -> None:
        print("sending an sms...")

OrderProcessor(notifier=SMSNotifier(settings.sms_service_api_key)).process_order(items=...)
```

### Об инъекции (Dependency Injection, DI)

В примере мы также вынесли инициализацию `Notifier` из `OrderProcessor` в клиентский код — это делает `OrderProcessor` более гибким и устойчивым к изменениям. Инъекция зависимостей (DI, Dependency Injection) часто помогает достигать принципов SRP (принцип единой ответственности) и DIP (принцип инверсии зависимостей).

### Пример без использования принципа инверсии зависимостей, но с инъекцией

Если использовать принцип инверсии зависимостей во всём коде, то будет много шаблонного и повторяющегося кода. Возьмём пример FastAPI-приложения:

```python
import fastapi

class Todo:
    def __init__(self, description: str) -> None:
        self.description = description

class TodoService:
    def __init__(self) -> None:
        self.todos = []

    def get_todos(self) -> list[Todo]:
        return self.todos

    def add_todo(self, todo: Todo) -> Todo:
        self.todos.append(todo)
        return todo

application = fastapi.FastAPI()
todo_service = TodoService()

def get_todo_service() -> TodoService:
    return todo_service

@application.get("/todos/")
def get_todos(
    todo_service: TodoService = fastapi.Depends(get_todo_service),
) -> list[Todo]:
    return todo_service.get_todos()

@application.post("/todos/")
def add_todo(
    description: str,
    todo_service: TodoService = fastapi.Depends(get_todo_service),
) -> Todo:
    return todo_service.add_todo(todo=Todo(description=description))
```

Мы *можем* сделать абстрактный `TodoService` и реализовать его в `InMemoryTodoService`:

```python
import typing

class TodoService(typing.Protocol):
    def get_todos(self) -> list["Todo"]:
        ...

    def add_todo(self, todo: "Todo") -> "Todo":
        ...

class InMemoryTodoService:
    def __init__(self) -> None:
        self.todos = []

    def get_todos(self) -> list["Todo"]:
        return self.todos

    def add_todo(self, todo: "Todo") -> "Todo":
        self.todos.append(todo)
        return todo
```

Однако если мы не планируем поддерживать несколько имплементаций `TodoService` (например, in-memory и Postgres) и будем тестировать FastAPI-приложение интеграционно (не мокая `TodoService`), то можно обойтись без интерфейса.
