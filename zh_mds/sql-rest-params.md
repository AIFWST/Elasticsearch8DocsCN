

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« Columnar results](sql-rest-columnar.md) [Use runtime fields »](sql-
runtime-fields.md)

## 将参数传递给查询

例如，在查询条件或"HAVING"语句中使用值可以通过将值集成到查询字符串本身中来"内联"完成：

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        query: "SELECT YEAR(release_date) AS year FROM library WHERE page_count > 300 AND author = 'Frank Herbert' GROUP BY year HAVING COUNT(*) > 0"
      }
    )
    puts response
    
    
    POST /_sql?format=txt
    {
    	"query": "SELECT YEAR(release_date) AS year FROM library WHERE page_count > 300 AND author = 'Frank Herbert' GROUP BY year HAVING COUNT(*) > 0"
    }

或者可以通过提取单独的参数列表中的值并在查询字符串中使用问号占位符 ('？') 来完成：

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        query: 'SELECT YEAR(release_date) AS year FROM library WHERE page_count > ? AND author = ? GROUP BY year HAVING COUNT(*) > ?',
        params: [
          300,
          'Frank Herbert',
          0
        ]
      }
    )
    puts response
    
    
    POST /_sql?format=txt
    {
    	"query": "SELECT YEAR(release_date) AS year FROM library WHERE page_count > ? AND author = ? GROUP BY year HAVING COUNT(*) > ?",
    	"params": [300, "Frank Herbert", 0]
    }

将值传递给查询的推荐方法是使用问号占位符，以避免任何黑客攻击或 SQL 注入的尝试。

[« Columnar results](sql-rest-columnar.md) [Use runtime fields »](sql-
runtime-fields.md)
