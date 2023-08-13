

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« SHOW CATALOGS](sql-syntax-show-catalogs.md) [SHOW FUNCTIONS »](sql-
syntax-show-functions.md)

## 显示列

**Synopsis:**

    
    
    SHOW COLUMNS
        [CATALOG identifier]? __[INCLUDE FROZEN]? __[FROM | IN]
        [table_identifier | __LIKE pattern] __

__

|

目录(群集)标识符。支持通配符 ("*")。   ---|---    __

|

是否包括冻结的索引。   __

|

单表(索引或数据流)标识符或双引号多目标模式。   __

|

与表名匹配的 SQL LIKE 模式。   有关模式的详细信息，请参阅索引模式。

**描述**：列出表中的列及其数据类型(和其他属性)。

    
    
    SHOW COLUMNS IN emp;
    
           column       |     type      |    mapping
    --------------------+---------------+---------------
    birth_date          |TIMESTAMP      |datetime
    dep                 |STRUCT         |nested
    dep.dep_id          |VARCHAR        |keyword
    dep.dep_name        |VARCHAR        |text
    dep.dep_name.keyword|VARCHAR        |keyword
    dep.from_date       |TIMESTAMP      |datetime
    dep.to_date         |TIMESTAMP      |datetime
    emp_no              |INTEGER        |integer
    first_name          |VARCHAR        |text
    first_name.keyword  |VARCHAR        |keyword
    gender              |VARCHAR        |keyword
    hire_date           |TIMESTAMP      |datetime
    languages           |TINYINT        |byte
    last_name           |VARCHAR        |text
    last_name.keyword   |VARCHAR        |keyword
    name                |VARCHAR        |keyword
    salary              |INTEGER        |integer

[« SHOW CATALOGS](sql-syntax-show-catalogs.md) [SHOW FUNCTIONS »](sql-
syntax-show-functions.md)
