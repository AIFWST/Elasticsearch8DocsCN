

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« SHOW FUNCTIONS](sql-syntax-show-functions.md) [Data Types »](sql-data-
types.md)

## 展示表

**Synopsis:**

    
    
    SHOW TABLES
        [CATALOG [catalog_identifier | __LIKE pattern]]? __[INCLUDE FROZEN]? __[table_identifier | __LIKE pattern]? __

__

|

目录(群集)标识符。支持通配符 ("*")。   ---|---    __

|

与目录名称匹配的 SQL LIKE 模式。   __

|

是否包括冻结的索引。   __

|

单表(索引或数据流)标识符或双引号多目标模式。   __

|

与表名匹配的 SQL LIKE 模式。   有关模式的详细信息，请参阅索引模式。

**说明**：列出当前用户可用的表及其类型。

    
    
    SHOW TABLES;
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX
    javaRestTest      |employees      |VIEW      |ALIAS
    javaRestTest      |library        |TABLE     |INDEX

使用 Elasticsearch 多目标语法表示法匹配多个索引：

    
    
    SHOW TABLES "*,-l*";
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX
    javaRestTest      |employees      |VIEW      |ALIAS

还可以使用"LIKE"子句将名称列表限制为给定模式。

模式可以是完全匹配的：

    
    
    SHOW TABLES LIKE 'emp';
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX

多个字符：

    
    
    SHOW TABLES LIKE 'emp%';
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX
    javaRestTest      |employees      |VIEW      |ALIAS

单个字符：

    
    
    SHOW TABLES LIKE 'em_';
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX

或单个和多个字符的混合：

    
    
    SHOW TABLES LIKE '%em_';
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |emp            |TABLE     |INDEX

列出远程集群中名称与通配符匹配的表：

    
    
    SHOW TABLES CATALOG 'my_*' LIKE 'test_emp%';
    
         catalog     |     name      |     type      |     kind
    -----------------+---------------+---------------+---------------
    my_remote_cluster|test_emp       |TABLE          |INDEX
    my_remote_cluster|test_emp_copy  |TABLE          |INDEX

[« SHOW FUNCTIONS](sql-syntax-show-functions.md) [Data Types »](sql-data-
types.md)
