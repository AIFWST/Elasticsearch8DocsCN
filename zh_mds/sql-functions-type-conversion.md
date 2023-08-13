

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« String Functions](sql-functions-string.md) [Geo Functions »](sql-
functions-geo.md)

## 类型转换函数

用于将一种数据类型的表达式转换为另一种数据类型的函数。

###'演员表

**Synopsis:**

    
    
    CAST(
        expression __AS data_type) __

__

|

要投射的表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

要强制转换为的目标数据类型**说明**：将给定表达式的结果强制转换为目标数据类型。如果无法强制转换(例如，由于目标类型太窄或值本身无法转换)，则查询将失败。

    
    
    SELECT CAST('123' AS INT) AS int;
    
          int
    ---------------
    123
    
    
    SELECT CAST(123 AS VARCHAR) AS string;
    
        string
    ---------------
    123
    
    
    SELECT YEAR(CAST('2018-05-19T11:23:45Z' AS TIMESTAMP)) AS year;
    
         year
    ---------------
    2018

ANSI SQL和Elasticsearch SQL类型都支持前者优先。这只会影响"FLOAT"，由于命名冲突，它被解释为ANSI SQL，因此在Elasticsearch中映射到"double"作为反对的"float"。要获得 Elasticsearch 'float'，请执行转换为其 SQL等效的 'real' 类型。

###'转换'

**Synopsis:**

    
    
    CONVERT(
        expression, __data_type) __

__

|

要转换的表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

要转换为的目标数据类型**描述**：与"CAST"完全相同，但语法略有不同。此外，除了标准数据类型外，它还支持相应的 ODBC 数据类型。

    
    
    SELECT CONVERT('123', SQL_INTEGER) AS int;
    
          int
    ---------------
    123
    
    
    SELECT CONVERT('123', INTEGER) AS int;
    
          int
    ---------------
    123

[« String Functions](sql-functions-string.md) [Geo Functions »](sql-
functions-geo.md)
