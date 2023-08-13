

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md)

[« Set up a data stream](set-up-a-data-stream.md) [Modify a data stream
»](modify-data-streams.md)

## 使用数据流

设置数据流后，您可以执行以下操作：

* 将文档添加到数据流 * 搜索数据流 * 获取数据流的统计信息 * 手动滚动数据流 * 打开封闭的支持索引 * 使用数据流重新编制索引 * 通过查询更新数据流中的文档 * 通过查询删除数据流中的文档 * 更新或删除后备索引中的文档

### 将文档添加到数据流

若要添加单个文档，请使用索引 API。支持引入管道。

    
    
    POST /my-data-stream/_doc/
    {
      "@timestamp": "2099-03-08T11:06:07.000Z",
      "user": {
        "id": "8a4f500d"
      },
      "message": "Login successful"
    }

您无法使用索引 API 的"PUT//<target>_doc/<_id>"请求格式向数据流添加新文档。要指定文档 ID，请改用"PUT//<target>_create/<_id>"格式。仅支持"创建"的"op_type"。

要使用单个请求添加多个文档，请使用批量 API。仅支持"创建"操作。

    
    
    response = client.bulk(
      index: 'my-data-stream',
      refresh: true,
      body: [
        {
          create: {}
        },
        {
          "@timestamp": '2099-03-08T11:04:05.000Z',
          user: {
            id: 'vlb44hny'
          },
          message: 'Login attempt failed'
        },
        {
          create: {}
        },
        {
          "@timestamp": '2099-03-08T11:06:07.000Z',
          user: {
            id: '8a4f500d'
          },
          message: 'Login successful'
        },
        {
          create: {}
        },
        {
          "@timestamp": '2099-03-09T11:07:08.000Z',
          user: {
            id: 'l7gk7f82'
          },
          message: 'Logout successful'
        }
      ]
    )
    puts response
    
    
    PUT /my-data-stream/_bulk?refresh
    {"create":{ }}
    { "@timestamp": "2099-03-08T11:04:05.000Z", "user": { "id": "vlb44hny" }, "message": "Login attempt failed" }
    {"create":{ }}
    { "@timestamp": "2099-03-08T11:06:07.000Z", "user": { "id": "8a4f500d" }, "message": "Login successful" }
    {"create":{ }}
    { "@timestamp": "2099-03-09T11:07:08.000Z", "user": { "id": "l7gk7f82" }, "message": "Logout successful" }

### 搜索数据流

以下搜索 API 支持数据流：

* 搜索 * 异步搜索 * 多重搜索 * 字段功能 * EQL 搜索

### 获取数据流的统计信息

使用数据流统计信息 API 获取一个或多个数据流的统计信息：

    
    
    response = client.indices.data_streams_stats(
      name: 'my-data-stream',
      human: true
    )
    puts response
    
    
    GET /_data_stream/my-data-stream/_stats?human=true

### 手动滚动数据流

使用滚动更新 API 手动滚动更新数据流：

    
    
    response = client.indices.rollover(
      alias: 'my-data-stream'
    )
    puts response
    
    
    POST /my-data-stream/_rollover/

### 打开封闭背衬索引

您无法搜索封闭的后备索引，即使通过搜索其数据流也是如此。您也不能更新或删除封闭索引中的文档。

要重新打开已关闭的支持索引，请直接向索引提交开放索引 API 请求：

    
    
    response = client.indices.open(
      index: '.ds-my-data-stream-2099.03.07-000001'
    )
    puts response
    
    
    POST /.ds-my-data-stream-2099.03.07-000001/_open/

要重新打开数据流的所有已关闭的支持索引，请向流提交打开的索引 API 请求：

    
    
    response = client.indices.open(
      index: 'my-data-stream'
    )
    puts response
    
    
    POST /my-data-stream/_open/

### 使用数据流重新编制索引

使用重新索引 API 将文档从现有索引、别名或数据流复制到数据流。由于数据流是仅追加的，因此重新索引到数据流中必须使用"创建"的"op_type"。Areindex 无法更新数据流中的现有文档。

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'archive'
        },
        dest: {
          index: 'my-data-stream',
          op_type: 'create'
        }
      }
    )
    puts response
    
    
    POST /_reindex
    {
      "source": {
        "index": "archive"
      },
      "dest": {
        "index": "my-data-stream",
        "op_type": "create"
      }
    }

### 按查询更新数据流中的文档

