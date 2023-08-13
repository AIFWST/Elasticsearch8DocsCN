

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« `?refresh`](docs-refresh.md) [Enrich APIs »](enrich-apis.md)

## 乐观并发控制

Elasticsearch是分布式的。创建、更新或删除文档时，必须将文档的新版本复制到群集中的其他节点。Elasticsearch也是异步和并发的，这意味着这些复制请求是并行发送的，并且可能不按顺序到达目的地。Elasticsearch 需要一种方法来确保文档的旧版本永远不会覆盖较新版本。

为了确保较旧版本的文档不会覆盖较新版本，对文档执行的每个操作都由协调该更改的主分片分配一个序列号。每个操作都会增加序列号，因此保证较新的操作具有比旧操作更高的序列号。然后，Elasticsearch 可以使用操作的序列号来确保较新的文档版本永远不会被分配了较小序列号的更改覆盖。

例如，以下索引命令将创建一个文档并为其分配初始序列号和主要术语：

    
    
    PUT products/_doc/1567
    {
      "product" : "r2d2",
      "details" : "A resourceful astromech droid"
    }

您可以在响应的"_seq_no"和"_primary_term"字段中看到分配的序列号和主要术语：

    
    
    {
      "_shards": {
        "total": 2,
        "failed": 0,
        "successful": 1
      },
      "_index": "products",
      "_id": "1567",
      "_version": 1,
      "_seq_no": 362,
      "_primary_term": 2,
      "result": "created"
    }

Elasticsearch 会跟踪上次操作的序列号和主要术语，以更改它存储的每个文档。序列号和主要术语在 GET API 响应的"_seq_no"和"_primary_term"字段中返回：

    
    
    response = client.get(
      index: 'products',
      id: 1567
    )
    puts response
    
    
    GET products/_doc/1567

returns:

    
    
    {
      "_index": "products",
      "_id": "1567",
      "_version": 1,
      "_seq_no": 362,
      "_primary_term": 2,
      "found": true,
      "_source": {
        "product": "r2d2",
        "details": "A resourceful astromech droid"
      }
    }

注意：搜索 API 可以通过设置"seq_no_primary_term"参数为每个搜索命中返回"_seq_no"和"_primary_term"。

序列号和主要术语唯一标识更改。通过记下返回的序列号和主要术语，您可以确保仅在检索文档后未对文档进行其他更改时才更改文档。这是通过设置索引 API、更新 API 或删除 API 的"if_seq_no"和"if_primary_term"参数来完成的。

例如，以下索引调用将确保向文档添加标记，而不会丢失对描述的任何潜在更改或另一个 API 添加的另一个标记：

    
    
    PUT products/_doc/1567?if_seq_no=362&if_primary_term=2
    {
      "product": "r2d2",
      "details": "A resourceful astromech droid",
      "tags": [ "droid" ]
    }

[« `?refresh`](docs-refresh.md) [Enrich APIs »](enrich-apis.md)
