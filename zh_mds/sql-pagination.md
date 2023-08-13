

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« Response Data Formats](sql-rest-format.md) [Filtering using Elasticsearch
Query DSL »](sql-rest-filtering.md)

## 通过大响应进行分页

使用上一节中的示例，可以通过发回光标字段来继续下一页。对于 CSV、TSV 和 TXT 格式，游标在"游标"HTTP 标头中返回。

    
    
    POST /_sql?format=json
    {
      "cursor": "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWYUpOYklQMHhRUEtld3RsNnFtYU1hQQ==:BAFmBGRhdGUBZgVsaWtlcwFzB21lc3NhZ2UBZgR1c2Vy9f///w8="
    }

看起来像：

    
    
    {
      "rows" : [
        ["Dan Simmons",        "Hyperion",             482,  "1989-05-26T00:00:00.000Z"],
        ["Iain M. Banks",      "Consider Phlebas",     471,  "1987-04-23T00:00:00.000Z"],
        ["Neal Stephenson",    "Snow Crash",           470,  "1992-06-01T00:00:00.000Z"],
        ["Frank Herbert",      "God Emperor of Dune",  454,  "1981-05-28T00:00:00.000Z"],
        ["Frank Herbert",      "Children of Dune",     408,  "1976-04-21T00:00:00.000Z"]
      ],
      "cursor" : "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWODRMaXBUaVlRN21iTlRyWHZWYUdrdw==:BAFmBmF1dGhvcgFmBG5hbWUBZgpwYWdlX2NvdW50AWYMcmVsZWFzZV9kYXRl9f///w8="
    }

请注意，"列"对象只是第一页的一部分。

当结果中没有返回"光标"时，您已到达最后一页。与 Elasticsearch 的滚动一样，SQL 可以在 Elasticsearch 中保留状态以支持光标。与滚动不同，接收最后一页足以保证清除 Elasticsearch 状态。

若要提前清除状态，请使用清除游标 API：

    
    
    POST /_sql/close
    {
      "cursor": "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWYUpOYklQMHhRUEtld3RsNnFtYU1hQQ==:BAFmBGRhdGUBZgVsaWtlcwFzB21lc3NhZ2UBZgR1c2Vy9f///w8="
    }

哪个会喜欢返回

    
    
    {
      "succeeded" : true
    }

[« Response Data Formats](sql-rest-format.md) [Filtering using Elasticsearch
Query DSL »](sql-rest-filtering.md)
