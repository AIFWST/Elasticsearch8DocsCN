

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« Data Types](sql-data-types.md) [Frozen Indices »](sql-index-frozen.md)

## 索引模式

Elasticsearch SQL支持两种类型的模式来匹配多个索引或表：

#### 弹性搜索多目标语法

_as long_支持用于枚举、包括或排除多目标语法的 Elasticsearch 表示法，因为它作为表标识符被引用或转义。

例如：

    
    
    SHOW TABLES "*,-l*";
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX
    javaRestTest      |employees      |VIEW      |ALIAS

请注意，模式由双引号 '"' 括起来。它枚举了"*"表示所有索引，但它排除了(由于"-")所有以"l"开头的索引。这种表示法非常方便和强大，因为它允许包含和排除，具体取决于目标命名约定。

相同类型的模式也可用于查询多个索引或表。

例如：

    
    
    SELECT emp_no FROM "e*p" LIMIT 1;
    
        emp_no
    ---------------
    10001

存在一个限制，即所有解析的具体表都具有完全相同的映射。

preview] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 要运行 [跨集群搜索，请使用 '：" 语法指定集群名称<remote_cluster><target>，其中 '' <remote_cluster>映射到 SQLcatalog(集群)，而 '<target>' 映射到表(索引或数据流)。""<remote_cluster>支持通配符("*")，"<target>"可以是索引模式。

例如：

    
    
    SELECT emp_no FROM "my*cluster:*emp" LIMIT 1;
    
        emp_no
    ---------------
    10001

#### SQL 'LIKE'表示法

常见的"LIKE"语句(包括在需要时进行转义)，用于匹配基于一个"_"或多个"%"字符的通配符模式。

再次使用"显示表"命令：

    
    
    SHOW TABLES LIKE 'emp%';
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX
    javaRestTest      |employees      |VIEW      |ALIAS

该模式匹配所有以"emp"开头的表。

此命令也支持 _escaping_，例如：

    
    
    SHOW TABLES LIKE 'emp!%' ESCAPE '!';
    
     catalog       |     name      |     type      |     kind
    ---------------+---------------+---------------+---------------

请注意，现在 "emp%" 与任何表都不匹配，因为 "%"(表示匹配零个或多个字符)已被 '！' 转义，因此成为常规字符。由于没有名为"emp%"的表，因此返回一个空表。

简而言之，两种模式之间的区别是：

**Feature**

|

**多索引**

|

**SQL'LIKE'** ---|---|--- **引用类型**

|

`"`

|

""**包含**

|

Yes

|

是 **排除**

|

Yes

|

无枚举**

|

Yes

|

否 **一个字符模式**

|

No

|

'_' **多字符模式**

|

`*`

|

'%' **正在转义**

|

No

|

"逃逸"使用哪一个取决于您，但是请尝试在您的查询中坚持使用同一个查询以保持一致性。

由于两种模式之间的引用查询类型非常相似(""vs ")，Elasticsearch SQL _always_ 需要关键字"LIKE"来表示 SQL "LIKE"模式。

[« Data Types](sql-data-types.md) [Frozen Indices »](sql-index-frozen.md)
