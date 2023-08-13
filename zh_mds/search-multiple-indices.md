

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Search across clusters](modules-cross-cluster-search.md) [Search shard
routing »](search-shard-routing.md)

## 搜索多个数据流和索引

要搜索多个数据流和索引，请将它们作为逗号分隔的值添加到搜索 API 的请求路径中。

以下请求搜索"my-index-000001"和"my-index-000002"索引。

    
    
    response = client.search(
      index: 'my-index-000001,my-index-000002',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001,my-index-000002/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

您还可以使用索引模式搜索多个数据流和索引。

以下请求以"my-index-*"索引模式为目标。该请求搜索集群中以"my-index-"开头的任何数据流或索引。

    
    
    response = client.search(
      index: 'my-index-*',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-*/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

要搜索集群中的所有数据流和索引，请从请求路径中省略目标。或者，您可以使用"_all"或"*"。

以下请求是等效的，可搜索集群中的所有数据流和索引。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: '_all',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: '*',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }
    
    GET /_all/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }
    
    GET /*/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

### 指数提升

搜索多个索引时，可以使用"indices_boost"参数提升一个或多个指定索引的结果。当来自某些指数的命中比其他指数的命中更重要时，这很有用。

不能对数据流使用"indices_boost"。

    
    
    response = client.search(
      body: {
        indices_boost: [
          {
            "my-index-000001": 1.4
          },
          {
            "my-index-000002": 1.3
          }
        ]
      }
    )
    puts response
    
    
    GET /_search
    {
      "indices_boost": [
        { "my-index-000001": 1.4 },
        { "my-index-000002": 1.3 }
      ]
    }

还可以使用别名和索引模式：

    
    
    response = client.search(
      body: {
        indices_boost: [
          {
            "my-alias": 1.4
          },
          {
            "my-index*": 1.3
          }
        ]
      }
    )
    puts response
    
    
    GET /_search
    {
      "indices_boost": [
        { "my-alias":  1.4 },
        { "my-index*": 1.3 }
      ]
    }

如果找到多个匹配项，将使用第一个匹配项。例如，如果索引包含在"alias1"中并且与"my-index*"模式匹配，则应用"1.4"的提升值。

[« Search across clusters](modules-cross-cluster-search.md) [Search shard
routing »](search-shard-routing.md)
