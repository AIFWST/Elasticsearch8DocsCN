

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[SQL APIs](sql-apis.md)

[« Clear SQL cursor API](clear-sql-cursor-api.md) [Get async SQL search API
»](get-async-sql-search-api.md)

## 删除异步 SQL 搜索API

删除异步 SQL 搜索或存储的同步 SQL 搜索。如果搜索仍在运行，API 将取消搜索。

    
    
    response = client.sql.delete_async(
      id: 'FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM='
    )
    puts response
    
    
    DELETE _sql/async/delete/FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM=

###Request

"删除_sql/异步/删除/<search_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则只有以下用户可以使用此 API 删除搜索：

    * Users with the `cancel_task` [cluster privilege](security-privileges.html#privileges-list-cluster "Cluster privileges")
    * The user who first submitted the search 

####Limitations

请参阅_SQL Limitations_。

### 路径参数

`<search_id>`

     (Required, string) Identifier for the search. 

[« Clear SQL cursor API](clear-sql-cursor-api.md) [Get async SQL search API
»](get-async-sql-search-api.md)
