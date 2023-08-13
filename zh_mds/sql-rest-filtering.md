

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« Paginating through a large response](sql-pagination.md) [Columnar results
»](sql-rest-columnar.md)

## 使用 Elasticsearch QueryDSL 进行过滤

可以通过在过滤器参数中指定查询来过滤SQL将使用标准ElasticsearchQuery DSL运行的结果。

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        filter: {
          range: {
            page_count: {
              gte: 100,
              lte: 200
            }
          }
        },
        fetch_size: 5
      }
    )
    puts response
    
    
    POST /_sql?format=txt
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "filter": {
        "range": {
          "page_count": {
            "gte" : 100,
            "lte" : 200
          }
        }
      },
      "fetch_size": 5
    }

其中返回：

    
    
        author     |                name                |  page_count   | release_date
    ---------------+------------------------------------+---------------+------------------------
    Douglas Adams  |The Hitchhiker's Guide to the Galaxy|180            |1979-10-12T00:00:00.000Z

标准查询 DSL 筛选的一个有用且不太明显的用法是按特定路由键搜索文档。由于 Elasticsearch SQL 不支持"路由"参数，因此可以为"_routing"字段指定"术语"过滤器：

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        query: 'SELECT * FROM library',
        filter: {
          terms: {
            _routing: [
              'abc'
            ]
          }
        }
      }
    )
    puts response
    
    
    POST /_sql?format=txt
    {
      "query": "SELECT * FROM library",
      "filter": {
        "terms": {
          "_routing": ["abc"]
        }
      }
    }

[« Paginating through a large response](sql-pagination.md) [Columnar results
»](sql-rest-columnar.md)
