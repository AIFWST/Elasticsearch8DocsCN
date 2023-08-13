

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« Overview](sql-overview.md) [Conventions and Terminology »](sql-
concepts.md)

## SQL入门

要开始使用 Elasticsearch SQL，请创建一个包含一些数据的索引以供试验：

    
    
    response = client.bulk(
      index: 'library',
      refresh: true,
      body: [
        {
          index: {
            _id: 'Leviathan Wakes'
          }
        },
        {
          name: 'Leviathan Wakes',
          author: 'James S.A. Corey',
          release_date: '2011-06-02',
          page_count: 561
        },
        {
          index: {
            _id: 'Hyperion'
          }
        },
        {
          name: 'Hyperion',
          author: 'Dan Simmons',
          release_date: '1989-05-26',
          page_count: 482
        },
        {
          index: {
            _id: 'Dune'
          }
        },
        {
          name: 'Dune',
          author: 'Frank Herbert',
          release_date: '1965-06-01',
          page_count: 604
        }
      ]
    )
    puts response
    
    
    PUT /library/_bulk?refresh
    {"index":{"_id": "Leviathan Wakes"}}
    {"name": "Leviathan Wakes", "author": "James S.A. Corey", "release_date": "2011-06-02", "page_count": 561}
    {"index":{"_id": "Hyperion"}}
    {"name": "Hyperion", "author": "Dan Simmons", "release_date": "1989-05-26", "page_count": 482}
    {"index":{"_id": "Dune"}}
    {"name": "Dune", "author": "Frank Herbert", "release_date": "1965-06-01", "page_count": 604}

现在，您可以使用SQL搜索API执行SQL：

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        query: "SELECT * FROM library WHERE release_date < '2000-01-01'"
      }
    )
    puts response
    
    
    POST /_sql?format=txt
    {
      "query": "SELECT * FROM library WHERE release_date < '2000-01-01'"
    }

它应该返回如下内容：

    
    
        author     |     name      |  page_count   | release_date
    ---------------+---------------+---------------+------------------------
    Dan Simmons    |Hyperion       |482            |1989-05-26T00:00:00.000Z
    Frank Herbert  |Dune           |604            |1965-06-01T00:00:00.000Z

您也可以使用_SQL CLI_。在 x-pack 的 bin 目录中有一个脚本来启动它：

    
    
    $ ./bin/elasticsearch-sql-cli

从那里，您可以运行相同的查询：

    
    
    sql> SELECT * FROM library WHERE release_date < '2000-01-01';
        author     |     name      |  page_count   | release_date
    ---------------+---------------+---------------+------------------------
    Dan Simmons    |Hyperion       |482            |1989-05-26T00:00:00.000Z
    Frank Herbert  |Dune           |604            |1965-06-01T00:00:00.000Z

[« Overview](sql-overview.md) [Conventions and Terminology »](sql-
concepts.md)
