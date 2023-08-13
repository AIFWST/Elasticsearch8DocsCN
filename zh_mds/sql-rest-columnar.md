

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« Filtering using Elasticsearch Query DSL](sql-rest-filtering.md) [Passing
parameters to a query »](sql-rest-params.md)

## 列结果

通常，显示 SQL 查询结果结果的最广为人知的方式是每个单独的记录/文档表示一行/一行。对于某些格式，Elasticsearch SQL 可以以列式方式返回结果：一行表示当前结果页面中某个列的所有值。

可以按列方向返回以下格式："json"、"yaml"、"cbor"和"smile"。

    
    
    response = client.sql.query(
      format: 'json',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5,
        columnar: true
      }
    )
    puts response
    
    
    POST /_sql?format=json
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5,
      "columnar": true
    }

其中返回：

    
    
    {
      "columns": [
        {"name": "author", "type": "text"},
        {"name": "name", "type": "text"},
        {"name": "page_count", "type": "short"},
        {"name": "release_date", "type": "datetime"}
      ],
      "values": [
        ["Peter F. Hamilton", "Vernor Vinge", "Frank Herbert", "Alastair Reynolds", "James S.A. Corey"],
        ["Pandora's Star", "A Fire Upon the Deep", "Dune", "Revelation Space", "Leviathan Wakes"],
        [768, 613, 604, 585, 561],
        ["2004-03-02T00:00:00.000Z", "1992-06-01T00:00:00.000Z", "1965-06-01T00:00:00.000Z", "2000-03-15T00:00:00.000Z", "2011-06-02T00:00:00.000Z"]
      ],
      "cursor": "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWWWdrRlVfSS1TbDYtcW9lc1FJNmlYdw==:BAFmBmF1dGhvcgFmBG5hbWUBZgpwYWdlX2NvdW50AWYMcmVsZWFzZV9kYXRl+v///w8="
    }

任何使用"游标"的后续调用仍然必须包含"columnar"参数以保留方向，这意味着初始查询将not_remember_列式选项。

    
    
    POST /_sql?format=json
    {
      "cursor": "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWWWdrRlVfSS1TbDYtcW9lc1FJNmlYdw==:BAFmBmF1dGhvcgFmBG5hbWUBZgpwYWdlX2NvdW50AWYMcmVsZWFzZV9kYXRl+v///w8=",
      "columnar": true
    }

看起来像：

    
    
    {
      "values": [
        ["Dan Simmons", "Iain M. Banks", "Neal Stephenson", "Frank Herbert", "Frank Herbert"],
        ["Hyperion", "Consider Phlebas", "Snow Crash", "God Emperor of Dune", "Children of Dune"],
        [482, 471, 470, 454, 408],
        ["1989-05-26T00:00:00.000Z", "1987-04-23T00:00:00.000Z", "1992-06-01T00:00:00.000Z", "1981-05-28T00:00:00.000Z", "1976-04-21T00:00:00.000Z"]
      ],
      "cursor": "46ToAwFzQERYRjFaWEo1UVc1a1JtVjBZMmdCQUFBQUFBQUFBQUVXWjBaNlFXbzNOV0pVY21Wa1NUZDJhV2t3V2xwblp3PT3/////DwQBZgZhdXRob3IBBHRleHQAAAFmBG5hbWUBBHRleHQAAAFmCnBhZ2VfY291bnQBBGxvbmcBAAFmDHJlbGVhc2VfZGF0ZQEIZGF0ZXRpbWUBAAEP"
    }

[« Filtering using Elasticsearch Query DSL](sql-rest-filtering.md) [Passing
parameters to a query »](sql-rest-params.md)
