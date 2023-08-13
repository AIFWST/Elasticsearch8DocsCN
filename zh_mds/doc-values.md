

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `copy_to`](copy-to.md) [`dynamic` »](dynamic.md)

##'doc_values'

默认情况下，大多数字段都已编制索引，这使得它们可搜索。倒排索引允许查询在唯一的排序术语列表中查找搜索术语，并从中立即访问包含该术语的文档列表。

对脚本中的字段值进行排序、聚合和访问需要不同的数据访问模式。我们需要能够查找文档并查找它在字段中的术语，而不是查找术语和查找文档。

文档值是在文档索引时构建的磁盘上数据结构，这使得此数据访问模式成为可能。它们存储与"_source"相同的值，但以面向列的方式存储，可以更有效地进行排序和聚合。几乎所有字段类型都支持 Doc 值，_notable"文本"和"annotated_text"fields_除外。

### 仅文档值字段

数字类型、日期类型、布尔类型、iptype、geo_point 类型和关键字类型在未编制索引但仅启用文档值时也可以查询。文档值的查询性能比索引结构上的查询性能慢得多，但对于很少查询且查询性能不那么重要的字段，在磁盘使用和查询性能之间提供了一个有趣的权衡。这使得仅文档值字段非常适合通常不用于筛选的字段，例如指标数据的仪表或计数器。

仅文档值字段可以按如下方式配置：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            status_code: {
              type: 'long'
            },
            session_id: {
              type: 'long',
              index: false
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "status_code": { __"type":  "long"
          },
          "session_id": { __"type":  "long",
            "index": false
          }
        }
      }
    }

__

|

"status_code"字段是一个常规的长字段。   ---|---    __

|

"session_id"字段已禁用"索引"，因此是仅文档值的长字段，因为默认情况下启用文档值。   ### 禁用文档值编辑

默认情况下，所有支持 doc 值的字段都处于启用状态。如果您确定不需要对字段进行排序或聚合，或者从脚本访问字段值，则可以禁用文档值以节省磁盘空间：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            status_code: {
              type: 'keyword'
            },
            session_id: {
              type: 'keyword',
              doc_values: false
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "status_code": { __"type":       "keyword"
          },
          "session_id": { __"type":       "keyword",
            "doc_values": false
          }
        }
      }
    }

__

|

默认情况下，"status_code"字段启用了"doc_values"。   ---|---    __

|

"session_id"已禁用"doc_values"，但仍可查询。   您无法禁用"通配符"字段的文档值。

[« `copy_to`](copy-to.md) [`dynamic` »](dynamic.md)
