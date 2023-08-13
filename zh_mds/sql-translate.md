

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« Run an async SQL search](sql-async.md) [SQL CLI »](sql-cli.md)

## SQL 翻译接口

SQL Translate API 接受 JSON 文档中的 SQL，并将其转换为原生 Elasticsearch 查询。例如：

    
    
    response = client.sql.translate(
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 10
      }
    )
    puts response
    
    
    POST /_sql/translate
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 10
    }

其中返回：

    
    
    {
      "size": 10,
      "_source": false,
      "fields": [
        {
          "field": "author"
        },
        {
          "field": "name"
        },
        {
          "field": "page_count"
        },
        {
          "field": "release_date",
          "format": "strict_date_optional_time_nanos"
        }
      ],
      "sort": [
        {
          "page_count": {
            "order": "desc",
            "missing": "_first",
            "unmapped_type": "short"
          }
        }
      ],
      "track_total_hits": -1
    }

这是 SQL 将运行以提供结果的请求。在这种情况下，SQL 将使用滚动 API。如果结果包含聚合，则 SQL 将使用普通搜索 API。

请求正文接受与 SQL 搜索 API 相同的参数，不包括"游标"。

[« Run an async SQL search](sql-async.md) [SQL CLI »](sql-cli.md)
