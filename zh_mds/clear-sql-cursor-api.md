

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[SQL APIs](sql-apis.md)

[« SQL APIs](sql-apis.md) [Delete async SQL search API »](delete-async-sql-
search-api.md)

## 清除 SQL 游标API

清除 SQL 搜索游标。

    
    
    POST _sql/close
    {
      "cursor": "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWYUpOYklQMHhRUEtld3RsNnFtYU1hQQ==:BAFmBGRhdGUBZgVsaWtlcwFzB21lc3NhZ2UBZgR1c2Vy9f///w8="
    }

###Request

"发布_sql/关闭"

####Limitations

请参阅_SQL Limitations_。

### 请求正文

`cursor`

     (Required, string) Cursor to clear. 

[« SQL APIs](sql-apis.md) [Delete async SQL search API »](delete-async-sql-
search-api.md)
