

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[SQL APIs](sql-apis.md)

[« SQL search API](sql-search-api.md) [Transform APIs »](transform-
apis.md)

## SQL 翻译接口

将 SQL 搜索转换为包含 QueryDSL 的搜索 API 请求。请参阅_SQL翻译API_。

    
    
    POST _sql/translate
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 10
    }

###Request

"获取_sql/翻译"

"发布_sql/翻译"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对搜索的数据流、索引或别名具有"读取"索引权限。

####Limitations

请参阅_SQL Limitations_。

### 请求正文

SQL 翻译 API 接受与 SQLsearch API 相同的请求正文参数，不包括"游标"。

### 响应正文

SQL 翻译 API 返回与搜索 API 相同的响应正文。

[« SQL search API](sql-search-api.md) [Transform APIs »](transform-
apis.md)
