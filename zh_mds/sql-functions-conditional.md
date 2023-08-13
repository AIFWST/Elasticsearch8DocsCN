

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Geo Functions](sql-functions-geo.md) [System Functions »](sql-functions-
system.md)

## 条件函数和表达式

通过以 if-else 方式求值来返回其参数之一的函数。

###'案例'

**Synopsis:**

    
    
    CASE WHEN condition THEN result
        [WHEN ...]
        [ELSE default_result]
    END

**输入**：

使用一个或多个_WHEN **条件** 然后 **result_** 子句，表达式可以选择具有_ELSE **default_result_** 子句。每个条件**都应该是一个布尔表达式。

输出**：如果相应的 _WHEN**condition_** 计算结果为 'true'，则为 ** 结果表达式之一;如果所有 _WHEN**condition_** 子句的计算结果均为 'false'，则为 **default_result**。如果缺少可选的 _ELSE**default_result_** 子句，并且所有 _WHEN **condition_** 子句的计算结果为 'false'，则返回 'null'。

**描述**：CASE表达式是一个通用条件表达式，它模拟其他编程语言的if/else语句 如果条件的结果为真，则条件后面的结果表达式的值将是后续返回的，当子句将被跳过并且不被处理时。

    
    
    SELECT CASE WHEN 1 > 2 THEN 'elastic'
                WHEN 2 <= 3 THEN 'search'
           END AS "case";
    
        case
    ---------------
    search
    
    
    SELECT CASE WHEN 1 > 2 THEN 'elastic'
                WHEN 2 > 10 THEN 'search'
           END AS "case";
    
        case
    ---------------
    null
    
    
    SELECT CASE WHEN 1 > 2 THEN 'elastic'
                WHEN 2 > 10 THEN 'search'
                ELSE 'default'
           END AS "case";
    
        case
    ---------------
    default

作为一种变体，case 表达式可以用类似于其他编程语言的 switch-case** 的语法来表示：

    
    
    CASE expression
         WHEN value1 THEN result1
        [WHEN value2 THEN result2]
        [WHEN ...]
        [ELSE default_result]
    END

在这种情况下，它在内部转换为：

    
    
    CASE WHEN expression = value1 THEN result1
        [WHEN expression = value2 THEN result2]
        [WHEN ...]
        [ELSE default_result]
    END
    
    
    SELECT CASE 5
                WHEN 1 THEN 'elastic'
                WHEN 2 THEN 'search'
                WHEN 5 THEN 'elasticsearch'
           END AS "case";
    
        case
    ---------------
    elasticsearch
    
    
    SELECT CASE 5
                WHEN 1 THEN 'elastic'
                WHEN 2 THEN 'search'
                WHEN 3 THEN 'elasticsearch'
                ELSE 'default'
           END AS "case";
    
        case
    ---------------
    default

所有结果表达式都必须是兼容的数据类型。更具体地说，allresult 表达式应具有与第一个_non null_result表达式兼容的数据类型。例如：

对于以下查询：

    
    
    CASE WHEN a = 1 THEN null
         WHEN a > 2 THEN 10
         WHEN a > 5 THEN 'foo'
    END

将返回一条错误消息，指出 **_foo_** 的数据类型为 **关键字** ，这与预期的数据类型 **整数** 不匹配(基于结果 **10**)。

#### 条件分桶

CASE 可用作查询中的 GROUP BY 键，以方便自定义存储桶并为这些存储桶分配描述性名称。例如，如果键的值太多，或者简单地说，这些值的范围比每个值都更有趣，则 CASE 可以创建自定义存储桶，如以下示例所示：

    
    
    SELECT count(*) AS count,
      CASE WHEN NVL(languages, 0) = 0 THEN 'zero'
        WHEN languages = 1 THEN 'one'
        WHEN languages = 2 THEN 'bilingual'
        WHEN languages = 3 THEN 'trilingual'
        ELSE 'multilingual'
      END as lang_skills
    FROM employees
    GROUP BY lang_skills
    ORDER BY lang_skills;

使用此查询，可以使用描述性名称为值 _0、1、2，3_ 创建正常的分组存储桶，并且每个值 _> = 4_ 都落入the_multilingual_存储桶中。

###'合并'

**Synopsis:**

    
    
    COALESCE(
        expression, __expression, __...)

**输入**：

__

|

第一个表达式 ---|--- __

|

第二个表达式...

**N** 第

COALESCE 可以接受任意数量的参数。

**输出**：表达式之一或"空"

**说明**：返回其第一个非 null 参数。如果所有参数都为空，则返回"null"。

    
    
    SELECT COALESCE(null, 'elastic', 'search') AS "coalesce";
    
        coalesce
    ---------------
    elastic
    
    
    SELECT COALESCE(null, null, null, null) AS "coalesce";
    
        coalesce
    ---------------
    null

###"最伟大"

**Synopsis:**

    
    
    GREATEST(
        expression, __expression, __...)

**输入**：

__

|

第一个表达式 ---|--- __

|

第二个表达式...

**N** 第

GREATEST 可以接受任意数量的参数，并且所有参数都必须具有相同的数据类型。

