Title:Memoryview в python: как использовать и зачем
Date: 2023-04-10
Category: Python
Slug: memoryviews-why-and-how-to-use-them
Lang: ru

## Мотивация 

Иногда бывает необходимо поделиться сырыми данными с другой программой. К примеру, мы работаем с изображением и хотим отправить его в специализированную библиотеку, написанную на C++. При этом пересылка всего изображения может быть слишком излишней и мы хотим обработать его по частям. В этом случае мы можем использовать специальную структуру, которая позволяет эффективно работать с массивами сырых данных без создания копий объекта — memoryview.

## Об объектах memoryview

Объекты memoryview позволяют делиться участками памяти интерпретатора. Объекты memoryview можно получить из объектов, которые поддерживают протокол для работы с программами на языке C (buffer protocol). В python — это bytes и bytearray. Работа с memoryview строится следующим образом: взять подходящий объект, создать из него объект memoryview, создавать срезы из memoryview без привлечения новой памяти.

**Пример использования:**

```
>>> v = memoryview(b'abcefg')
>>> print(type(v))
<class 'memoryview'>

>>> print(v[2])
99

>>> print(v[1:3])
<memory at 0x7f454a259000>

>>> print(bytes(v[1:3]))
b'bc'
```

**Пример сохранения памяти:**

Давайте теперь убедимся, что memoryview не выделяет дополнительную память под срезы. Для того, чтобы увидеть, сколько памяти используется, мы будет использовать стандартную библиотеку tracemalloc (https://docs.python.org/3/library/tracemalloc.html):

Для начала создадим объект bytes и убедимся, что при создании из него среза типа bytes, новая память выделяется:
```python
tracemalloc.start()
# create a byte sequence of 1000000 bytes
data = bytes(1000000)
# take a snapshot before making a slice
snapshot1 = tracemalloc.take_snapshot()
# slice! type(new_data) == 'bytes', its size is around 500 KB
new_data = data[:500000]

# take a snapshot after making the slice
snapshot2 = tracemalloc.take_snapshot()
tracemalloc.stop()

top_stats = snapshot2.compare_to(snapshot1, 'lineno')
print("[ Top 10 ]")
for stat in top_stats[:5]:
	print(stat)
```
получаем вывод (cpython):

```
<stdin>:1: size=1465 KiB (+488 KiB), count=2 (+1), average=732 KiB
/usr/lib/python3.10/tracemalloc.py:423: size=88 B (+88 B), count=2 (+2), average=44 B
/usr/lib/python3.10/tracemalloc.py:560: size=48 B (+48 B), count=1 (+1), average=48 B
/usr/lib/python3.10/tracemalloc.py:315: size=40 B (+40 B), count=1 (+1), average=40 B
<unknown>:0: size=9220 B (+0 B), count=10 (+0), average=922 B
```
Можно увидеть, что у нас было выделено дополнительно примерно 488 Кибибайт (488 * 1024 байта). Посмотрим, что будет, если использовать memoryview:

```python
tracemalloc.start()
# create a byte sequence of 1000000 bytes
data = bytes(1000000)

# take a snapshot before making a slice
snapshot1 = tracemalloc.take_snapshot()

# create memoryview
mview = memoryview(data)
# slice! type(new_data) == 'memoryview', shouldn't consume much memory
new_mdata = mview[:500000]

# take a snapshot after making the slice
snapshot2 = tracemalloc.take_snapshot()
tracemalloc.stop()

top_stats = snapshot2.compare_to(snapshot1, 'lineno')
print("[ Top 10 ]")
for stat in top_stats[:5]:
	print(stat)
```

получаем вывод (cpython):

```
<stdin>:1: size=977 KiB (+496 B), count=4 (+3), average=244 KiB
/usr/lib/python3.10/tracemalloc.py:423: size=88 B (+88 B), count=2 (+2), average=44 B
/usr/lib/python3.10/tracemalloc.py:560: size=48 B (+48 B), count=1 (+1), average=48 B
/usr/lib/python3.10/tracemalloc.py:315: size=40 B (+40 B), count=1 (+1), average=40 B
<unknown>:0: size=9220 B (+0 B), count=10 (+0), average=922 B
```

К исходному расходу памяти у нас прибавилось всего около 500 байт, несмотря на создание memoryview размером в 500 тысяч байт. Таким образом, новая память под элементы среза в memoryview не была выделена, мы буквально получаем ссылку на кусок уже существующей памяти.

## Заключение
Мы рассмотрели класс memoryview для предоставления доступа к сырой памяти. Обычно он используется, когда необходимо передать в более низкоуровневую библиотеку набор сырых байт, как они представлены в памяти, либо когда мы хотим работать со срезами байтовых объектов, но хотим предотвратить их многократное копирование. Срезы memoryview позволяют сэкономить и память, и время, однако, из-за своей узконаправленности и низкоуровневости используются достаточно редко.
