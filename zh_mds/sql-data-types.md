

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« SHOW TABLES](sql-syntax-show-tables.md) [Index patterns »](sql-index-
patterns.md)

## 数据类型

**弹性搜索类型**

|

**Elasticsearch SQL 类型**

|

**SQL 类型**

|

**SQL 精度** ---|---|---|--- **核心类型** 'null'

|

`null`

|

NULL

|

0 '布尔值'

|

`boolean`

|

BOOLEAN

|

1 个"字节"

|

`byte`

|

TINYINT

|

3 "短"

|

`short`

|

SMALLINT

|

5 '整数'

|

`integer`

|

INTEGER

|

10 "长"

|

`long`

|

BIGINT

|

19 "unsigned_long"

|

' [预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 unsigned_long'

|

BIGINT

|

20 "双"

|

`double`

|

DOUBLE

|

15 "浮子"

|

`float`

|

REAL

|

7 "half_float"

|

`half_float`

|

FLOAT

|

3 "scaled_float"

|

`scaled_float`

|

DOUBLE

|

15 关键字类型系列

|

`keyword`

|

VARCHAR

|

32，766 "文本"

|

`text`

|

VARCHAR

|

2，147，483，647 "二进制"

|

`binary`

|

VARBINARY

|

2，147，483，647 "日期"

|

`datetime`

|

TIMESTAMP

|

29 "ip"

|

`ip`

|

VARCHAR

|

39 '版本'

|

`version`

|

VARCHAR

|

32，766 **复杂类型** "对象"

|

`object`

|

STRUCT

|

0 "嵌套"

|

`nested`

|

STRUCT

|

0 **不支持的类型** _types未提及above_

|

`unsupported`

|

OTHER

|

0 如上所述，大多数 Elasticsearch 数据类型都可以在 Elasticsearch SQL 中使用。正如人们所看到的，所有Elasticsearch数据类型都映射到Elasticsearch SQL中具有相同名称的数据类型，除了在Elasticsearch SQL中映射到**datetime**的数据类型。这是为了避免与 ANSI SQL 类型 **DATE**(仅限日期)和 **TIME**(仅限时间)混淆，Elasticsearch SQL 在查询中也支持它们(使用 'CAST'/'CONVERT')，但与 Elasticsearch 中的实际映射不对应(参见下面的"表")。

显然，并非所有Elasticsearch中的类型在SQL中都有等价物，反之亦然，因此，Elasticsearch SQL使用前者的数据类型_特殊性_而不是后者，因为最终Elasticsearch是后备存储。

除了上述类型之外，Elasticsearch SQL 还支持特定于 _runtime_SQL 的类型，这些类型在 Elasticsearch 中没有等效类型。这些类型不能从Elasticsearch加载(因为它不知道它们)，但是可以在Elasticsearch SQL的查询或其结果中使用。

下表指出了这些类型：

**SQL 类型**

|

**SQL 精度** ---|--- 'date'

|

29 "时间"

|

18 'interval_year'

|

7 "interval_month"

|

7 "interval_day"

|

23 "interval_hour"

|

23 "interval_minute"

|

23 "interval_second"

|

23 "interval_year_to_month"

|

7 "interval_day_to_hour"

|

23 "interval_day_to_minute"

|

23 "interval_day_to_second"

|

23 "interval_hour_to_minute"

|

23 "interval_hour_to_second"

|

23 "interval_minute_to_second"

|

23 "geo_point"

|

52 "geo_shape"

|

2，147，483，647 "形状"

|

2，147，483，647 #### SQL 和多字段编辑

Elasticsearch 中的核心概念是"分析"字段，即为了有效索引而解释的全文值。这些字段的类型是"文本"，不用于排序或聚合，因为它们的实际值取决于所使用的"分析器"，因此 Elasticsearch 还提供用于存储 _exact_ 值的"关键字"类型。

在大多数情况下，实际上是默认的，是将两种类型用于Elasticsearch通过多字段支持的字符串，即能够以多种方式索引同一字符串;例如，将其索引为搜索的"文本"，也作为排序和聚合的"关键字"。

由于SQL需要精确的值，当遇到"文本"字段时，LasticsearchSQL将搜索一个精确的多字段，可用于比较，排序和聚合。为此，它将搜索它可以找到的第一个"关键字"，并将其用作原始field_exact_值。

请考虑以下"字符串"映射：

    
    
    {
      "first_name": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      }
    }

以下 SQL 查询：

    
    
    SELECT first_name FROM index WHERE first_name = 'John'

与以下内容相同：

    
    
    SELECT first_name FROM index WHERE first_name.raw = 'John'

因为 Elasticsearch SQL 会自动从"原始"中选取"原始"多字段以进行精确匹配。

[« SHOW TABLES](sql-syntax-show-tables.md) [Index patterns »](sql-index-
patterns.md)
