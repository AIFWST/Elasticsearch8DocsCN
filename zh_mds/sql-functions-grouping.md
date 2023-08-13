

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Aggregate Functions](sql-functions-aggs.md) [Date/Time and Interval
Functions and Operators »](sql-functions-datetime.md)

## 分组函数

用于创建特殊 _grouping_ s 的函数(也称为 _bucketing_ );因此，这些需要用作分组的一部分。

###'直方图'

**Synopsis:**

    
    
    HISTOGRAM(
        numeric_exp,        __numeric_interval) __HISTOGRAM(
        date_exp, __date_time_interval) __

**输入**：

__

|

数值表达式(通常为字段)。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|---    __

|

数字间隔。如果为"null"，则函数返回"null"。   __

|

日期/时间表达式(通常为字段)。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   __

|

日期/时间间隔。如果为"null"，则函数返回"null"。   输出**：给定表达式的非空桶或组根据给定间隔划分

**描述**：直方图函数获取所有匹配值，并将它们划分为与给定间隔匹配的固定大小的存储桶，使用以下公式：

    
    
    bucket_key = Math.floor(value / interval) * interval

SQL 中的直方图不会像传统的直方图和日期直方图一样返回缺少间隔的空存储桶。这种行为在概念上不适合将所有缺失值视为"null"的 SQL;因此，直方图将所有缺失值放在"null"组中。

"直方图"可以应用于任一数值字段：

    
    
    SELECT HISTOGRAM(salary, 5000) AS h FROM emp GROUP BY h;
    
           h
    ---------------
    25000
    30000
    35000
    40000
    45000
    50000
    55000
    60000
    65000
    70000

或日期/时间字段：

    
    
    SELECT HISTOGRAM(birth_date, INTERVAL 1 YEAR) AS h, COUNT(*) AS c FROM emp GROUP BY h;
    
    
               h            |       c
    ------------------------+---------------
    null                    |10
    1952-01-01T00:00:00.000Z|8
    1953-01-01T00:00:00.000Z|11
    1954-01-01T00:00:00.000Z|8
    1955-01-01T00:00:00.000Z|4
    1956-01-01T00:00:00.000Z|5
    1957-01-01T00:00:00.000Z|4
    1958-01-01T00:00:00.000Z|7
    1959-01-01T00:00:00.000Z|9
    1960-01-01T00:00:00.000Z|8
    1961-01-01T00:00:00.000Z|8
    1962-01-01T00:00:00.000Z|6
    1963-01-01T00:00:00.000Z|7
    1964-01-01T00:00:00.000Z|4
    1965-01-01T00:00:00.000Z|1

直方图中的表达式也受支持，只要返回类型为数字：

    
    
    SELECT HISTOGRAM(salary % 100, 10) AS h, COUNT(*) AS c FROM emp GROUP BY h;
    
           h       |       c
    ---------------+---------------
    0              |10
    10             |15
    20             |10
    30             |14
    40             |9
    50             |9
    60             |8
    70             |13
    80             |3
    90             |9

请注意，直方图(以及一般的分组函数)允许自定义表达式，但不能在"GROUP BY"中应用任何函数。换句话说，以下语句是不允许的：

    
    
    SELECT MONTH(HISTOGRAM(birth_date), 2)) AS h, COUNT(*) as c FROM emp GROUP BY h ORDER BY h DESC;

因为它需要两个分组(一个用于直方图，另一个用于在直方图组之上应用函数)。

相反，可以重写查询以在其histogram_inside_上移动表达式：

    
    
    SELECT HISTOGRAM(MONTH(birth_date), 2) AS h, COUNT(*) as c FROM emp GROUP BY h ORDER BY h DESC;
    
           h       |       c
    ---------------+---------------
    12             |7
    10             |17
    8              |16
    6              |16
    4              |18
    2              |10
    0              |6
    null           |10

当 SQL 中的直方图应用于 **DATE** 类型而不是 **DATETIME** 时，指定的间隔将被截断为一天的倍数。例如：对于"直方图(CAST(birth_date 作为日期)，间隔"2 3：04"天到分钟)"实际使用的间隔将是"间隔"2"天"。如果指定的间隔小于 1 天，例如："直方图(CAST(birth_date 作为日期)，间隔 '20'HOUR)"，则使用的间隔将为"间隔 '1' 天"。

为日期/时间直方图指定的所有间隔都将在其"date_histogram"聚合定义中使用固定间隔，但使用日历间隔的"间隔'1'年"、"间隔'1'个月"和"间隔'1'天"除外。选择日历间隔是为了获得更直观的年、月和日分组结果。例如，在 YEAR 的情况下，日历间隔将一年的存储桶视为从该特定年份的 1 月 1 日开始的存储桶，而固定间隔的一年存储桶将一年视为毫秒数(例如，"31536000000ms"对应于 365 天、每天 24 小时、每小时 60 分钟等)。例如，在固定间隔的情况下，2019 年 2 月 5 日这一天属于从 2018 年 12 月 20 日开始的存储桶，Elasticsearch(以及隐式的 Elasticsearch SQL)将返回 2018 年，日期实际上是 2019 年。使用日历间隔，此行为更直观，2019 年 2 月 5 日这一天实际上属于 2019 年桶。

SQL 中的直方图不能应用于 **TIME** 类型。例如："直方图(birth_date作为时间)，间隔'10'分钟)"目前不受支持。

[« Aggregate Functions](sql-functions-aggs.md) [Date/Time and Interval
Functions and Operators »](sql-functions-datetime.md)
