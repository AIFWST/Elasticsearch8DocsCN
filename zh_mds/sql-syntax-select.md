

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« DESCRIBE TABLE](sql-syntax-describe-table.md) [SHOW CATALOGS »](sql-
syntax-show-catalogs.md)

##SELECT

**Synopsis:**

    
    
    SELECT [TOP [ count ] ] select_expr [, ...]
    [ FROM table_name ]
    [ WHERE condition ]
    [ GROUP BY grouping_element [, ...] ]
    [ HAVING condition]
    [ ORDER BY expression [ ASC | DESC ] [, ...] ]
    [ LIMIT [ count ] ]
    [ PIVOT ( aggregation_expr FOR column IN ( value [ [ AS ] alias ] [, ...] ) ) ]

**说明**：从零个或多个表中检索行。

"SELECT"的一般执行如下：

1. 计算"FROM"列表中的所有元素(每个元素可以是基表或别名表)。目前"FROM"仅支持一个表。但请注意，表名可以是一种模式(请参阅下面的 FROM 子句)。  2. 如果指定了"WHERE"子句，则从输出中删除所有不满足条件的行。(请参阅下面的 WHERE 条款。  3. 如果指定了"GROUP BY"子句，或者存在聚合函数调用，则输出将组合成与一个或多个值匹配的行组，并计算聚合函数的结果。如果存在"HAVING"子句，则会消除不满足给定条件的组。(请参阅下面的分组依据条款和 HAVING 条款。  4. 实际输出行是使用每个选定行或行组的"SELECT"输出表达式计算的。  5. 如果指定了"ORDER BY"子句，则返回的行将按指定的顺序排序。如果未给出"ORDER BY"，则按系统认为最快的任何顺序返回行。(请参阅下面的排序依据条款。  6. 如果指定了"LIMIT"或"TOP"(不能在同一查询中使用两者)，则"SELECT"语句仅返回结果行的子集。(请参阅下面的限制条款和 TOP 条款。

### '选择'列表

"SELECT"列表，即"SELECT"和"FROM"之间的表达式，表示"SELECT"语句的输出行。

与表一样，"SELECT"的每个输出列都有一个名称，可以通过"AS"关键字按列指定：

    
    
    SELECT 1 + 1 AS result;
    
        result
    ---------------
    2

注意："AS"是一个可选关键字，但它有助于查询的可读性和在某些情况下的歧义，这就是为什么建议指定它的原因。

由 Elasticsearch SQL 分配，如果未给出名称：

    
    
    SELECT 1 + 1;
    
        1 + 1
    --------------
    2

或者，如果是简单的列引用，请使用其名称作为列名称：

    
    
    SELECT emp_no FROM emp LIMIT 1;
    
        emp_no
    ---------------
    10001

###Wildcard

要选择源中的所有列，可以使用"*"：

    
    
    SELECT * FROM emp LIMIT 1;
    
         birth_date     |    emp_no     |  first_name   |    gender     |       hire_date        |   languages   |   last_name   |     name      |    salary
    --------------------+---------------+---------------+---------------+------------------------+---------------+---------------+---------------+---------------
    1953-09-02T00:00:00Z|10001          |Georgi         |M              |1986-06-26T00:00:00.000Z|2              |Facello        |Georgi Facello |57305

它基本上返回找到的all(顶级字段，子字段，例如多字段被忽略)列。

###TOP

"TOP"子句可以在"SELECT"列表或<<sql-syntax-select-wildcard，"通配符"之前使用>来限制(限制)返回的行数，使用以下格式：

    
    
    SELECT TOP <count> <select list> ...

where

count

     is a positive integer or zero indicating the maximum **possible** number of results being returned (as there might be fewer matches than the limit). If `0` is specified, no results are returned. 
    
    
    SELECT TOP 2 first_name, last_name, emp_no FROM emp;
    
      first_name   |   last_name   |    emp_no
    ---------------+---------------+---------------
    Georgi         |Facello        |10001
    Bezalel        |Simmel         |10002

"TOP"和"LIMIT"不能在同一查询中一起使用，否则将返回错误。

### 来自克劳斯

"FROM"子句为"SELECT"指定一个表，并具有以下语法：

    
    
    FROM table_name [ [ AS ] alias ]

where:

`table_name`

     Represents the name (optionally qualified) of an existing table, either a concrete or base one (actual index) or alias. 

如果表名包含特殊的 SQL 字符(如"."、"-"、"*"等)使用双引号对它们进行转义：

    
    
    SELECT * FROM "emp" LIMIT 1;
    
         birth_date     |    emp_no     |  first_name   |    gender     |       hire_date        |   languages   |   last_name   |     name      |    salary
    --------------------+---------------+---------------+---------------+------------------------+---------------+---------------+---------------+---------------
    1953-09-02T00:00:00Z|10001          |Georgi         |M              |1986-06-26T00:00:00.000Z|2              |Facello        |Georgi Facello |57305

该名称可以是指向多个索引的模式(可能需要如上所述引用)，但限制**所有**解析的具体表具有**精确映射**。

    
    
    SELECT emp_no FROM "e*p" LIMIT 1;
    
        emp_no
    ---------------
    10001

preview] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 要运行 [跨集群搜索，请使用 '：" 语法指定集群名称<remote_cluster><target>，其中 '' <remote_cluster>映射到 SQLcatalog(集群)，而 '<target>' 映射到表(索引或数据流)。""<remote_cluster>支持通配符("*")，"<target>"可以是索引模式。

    
    
    SELECT emp_no FROM "my*cluster:*emp" LIMIT 1;
    
        emp_no
    ---------------
    10001

`alias`

     A substitute name for the `FROM` item containing the alias. An alias is used for brevity or to eliminate ambiguity. When an alias is provided, it completely hides the actual name of the table and must be used in its place. 
    
    
    SELECT e.emp_no FROM emp AS e LIMIT 1;
    
        emp_no
    -------------
    10001

### 哪里克劳斯

可选的"WHERE"子句用于筛选查询中的行，并具有以下语法：

    
    
    WHERE condition

where:

`condition`

     Represents an expression that evaluates to a `boolean`. Only the rows that match the condition (to `true`) are returned. 
    
    
    SELECT last_name FROM emp WHERE emp_no = 10001;
    
       last_name
    ---------------
    Facello

### 分组

"GROUP BY"子句用于将结果划分为与指定列匹配值的行组。它具有以下语法：

    
    
    GROUP BY grouping_element [, ...]

where:

`grouping_element`

     Represents an expression on which rows are being grouped _on_. It can be a column name, alias or ordinal number of a column or an arbitrary expression of column values. 

按列名称分组的常见名称：

    
    
    SELECT gender AS g FROM emp GROUP BY gender;
    
           g
    ---------------
    null
    F
    M

按输出序号分组：

    
    
    SELECT gender FROM emp GROUP BY 1;
    
        gender
    ---------------
    null
    F
    M

按别名分组：

    
    
    SELECT gender AS g FROM emp GROUP BY g;
    
           g
    ---------------
    null
    F
    M

并按列表达式分组(通常与别名一起使用)：

    
    
    SELECT languages + 1 AS l FROM emp GROUP BY l;
    
           l
    ---------------
    null
    2
    3
    4
    5
    6

或上述的混合物：

    
    
    SELECT gender g, languages l, COUNT(*) c FROM "emp" GROUP BY g, l ORDER BY languages ASC, gender DESC;
    
           g       |       l       |       c
    ---------------+---------------+---------------
    M              |null           |7
    F              |null           |3
    M              |1              |9
    F              |1              |4
    null           |1              |2
    M              |2              |11
    F              |2              |5
    null           |2              |3
    M              |3              |11
    F              |3              |6
    M              |4              |11
    F              |4              |6
    null           |4              |1
    M              |5              |8
    F              |5              |9
    null           |5              |4

当在"SELECT"中使用"GROUP BY"子句时，_all_ 输出表达式必须是用于分组或派生的聚合函数或表达式(否则，每个未分组的列将有多个可能的值要返回)。

即：

    
    
    SELECT gender AS g, COUNT(*) AS c FROM emp GROUP BY gender;
    
           g       |       c
    ---------------+---------------
    null           |10
    F              |33
    M              |57

输出中使用的聚合表达式：

    
    
    SELECT gender AS g, ROUND((MIN(salary) / 100)) AS salary FROM emp GROUP BY gender;
    
           g       |    salary
    ---------------+---------------
    null           |253
    F              |259
    M              |259

使用了多个聚合：

    
    
    SELECT gender AS g, KURTOSIS(salary) AS k, SKEWNESS(salary) AS s FROM emp GROUP BY gender;
    
           g       |        k         |         s
    ---------------+------------------+-------------------
    null           |2.2215791166941923|-0.03373126000214023
    F              |1.7873117044424276|0.05504995122217512
    M              |2.280646181070106 |0.44302407229580243

如果需要自定义存储桶，可以使用"CASE"来实现，如下所示。

#### 隐式分组

当在没有关联的"GROUP BY"的情况下使用聚合时，将应用 _implicitgrouping_，这意味着所有选定的行都被视为形成单个默认或隐式组。因此，查询仅发出一行(因为只有一个组)。

一个常见的例子是计算记录数：

    
    
    SELECT COUNT(*) AS count FROM emp;
    
         count
    ---------------
    100

当然，可以应用多个聚合：

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, AVG(salary) AS avg, COUNT(*) AS count FROM emp;
    
          min:i    |      max:i    |      avg:d    |     count:l
    ---------------+---------------+---------------+---------------
    25324          |74999          |48248.55       |100

###HAVING

"HAVING"子句可以_仅_与聚合函数一起使用(因此"GROUP BY")来过滤保留或不保留的组，并具有以下语法：

    
    
    HAVING condition

where:

`condition`

     Represents an expression that evaluates to a `boolean`. Only groups that match the condition (to `true`) are returned. 

"WHERE"和"HAVING"都用于过滤，但它们之间有几个显着差异：

1. "WHERE"适用于单个**行**，"HAVING"适用于由"GROUP BY"创建的**组** 2."WHERE"在分组之前评估，"HAVING"在分组之后评估

    
    
    SELECT languages AS l, COUNT(*) AS c FROM emp GROUP BY l HAVING c BETWEEN 15 AND 20;
    
           l       |       c
    ---------------+---------------
    1              |15
    2              |19
    3              |17
    4              |18

此外，可以在"HAVING"中使用输出中未使用的偶数("SELECT")中的多个聚合表达式：

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, MAX(salary) - MIN(salary) AS diff FROM emp GROUP BY languages HAVING diff - max % min > 0 AND AVG(salary) > 30000;
    
          min      |      max      |     diff
    ---------------+---------------+---------------
    28336          |74999          |46663
    25976          |73717          |47741
    29175          |73578          |44403
    26436          |74970          |48534
    27215          |74572          |47357
    25324          |66817          |41493

#### 隐式分组

如上所述，可以有一个没有"GROUPBY"的"HAVING"子句。在这种情况下，应用所谓的_implicit grouping_，这意味着所有选定的行都被视为形成一个组，并且"HAVING"可以应用于该组上指定的任何聚合函数。因此，查询仅发出一行(因为只有一个组)，并且"HAVING"条件返回一行(组)或零(如果条件失败)。

在此示例中，"HAVING"匹配：

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max FROM emp HAVING min > 25000;
    
          min      |      max
    ---------------+---------------
    25324          |74999

### 排序方式

"ORDER BY"子句用于按一个或多个表达式对"SELECT"的结果进行排序：

    
    
    ORDER BY expression [ ASC | DESC ] [, ...]

where:

`expression`

     Represents an input column, an output column or an ordinal number of the position (starting from one) of an output column. Additionally, ordering can be done based on the results _score_. The direction, if not specified, is by default `ASC` (ascending). Regardless of the ordering specified, null values are ordered last (at the end). 

当一起使用时，"GROUP BY"表达式可以指向_only_用于分组或聚合函数的列。

例如，以下查询按任意输入字段 ('page_count) 排序：

    
    
    SELECT * FROM library ORDER BY page_count DESC LIMIT 5;
    
         author      |        name        |  page_count   |    release_date
    -----------------+--------------------+---------------+--------------------
    Peter F. Hamilton|Pandora's Star      |768            |2004-03-02T00:00:00Z
    Vernor Vinge     |A Fire Upon the Deep|613            |1992-06-01T00:00:00Z
    Frank Herbert    |Dune                |604            |1965-06-01T00:00:00Z
    Alastair Reynolds|Revelation Space    |585            |2000-03-15T00:00:00Z
    James S.A. Corey |Leviathan Wakes     |561            |2011-06-02T00:00:00Z

### 排序依据和分组

对于执行分组的查询，可以对分组列(默认情况下升序)或聚合函数应用排序。

使用"GROUP BY"，确保排序以结果组为目标 - 将其应用于组内的各个元素不会影响结果，因为无论顺序如何，组内的值都会聚合。

例如，要对组进行排序，只需指示分组键：

    
    
    SELECT gender AS g, COUNT(*) AS c FROM emp GROUP BY gender ORDER BY g DESC;
    
           g       |       c
    ---------------+---------------
    M              |57
    F              |33
    null           |10

当然，可以指定多个键：

    
    
    SELECT gender g, languages l, COUNT(*) c FROM "emp" GROUP BY g, l ORDER BY languages ASC, gender DESC;
    
           g       |       l       |       c
    ---------------+---------------+---------------
    M              |null           |7
    F              |null           |3
    M              |1              |9
    F              |1              |4
    null           |1              |2
    M              |2              |11
    F              |2              |5
    null           |2              |3
    M              |3              |11
    F              |3              |6
    M              |4              |11
    F              |4              |6
    null           |4              |1
    M              |5              |8
    F              |5              |9
    null           |5              |4

此外，还可以根据其值的聚合对组进行排序：

    
    
    SELECT gender AS g, MIN(salary) AS salary FROM emp GROUP BY gender ORDER BY salary DESC;
    
           g       |    salary
    ---------------+---------------
    F              |25976
    M              |25945
    null           |25324

出于内存消耗原因，最多可以对 **10000** 个条目进行聚合排序。如果结果超过此阈值，请使用"LIMIT"或"TOP"来减少结果数。

### 按分数排序

在"WHERE"子句中执行全文查询时，可以根据结果的评分或与给定查询的相关性返回结果。

当在"WHERE"子句中执行多个文本查询时，它们的分数将使用与Elasticsearch的布尔查询相同的规则进行组合。

要根据"分数"进行排序，请使用特殊函数"SCORE()"：

    
    
    SELECT SCORE(), * FROM library WHERE MATCH(name, 'dune') ORDER BY SCORE() DESC;
    
        SCORE()    |    author     |       name        |  page_count   |    release_date
    ---------------+---------------+-------------------+---------------+--------------------
    2.2886353      |Frank Herbert  |Dune               |604            |1965-06-01T00:00:00Z
    1.8893257      |Frank Herbert  |Dune Messiah       |331            |1969-10-15T00:00:00Z
    1.6086556      |Frank Herbert  |Children of Dune   |408            |1976-04-21T00:00:00Z
    1.4005898      |Frank Herbert  |God Emperor of Dune|454            |1981-05-28T00:00:00Z

请注意，您可以通过在"WHERE"子句中使用全文搜索谓词来返回"SCORE()"。即使"SCORE()"不用于排序，这也是可能的：

    
    
    SELECT SCORE(), * FROM library WHERE MATCH(name, 'dune') ORDER BY page_count DESC;
    
        SCORE()    |    author     |       name        |  page_count   |    release_date
    ---------------+---------------+-------------------+---------------+--------------------
    2.2886353      |Frank Herbert  |Dune               |604            |1965-06-01T00:00:00Z
    1.4005898      |Frank Herbert  |God Emperor of Dune|454            |1981-05-28T00:00:00Z
    1.6086556      |Frank Herbert  |Children of Dune   |408            |1976-04-21T00:00:00Z
    1.8893257      |Frank Herbert  |Dune Messiah       |331            |1969-10-15T00:00:00Z

注意：尝试从非全文查询返回"score"将为所有结果返回相同的值，因为所有结果都同样相关。

###LIMIT

"LIMIT"子句使用以下格式限制(限制)返回的行数：

    
    
    LIMIT ( <count> | ALL )

where

count

     is a positive integer or zero indicating the maximum **possible** number of results being returned (as there might be fewer matches than the limit). If `0` is specified, no results are returned. 
ALL

     indicates there is no limit and thus all results are being returned. 
    
    
    SELECT first_name, last_name, emp_no FROM emp LIMIT 1;
    
      first_name   |   last_name   |    emp_no
    ---------------+---------------+---------------
    Georgi         |Facello        |10001

"TOP"和"LIMIT"不能在同一查询中一起使用，否则将返回错误。

###PIVOT

"PIVOT"子句对查询结果执行交叉制表：斜体聚合结果并将行旋转为列。旋转是通过将表达式中的一列(透视列)中的唯一值转换为输出中的多列来完成的。列值是表达式中指定的其余列的聚合。

该子句可以分为三个部分：聚合、"FOR"和"IN"子句。

"aggregation_expr"子句指定一个表达式，其中包含要应用于其中一个源列的聚合函数。目前只能提供一个聚合。

"FOR"子句指定透视列：此列的不同值将成为要旋转的候选值集。

"IN"子句定义了一个过滤器：此处提供的集合与"FOR"子句中的候选集合之间的交集将被旋转，成为附加到最终结果的列的标题。过滤器不能是子查询，这里必须提供文字值，提前获得。

透视操作将对"PIVOT"子句中未指定的所有源列以及通过"IN"子句过滤的值执行隐式 GROUP BY。请考虑以下语句：

    
    
    SELECT * FROM test_emp PIVOT (SUM(salary) FOR languages IN (1, 2)) LIMIT 5;
    
           birth_date    |    emp_no     |  first_name   |    gender     |     hire_date       |   last_name   |       name       |       1       |       2
    ---------------------+---------------+---------------+---------------+---------------------+---------------+------------------+---------------+---------------
    null                 |10041          |Uri            |F              |1989-11-12 00:00:00.0|Lenart         |Uri Lenart        |56415          |null
    null                 |10043          |Yishay         |M              |1990-10-20 00:00:00.0|Tzvieli        |Yishay Tzvieli    |34341          |null
    null                 |10044          |Mingsen        |F              |1994-05-21 00:00:00.0|Casley         |Mingsen Casley    |39728          |null
    1952-04-19 00:00:00.0|10009          |Sumant         |F              |1985-02-18 00:00:00.0|Peac           |Sumant Peac       |66174          |null
    1953-01-07 00:00:00.0|10067          |Claudi         |M              |1987-03-04 00:00:00.0|Stavenow       |Claudi Stavenow   |null           |52044

从逻辑上讲，查询执行可以分解为以下步骤：

1. 在"FOR"子句中的一栏上按分组："语言";  2. 通过"IN"子句中提供的集合过滤结果值;  3. 现在过滤的列被透视以形成附加到结果的两个附加列的标题："1"和"2";  4. 源表"test_emp"的所有列上的 GROUP BY，除了"薪水"(聚合子句的一部分)和"语言"("FOR"子句的一部分);  5. 这些附加列中的值是"工资"的"SUM"聚合，按相应的语言分组。

要交叉制表的表值表达式也可以是子查询的结果：

    
    
    SELECT * FROM (SELECT languages, gender, salary FROM test_emp) PIVOT (AVG(salary) FOR gender IN ('F'));
    
       languages   |       'F'
    ---------------+------------------
    null           |62140.666666666664
    1              |47073.25
    2              |50684.4
    3              |53660.0
    4              |49291.5
    5              |46705.555555555555

透视列可以别名(并且需要引号以容纳空格)，无论是否支持"AS"标记：

    
    
    SELECT * FROM (SELECT languages, gender, salary FROM test_emp) PIVOT (AVG(salary) FOR gender IN ('M' AS "XY", 'F' "XX"));
    
       languages   |        XY       |        XX
    ---------------+-----------------+------------------
    null           |48396.28571428572|62140.666666666664
    1              |49767.22222222222|47073.25
    2              |44103.90909090909|50684.4
    3              |51741.90909090909|53660.0
    4              |47058.90909090909|49291.5
    5              |39052.875        |46705.555555555555

生成的交叉制表可以进一步应用 ORDER BY 和 LIMIT 子句：

    
    
    SELECT * FROM (SELECT languages, gender, salary FROM test_emp) PIVOT (AVG(salary) FOR gender IN ('F')) ORDER BY languages DESC LIMIT 4;
       languages   |       'F'
    ---------------+------------------
    5              |46705.555555555555
    4              |49291.5
    3              |53660.0
    2              |50684.4

[« DESCRIBE TABLE](sql-syntax-describe-table.md) [SHOW CATALOGS »](sql-
syntax-show-catalogs.md)
