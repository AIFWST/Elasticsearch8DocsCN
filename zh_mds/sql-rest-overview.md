

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« SQL REST API](sql-rest.md) [Response Data Formats »](sql-rest-
format.md)

##Overview

SQL 搜索 API 接受 JSON 文档中的 SQL，执行它并返回结果。例如：

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC LIMIT 5'
      }
    )
    puts response
    
    
    POST /_sql?format=txt
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC LIMIT 5"
    }

其中返回：

    
    
         author      |        name        |  page_count   | release_date
    -----------------+--------------------+---------------+------------------------
    Peter F. Hamilton|Pandora's Star      |768            |2004-03-02T00:00:00.000Z
    Vernor Vinge     |A Fire Upon the Deep|613            |1992-06-01T00:00:00.000Z
    Frank Herbert    |Dune                |604            |1965-06-01T00:00:00.000Z
    Alastair Reynolds|Revelation Space    |585            |2000-03-15T00:00:00.000Z
    James S.A. Corey |Leviathan Wakes     |561            |2011-06-02T00:00:00.000Z

### 使用 Kibana 控制台

如果您使用的是 Kibana 控制台(强烈建议这样做)，请在创建查询时利用三引号 '"""'。这不仅会自动转义查询字符串中的双引号 ('"')，而且还支持多行，如下所示：

！控制台三重引号

[« SQL REST API](sql-rest.md) [Response Data Formats »](sql-rest-
format.md)
