

# Cheat sheet
## Чтение данных и запись данных
| Функция | Пример | Комментарий |
|---------|--------|-------------|
| `read.csv()` | `spark.read.csv("file.csv", header=True, sep='\t', nullValue=r'\N')` | Чтение CSV файла с заголовком \N считается как Null |
| `read.text()` | `spark.read.text("file.txt")` | Чтение файла по строкам |
| `read.json()` | `spark.read.json("data.json")` | Чтение JSON файла |
| `read.parquet()` | `spark.read.parquet("data.parquet")` | Чтение Parquet файла |
| `write.csv()` | `df.write.csv("output.csv", mode="overwrite")` | Запись в CSV с перезаписью существующих данных |
| `write.parquet()` | `df.write.parquet("output.parquet")` | Запись в Parquet формат |

## Характеристики DataFrame
|  |  |
|--|--|
| df.show() | посмотреть данные |
| df.show(10, truncate=False) | не обрезать длинные строки |
| df.count() | число строк |
| df.printSchema() | вывести схему данных |
| df.columns | список имен колонок |
## Обращение к колонкам
|  |  |комментарий |
|--|--|--|
| по имени| "primaryTitle" | если функция принимает str |
| по атрибуту| df.primaryTitle | конфликтуют с атрибутами DataFrame, например, columns |
| по индексу| df["primaryTitle"] | нет подсказок IDE |
| через функцию col(column)| F.col("primaryTitle") | при import pyspark.sql.functions as F|

## Основные трансформации
| Функция | Пример | Комментарий |
|------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------|
| `df.filter()` | `df.filter(df.age > 18)` | Фильтрация строк: выбирает строки, где возраст больше 18 |
| `df.select()` | `df.select("name", df.age)` | Выбор конкретных колонок по именам |
| `df.limit()` | `df.limit(100)` | Ограничение DataFrame первыми 100 строками |
| `df.drop()` | `df.drop("temp_column")` | Удаление одной колонки по имени |
| `df.sort()` | `df.sort("salary")` | Сортировка по колонке по возрастанию (аналог orderBy) |
| `df.dropDuplicates()` | `df.dropDuplicates(["name", "city"])` | Удаление строк, где дублируются только указанные колонки |
| `df.withColumn()` | `df.withColumn("full", concat(col("first"), lit(" "), col("last")))` | Добавление новой колонки |

## Основные действия
| Функция | Пример | Комментарий |
|---------|--------|-------------|
| `df.count()` | `df.count()` | Возвращает общее количество строк |
| `df.collect()` | `data = df.limit(1000).collect()` | Собирает все данные на драйвер-ноде. **ВНИМАНИЕ**: Может вызвать OOM при больших объемах данных |

## Методы для работы со столбцами (Column)

| Метод | Пример | Комментарий |
|-------|--------|-------------|
| `col.contains()` | `df.filter(df.primaryTitle.contains("World"))` | Проверяет, содержит ли строка указанную подстроку. Регистрозависимый. |
| `col.isin()` | `df.filter(col("genre").isin("Comedy", "Drama", "Action"))` | Проверяет, находится ли значение в списке. |
| `col.like()` | `df.filter(col("name").like("Joh%"))` | SQL-like сопоставление с шаблоном. `%` - любая последовательность, `_` - любой символ. Регистрозависимый. |
| `col.rlike()` | `df.filter(col("email").rlike("^[a-zA-Z0-9.+]+@[a-zA-Z0-9]+\.[a-zA-Z]+$"))` | Проверяет соответствие регулярному выражению (Regex). |
| `col.ilike()` | `df.filter(col("title").ilike("%secret%"))` | Аналог `like`, но регистронезависимый. |
| `when().otherwise()` | `df.withColumn("category", F.when(df.price > 100, "expensive").otherwise("cheap"))` | Выбор колонки с условием. |
| `col.isNull()` | `df.filter(col("email").isNull())` | Проверяет, является ли значение `NULL`. |
| `col.isNotNull()` | `df.filter(col("email").isNotNull())` | Проверяет, что значение не `NULL`. |
| `col.isNaN()` | `df.filter(col("temperature").isNaN())` | Проверяет, является ли числовое значение `NaN` (Not a Number). |
| `col.cast()` | `df.select(df.age_string.cast("integer"))` | Приведение типа. Можно использовать строку или объект типа данных (`IntegerType()`, `StringType()`). |

## Сложные структуры данных
| Метод | Пример | Комментарий |
|-------|--------|-------------|
|F.split|F.split(title_basics_df.genres, ",")| Разбивает строку на массив (list) по заданному разделителю. |
|[0]|title_basics_df.genres[0]|Извлекает первый элемент из массива или строки |
|F.array_size|F.array_size("genres") > 1|Возвращает количество элементов в массиве |
|F.array_contains|F.array_contains(df.genres, 'Drama')|Проверяет, есть ли в массиве конкретное значение|
|F.explode|F.explode('genres')|	Разворачивает массив в отдельные строки |

## Использование UDF
| Метод | Пример | Комментарий |
|-------|--------|-------------|
|F.udf|F.udf(lambda x: unicodedata.normalize('NFC', x))('primaryName')|Создание UDF в одну строку
|@F.udf|@udf(returnType=T.StringType())<br>def my_func(x):<br>&nbsp;&nbsp;&nbsp;&nbsp;return x| Создание UDF через декорирование существующей функции |
## Группировка
| Функция | Пример | Комментарий |
|---------|--------|-------------|
| `groupBy()` | `df.groupBy("department")` | Группировка данных |
| `agg()` | `df.groupBy('genre').agg({"salary": "avg", "age": "max"})` | Агрегатные функции |
| `count()` | `df.groupBy('genre').count()` | Подсчет количества строк |
| `sum()` | `df.groupBy("dept").sum("salary")` | Сумма по группе |
| `avg()` | `df.groupBy("dept").avg("salary")` | Среднее значение |
| `min()/max()` | `df.groupBy("dept").max("age")` | Минимальное/максимальное значение |

