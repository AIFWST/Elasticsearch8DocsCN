

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_meta` field](mapping-meta-field.md) [`_source` field »](mapping-source-
field.md)

## '_routing'字段

使用以下公式将文档路由到索引中的特定分片：

    
    
    routing_factor = num_routing_shards / num_primary_shards
    shard_num = (hash(_routing) % num_routing_shards) / routing_factor

"num_routing_shards"是"index.number_of_routing_shards"索引设置的值。"num_primary_shards"是"index.number_of_shards"索引设置的值。

默认的"_routing"值是文档的"_id"。可以通过为每个文档指定自定义"路由"值来实现自定义路由模式。例如：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      routing: 'user1',
      refresh: true,
      body: {
        title: 'This is a document'
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 1,
      routing: 'user1'
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?routing=user1&refresh=true __{
      "title": "This is a document"
    }
    
    GET my-index-000001/_doc/1?routing=user1 __

__

|

本文档使用"user1"作为其路由值，而不是其 ID。   ---|---    __

|

获取、删除或更新文档时需要提供相同的"路由"值。   "_routing"字段的值可在查询中访问：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          terms: {
            _routing: [
              'user1'
            ]
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "terms": {
          "_routing": [ "user1" ] __}
      }
    }

__

|

在"_routing"字段上进行查询(另请参阅"ids"查询) ---|--- 数据流不支持自定义路由，除非它们是在模板中启用"allow_custom_routing"设置的情况下创建的。

### 使用自定义路由进行搜索

自定义路由可以减少搜索的影响。不必将搜索请求扇出到索引中的所有分片，而是可以将请求发送到与特定路由值(或多个值)匹配的分片：

    
    
    response = client.search(
      index: 'my-index-000001',
      routing: 'user1,user2',
      body: {
        query: {
          match: {
            title: 'document'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search?routing=user1,user2 __{
      "query": {
        "match": {
          "title": "document"
        }
      }
    }

__

|

此搜索请求将仅在与"user1"和"user2"路由值关联的分片上执行。   ---|--- ### 创建路由值需要编辑

使用自定义路由时，每当索引、获取、删除或更新文档时，提供路由值非常重要。

忘记传送值可能会导致文档在多个分片上编制索引。作为保护措施，可以将"_routing"字段配置为使所有 CRUD 操作都需要自定义的"路由"值：

    
    
    response = client.indices.create(
      index: 'my-index-000002',
      body: {
        mappings: {
          _routing: {
            required: true
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000002',
      id: 1,
      body: {
        text: 'No routing value provided'
      }
    )
    puts response
    
    
    PUT my-index-000002
    {
      "mappings": {
        "_routing": {
          "required": true __}
      }
    }
    
    PUT my-index-000002/_doc/1 __{
      "text": "No routing value provided"
    }

__

|

所有文档都需要传送。   ---|---    __

|

此索引请求抛出"routing_missing_exception"。   ### 具有自定义路由编辑的唯一 ID

为指定自定义"_routing"的文档编制索引时，不能保证索引中所有分片中"_id"的唯一性。事实上，如果用不同的"_routing"值进行索引，具有相同"_id"的文档最终可能会在不同的分片上。

由用户来确保 ID 在整个索引中是唯一的。

### 路由到索引分区

可以配置索引，以便自定义路由值将转到分片的子集，而不是单个分片。这有助于降低最终出现不平衡群集的风险，同时仍可减少搜索的影响。

这是通过提供索引级别设置"index.routing_partition_size"atindex创建来完成的。随着分区大小的增加，数据分布越均匀，代价是必须为每个请求搜索更多分片。

当此设置存在时，用于计算分片的公式将变为：

    
    
    routing_value = hash(_routing) + hash(_id) % routing_partition_size
    shard_num = (routing_value % num_routing_shards) / routing_factor

也就是说，"_routing"字段用于计算索引中的一组分片，然后"_id"用于在该集中选择分片。

要启用此功能，"index.routing_partition_size"的值应大于 1 且小于"index.number_of_shards"。

启用后，分区索引将具有以下限制：

* 无法在其中创建具有"join"字段关系的映射。  * 索引中的所有映射都必须将"_routing"字段标记为必填。

[« `_meta` field](mapping-meta-field.md) [`_source` field »](mapping-source-
field.md)