使用查询更新 API 更新数据流中与提供的查询匹配的文档：

    
    
    response = client.update_by_query(
      index: 'my-data-stream',
      body: {
        query: {
          match: {
            "user.id": 'l7gk7f82'
          }
        },
        script: {
          source: 'ctx._source.user.id = params.new_id',
          params: {
            new_id: 'XgdX0NoX'
          }
        }
      }
    )
    puts response
    
    
    POST /my-data-stream/_update_by_query
    {
      "query": {
        "match": {
          "user.id": "l7gk7f82"
        }
      },
      "script": {
        "source": "ctx._source.user.id = params.new_id",
        "params": {
          "new_id": "XgdX0NoX"
        }
      }
    }

### 按查询删除数据流中的文档

使用按查询删除 API 删除数据流中与提供的查询匹配的文档：

    
    
    response = client.delete_by_query(
      index: 'my-data-stream',
      body: {
        query: {
          match: {
            "user.id": 'vlb44hny'
          }
        }
      }
    )
    puts response
    
    
    POST /my-data-stream/_delete_by_query
    {
      "query": {
        "match": {
          "user.id": "vlb44hny"
        }
      }
    }

### 更新或删除备份索引中的文档

如果需要，您可以通过向包含文档的后备索引发送请求来更新或删除数据流中的文档。您将需要：

* 文档 ID * 包含文档的支持索引的名称 * 如果更新文档，则为其序列号和主要术语

要获取此信息，请使用搜索请求：

    
    
    response = client.search(
      index: 'my-data-stream',
      body: {
        seq_no_primary_term: true,
        query: {
          match: {
            "user.id": 'yWIumJd7'
          }
        }
      }
    )
    puts response
    
    
    GET /my-data-stream/_search
    {
      "seq_no_primary_term": true,
      "query": {
        "match": {
          "user.id": "yWIumJd7"
        }
      }
    }

Response:

    
    
    {
      "took": 20,
      "timed_out": false,
      "_shards": {
        "total": 3,
        "successful": 3,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 0.2876821,
        "hits": [
          {
            "_index": ".ds-my-data-stream-2099.03.08-000003",      __"_id": "bfspvnIBr7VVZlfp2lqX", __"_seq_no": 0, __"_primary_term": 1, __"_score": 0.2876821,
            "_source": {
              "@timestamp": "2099-03-08T11:06:07.000Z",
              "user": {
                "id": "yWIumJd7"
              },
              "message": "Login successful"
            }
          }
        ]
      }
    }

__

|

包含匹配文档的支持索引 ---|--- __

|

文档的文档 ID __

|

文档的当前序列号 __

|

文档的主要术语 要更新文档，请使用具有有效"if_seq_no"和"if_primary_term"参数的索引 API请求：

    
    
    PUT /.ds-my-data-stream-2099-03-08-000003/_doc/bfspvnIBr7VVZlfp2lqX?if_seq_no=0&if_primary_term=1
    {
      "@timestamp": "2099-03-08T11:06:07.000Z",
      "user": {
        "id": "8a4f500d"
      },
      "message": "Login successful"
    }

要删除文档，请使用删除 API：

    
    
    response = client.delete(
      index: '.ds-my-data-stream-2099.03.08-000003',
      id: 'bfspvnIBr7VVZlfp2lqX'
    )
    puts response
    
    
    DELETE /.ds-my-data-stream-2099.03.08-000003/_doc/bfspvnIBr7VVZlfp2lqX

要使用单个请求删除或更新多个文档，请使用批量 API 的"删除"、"索引"和"更新"操作。对于"索引"操作，包括有效的"if_seq_no"和"if_primary_term"参数。

    
    
    response = client.bulk(
      refresh: true,
      body: [
        {
          index: {
            _index: '.ds-my-data-stream-2099.03.08-000003',
            _id: 'bfspvnIBr7VVZlfp2lqX',
            if_seq_no: 0,
            if_primary_term: 1
          }
        },
        {
          "@timestamp": '2099-03-08T11:06:07.000Z',
          user: {
            id: '8a4f500d'
          },
          message: 'Login successful'
        }
      ]
    )
    puts response
    
    
    PUT /_bulk?refresh
    { "index": { "_index": ".ds-my-data-stream-2099.03.08-000003", "_id": "bfspvnIBr7VVZlfp2lqX", "if_seq_no": 0, "if_primary_term": 1 } }
    { "@timestamp": "2099-03-08T11:06:07.000Z", "user": { "id": "8a4f500d" }, "message": "Login successful" }

[« Set up a data stream](set-up-a-data-stream.md) [Modify a data stream
»](modify-data-streams.md)
