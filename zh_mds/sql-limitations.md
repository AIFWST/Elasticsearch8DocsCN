

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« Reserved keywords](sql-syntax-reserved.md) [Scripting »](modules-
scripting.md)

## SQLLimitations

### 大型查询可能会引发"解析异常"

超大查询在解析阶段会消耗过多内存，在这种情况下，Elasticsearch SQL 引擎会中止解析并抛出错误。在这种情况下，请考虑通过可能简化查询或将其拆分为较小的查询来将查询减小到较小的大小。

### "系统列"和"可描述"中的嵌套字段

Elasticsearch有一种特殊类型的关系字段，称为"嵌套"字段。在Elasticsearch SQL中，可以通过引用其内部子字段来使用它们。即使非驱动程序模式下的"SYS 列"(在 CLI 和 REST 调用中)和"描述表"仍将它们显示为具有"嵌套"类型，但它们不能在查询中使用。只能以以下形式引用其子字段：

    
    
    [nested_field_name].[sub_field_name]

例如：

    
    
    SELECT dep.dep_name.keyword FROM test_emp GROUP BY languages;

### 嵌套字段上的标量函数不允许在"WHERE"和"ORDERBY"子句中使用

Elasticsearch SQL 不支持在 'WHERE' 和 'ORDER BY' 子句中的嵌套字段之上使用标量函数，但比较运算符和逻辑运算符除外。

例如：

    
    
    SELECT * FROM test_emp WHERE LENGTH(dep.dep_name.keyword) > 5;

and

    
    
    SELECT * FROM test_emp ORDER BY YEAR(dep.start_date);

不受支持，但：

    
    
    SELECT * FROM test_emp WHERE dep.start_date >= CAST('2020-01-01' AS DATE) OR dep.dep_end_date IS NULL;

受支持。

### 多嵌套字段

Elasticsearch SQL 不支持多嵌套文档，因此查询不能引用索引中的多个嵌套字段。这适用于多级嵌套字段，也适用于在同一级别上定义的多个嵌套字段。例如，对于此索引：

    
    
           column         |     type      |    mapping
    ----------------------+---------------+-------------
    nested_A              |STRUCT         |NESTED
    nested_A.nested_X     |STRUCT         |NESTED
    nested_A.nested_X.text|VARCHAR        |KEYWORD
    nested_A.text         |VARCHAR        |KEYWORD
    nested_B              |STRUCT         |NESTED
    nested_B.text         |VARCHAR        |KEYWORD

"nested_A"和"nested_B"不能同时使用，也不能同时使用"nested_A/nested_B"和"nested_A.nested_X"组合。对于这种情况，Elasticsearch SQL将显示一条错误消息。

### 分页嵌套内部点击

当 SELECT 嵌套字段时，分页将无法按预期工作，Elasticsearch SQL 将返回_at least_页面大小记录。这是因为嵌套查询在 Elasticsearch 中的工作方式：将返回根嵌套字段，并且它也匹配内部嵌套字段，分页发生在根嵌套文档上，而不是在其内部命中**上进行。

### 规范化的"关键字"字段

Elasticsearch 中的"关键字"字段可以通过定义"规范化器"来规范化。Elasticsearch SQL 不支持此类字段。

### 字段的数组类型

由于 Elasticsearch 处理值数组的"不可见"方式，不支持数组字段：映射不会指示字段是否是数组(具有多个值)，因此如果不读取所有数据，Elasticsearch SQL 无法知道字段是单值还是多值。当一个字段返回多个值时，默认情况下，Elasticsearch SQL会抛出异常。但是，可以通过 REST 中的"field_multi_value_leniency"参数(默认禁用)或驱动程序中的"field.multi.value.leniency"(默认启用)更改此行为。

### 按聚合排序

在进行聚合("GROUP BY")时，Elasticsearch SQL依赖于Elasticsearch的"复合"聚合来支持分页结果。但是，这种类型的聚合确实存在限制：排序只能应用于用于聚合存储桶的键。Elasticsearch SQL 通过执行客户端排序克服了这一限制，但作为一种安全措施，最多只允许 **65535** 行。

建议对使用聚合排序的查询使用"LIMIT"，本质上指示所需的前 N 个结果：

    
    
    SELECT * FROM test GROUP BY age ORDER BY COUNT(*) LIMIT 100;

