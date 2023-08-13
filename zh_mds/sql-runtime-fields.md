

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« Passing parameters to a query](sql-rest-params.md) [Run an async SQL
search »](sql-async.md)

## 使用运行时字段

在搜索期间，使用"runtime_mappings"参数从现有运行时字段或列中提取和创建运行时字段或列。

以下搜索从"release_date"创建一个"release_day_of_week"运行时字段，并在响应中返回该字段。

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        runtime_mappings: {
          release_day_of_week: {
            type: 'keyword',
            script: "\n        emit(doc['release_date'].value.dayOfWeekEnum.toString())\n      "
          }
        },
        query: "\n    SELECT * FROM library WHERE page_count > 300 AND author = 'Frank Herbert'\n  "
      }
    )
    puts response
    
    
    POST _sql?format=txt
    {
      "runtime_mappings": {
        "release_day_of_week": {
          "type": "keyword",
          "script": """
            emit(doc['release_date'].value.dayOfWeekEnum.toString())
          """
        }
      },
      "query": """
        SELECT * FROM library WHERE page_count > 300 AND author = 'Frank Herbert'
      """
    }

该 API 返回：

    
    
        author     |     name      |  page_count   |      release_date      |release_day_of_week
    ---------------+---------------+---------------+------------------------+-------------------
    Frank Herbert  |Dune           |604            |1965-06-01T00:00:00.000Z|TUESDAY

[« Passing parameters to a query](sql-rest-params.md) [Run an async SQL
search »](sql-async.md)