**输出**：表达式之一或"空"

**说明**：返回具有最大值(非空)的参数。如果所有参数均为 null，则返回 'null'。

    
    
    SELECT GREATEST(null, 1, 2) AS "greatest";
    
        greatest
    ---------------
    2
    
    
    SELECT GREATEST(null, null, null, null) AS "greatest";
    
        greatest
    ---------------
    null

###'IFNULL'

**Synopsis:**

    
    
    IFNULL(
        expression, __expression) __

**输入**：

__

|

第一个表达式 ---|--- __

|

第二个表达式 **输出** ：如果第一个表达式为 null，则为第二个表达式，否则第一个表达式。

**描述**：只有两个参数的"COALESCE"变体。返回其第一个不为 null 的参数。如果所有参数均为 null，则返回 'null'。

    
    
    SELECT IFNULL('elastic', null) AS "ifnull";
    
        ifnull
    ---------------
    elastic
    
    
    SELECT IFNULL(null, 'search') AS "ifnull";
    
        ifnull
    ---------------
    search

###'IIF'

**Synopsis:**

    
    
    IIF(
        expression,   __expression, __[expression]) __

**输入**：

__

|

用于检查 ---|--- __ 的布尔条件

|

如果布尔条件的计算结果为"true"，则返回值 __

|

如果布尔条件计算为"false"，则返回值;可选 **输出** ：如果第一个表达式(条件)的计算结果为 'true'，则为第二个表达式。如果它的计算结果为"false"，则返回第三个表达式。如果未提供第 3 个表达式，则返回"null"。

**描述**：实现编程语言<condition> <result1> 的标准_IF THEN ELSE <result2>_逻辑的条件函数。如果未提供第三个表达式，并且条件的计算结果为"false"，则返回"null"。

    
    
    SELECT IIF(1 < 2, 'TRUE', 'FALSE') AS result1, IIF(1 > 2, 'TRUE', 'FALSE') AS result2;
    
        result1    |    result2
    ---------------+---------------
    TRUE           |FALSE
    
    
    SELECT IIF(1 < 2, 'TRUE') AS result1, IIF(1 > 2 , 'TRUE') AS result2;
    
        result1    |    result2
    ---------------+---------------
    TRUE           |null

可以组合 IIF** 函数来实现更复杂的逻辑来模拟"CASE"表达式。例如：

    
    
    IIF(a = 1, 'one', IIF(a = 2, 'two', IIF(a = 3, 'three', 'many')))

###'ISNULL'

**Synopsis:**

    
    
    ISNULL(
        expression, __expression) __

**输入**：

__

|

第一个表达式 ---|--- __

|

第二个表达式 **输出** ：如果第一个表达式为 null，则为第二个表达式，否则第一个表达式。

**描述**：只有两个参数的"COALESCE"变体。返回其第一个不为 null 的参数。如果所有参数均为 null，则返回 'null'。

    
    
    SELECT ISNULL('elastic', null) AS "isnull";
    
        isnull
    ---------------
    elastic
    
    
    SELECT ISNULL(null, 'search') AS "isnull";
    
        isnull
    ---------------
    search

###'最少'

**Synopsis:**

    
    
    LEAST(
        expression, __expression, __...)

**输入**：

__

|

第一个表达式 ---|--- __

|

第二个表达式...

**N** 第

MINIMUM 可以接受任意数量的参数，并且所有参数都必须具有相同的数据类型。

**输出**：表达式之一或"空"

**说明**：返回具有最小值(不为 null)的参数。如果所有参数均为 null，则返回 'null'。

    
    
    SELECT LEAST(null, 2, 1) AS "least";
    
        least
    ---------------
    1
    
    
    SELECT LEAST(null, null, null, null) AS "least";
    
        least
    ---------------
    null

###'空'

**Synopsis:**

    
    
    NULLIF(
        expression, __expression) __

**输入**：

__

|

第一个表达式 ---|--- __

|

第二个表达式 **输出** ： 如果 2 个表达式相等，则为 'null'，否则是第一个表达式。

**说明**：当两个输入表达式相等时返回"null"，如果相等，则返回第一个表达式。

    
    
    SELECT NULLIF('elastic', 'search') AS "nullif";
        nullif
    ---------------
    elastic
    
    
    SELECT NULLIF('elastic', 'elastic') AS "nullif";
    
        nullif:s
    ---------------
    null

###'NVL'

**Synopsis:**

    
    
    NVL(
        expression, __expression) __

**输入**：

__

|

第一个表达式 ---|--- __

|

第二个表达式 **输出** ：如果第一个表达式为 null，则为第二个表达式，否则第一个表达式。

**描述**：只有两个参数的"COALESCE"变体。返回其第一个不为 null 的参数。如果所有参数均为 null，则返回 'null'。

    
    
    SELECT NVL('elastic', null) AS "nvl";
    
        nvl
    ---------------
    elastic
    
    
    SELECT NVL(null, 'search') AS "nvl";
    
        nvl
    ---------------
    search

[« Geo Functions](sql-functions-geo.md) [System Functions »](sql-functions-
system.md)