可以在没有"LIMIT"的情况下运行相同的查询，但是在这种情况下，如果传递了最大大小(**10000**)，将返回异常，因为Elasticsearch SQL无法跟踪(和排序)返回的所有结果。

此外，"ORDER BY"中使用的聚合必须只是普通聚合函数。不能使用标量函数或运算符，因此不能使用组合两个或更多聚合函数的复杂列进行排序。下面是一些不允许的查询示例：

    
    
    SELECT age, ROUND(AVG(salary)) AS avg FROM test GROUP BY age ORDER BY avg;
    
    SELECT age, MAX(salary) - MIN(salary) AS diff FROM test GROUP BY age ORDER BY diff;

### 使用子选择

使用子选择("从(选择 Y)中选择 X")在很小程度上得到支持：任何可以"扁平化"为单个"选择"的子选择都可以使用 Elasticsearch SQL。例如：

    
    
    SELECT * FROM (SELECT first_name, last_name FROM emp WHERE last_name NOT LIKE '%a%') WHERE first_name LIKE 'A%' ORDER BY 1;
    
      first_name   |   last_name
    ---------------+---------------
     Alejandro     |McAlpine
     Anneke        |Preusig
     Anoosh        |Peyn
     Arumugam      |Ossenbruggen

上面的查询是可能的，因为它等效于：

    
    
    SELECT first_name, last_name FROM emp WHERE last_name NOT LIKE '%a%' AND first_name LIKE 'A%' ORDER BY 1;

但是，如果子选择将包括"分组依据"或"具有"，或者封闭的"选择"将比"从中选择X(选择...WHERE[simple_condition]"，这目前不受支持。

### 在 'HAVING' 子句中使用 'FIRST'/'LAST' 聚合函数

不支持在"HAVING"子句中使用"FIRST"和"LAST"。这同样适用于"MIN"和"MAX"，当它们的目标列类型为"关键字"或"unsigned_long"时，因为它们在内部翻译为"FIRST"和"LAST"。

### 在 GROUP BY 或"直方图"中使用 TIME 数据类型

目前不支持使用"TIME"数据类型作为分组键。例如：

    
    
    SELECT count(*) FROM test GROUP BY CAST(date_created AS TIME);

另一方面，如果它包装有返回另一种数据类型的标量函数，它仍然可以使用，例如：

    
    
    SELECT count(*) FROM test GROUP BY MINUTE((CAST(date_created AS TIME));

直方图分组函数目前也不支持"TIME"数据类型。例如：

    
    
    SELECT HISTOGRAM(CAST(birth_date AS TIME), INTERVAL '10' MINUTES) as h, COUNT(*) FROM t GROUP BY h

### 地理相关函数

由于"geo_shape"字段没有文档值，因此这些字段不能用于过滤、分组或排序。

默认情况下，"geo_points"字段已编入索引并具有文档值。但是，仅存储和索引纬度和经度时，原始值的精度有所下降(纬度为 4.190951585769653E-8，经度为 8.381903171539307E-8)。高度分量被接受，但不存储在文档值中，也不编制索引。因此，在过滤、分组或排序中调用"ST_Z"函数将返回"null"。

### 使用"字段"搜索参数检索

Elasticsearch SQL使用搜索API的"fields"参数检索列值。对"fields"参数的任何限制也适用于Elasticsearch SQL查询。例如，如果对任何返回的字段或索引级别禁用了"_source"，则无法检索这些值。

### "PIVOT"子句中的聚合

"PIVOT"中的聚合表达式当前仅接受一个聚合。因此，不可能为任何一个透视列获取多个聚合。

### 在"PIVOT"s'IN'-子句中使用子查询

"PIVOT"查询可以透视的值必须在查询中作为文本列表提供;当前不支持提供子查询来生成此列表。例如，在此查询中：

    
    
    SELECT * FROM test_emp PIVOT (SUM(salary) FOR languages IN (1, 2))

感兴趣的"语言"必须明确列出："IN (1， 2)"。另一方面，此示例将**不起作用**：

    
    
    SELECT * FROM test_emp PIVOT (SUM(salary) FOR languages IN (SELECT languages FROM test_emp WHERE languages <=2 GROUP BY languages))

[« Reserved keywords](sql-syntax-reserved.md) [Scripting »](modules-
scripting.md)
