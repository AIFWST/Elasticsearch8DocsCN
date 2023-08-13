

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« Index patterns](sql-index-patterns.md) [Functions and Operators »](sql-
functions.md)

## 冻结指数

默认情况下，Elasticsearch SQL 不会搜索冻结的索引。要搜索冻结的索引，请使用以下功能之一：

专用配置参数

     Set to `true` properties `index_include_frozen` in the [SQL search API](sql-search-api.html "SQL search API") or `index.include.frozen` in the drivers to include frozen indices. 
dedicated keyword

     Explicitly perform the inclusion through the dedicated `FROZEN` keyword in the `FROM` clause or `INCLUDE FROZEN` in the `SHOW` commands: 
    
    
    SHOW TABLES INCLUDE FROZEN;
    
     catalog       |     name      | type     |     kind
    ---------------+---------------+----------+---------------
    javaRestTest      |archive        |TABLE     |FROZEN INDEX
    javaRestTest      |emp            |TABLE     |INDEX
    javaRestTest      |employees      |VIEW      |ALIAS
    javaRestTest      |library        |TABLE     |INDEX
    
    
    SELECT * FROM FROZEN archive LIMIT 1;
    
         author      |        name        |  page_count   |    release_date
    -----------------+--------------------+---------------+--------------------
    James S.A. Corey |Leviathan Wakes     |561            |2011-06-02T00:00:00Z

除非启用，否则冻结索引将被完全忽略;就好像它们不存在一样，因此，针对它们运行的查询可能会失败。

[« Index patterns](sql-index-patterns.md) [Functions and Operators »](sql-
functions.md)
