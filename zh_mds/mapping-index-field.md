

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_id` field](mapping-id-field.md) [`_meta` field »](mapping-meta-
field.md)

## '_index'字段

跨多个索引执行查询时，有时需要添加仅与某些索引的文档关联的查询子句。"_index"字段允许匹配文档索引到的索引。它的值在某些查询和聚合中以及排序或脚本编写时可访问：

    
    
    response = client.index(
      index: 'index_1',
      id: 1,
      body: {
        text: 'Document in index 1'
      }
    )
    puts response
    
    response = client.index(
      index: 'index_2',
      id: 2,
      refresh: true,
      body: {
        text: 'Document in index 2'
      }
    )
    puts response
    
    response = client.search(
      index: 'index_1,index_2',
      body: {
        query: {
          terms: {
            _index: [
              'index_1',
              'index_2'
            ]
          }
        },
        aggregations: {
          indices: {
            terms: {
              field: '_index',
              size: 10
            }
          }
        },
        sort: [
          {
            _index: {
              order: 'asc'
            }
          }
        ],
        script_fields: {
          index_name: {
            script: {
              lang: 'painless',
              source: "doc['_index']"
            }
          }
        }
      }
    )
    puts response
    
    
    PUT index_1/_doc/1
    {
      "text": "Document in index 1"
    }
    
    PUT index_2/_doc/2?refresh=true
    {
      "text": "Document in index 2"
    }
    
    GET index_1,index_2/_search
    {
      "query": {
        "terms": {
          "_index": ["index_1", "index_2"] __}
      },
      "aggs": {
        "indices": {
          "terms": {
            "field": "_index", __"size": 10
          }
        }
      },
      "sort": [
        {
          "_index": { __"order": "asc"
          }
        }
      ],
      "script_fields": {
        "index_name": {
          "script": {
            "lang": "painless",
            "source": "doc['_index']" __}
        }
      }
    }

__

|

查询"_index"字段 ---|--- __

|

聚合在"_index"字段 __

|

在"_index"字段 __ 上排序

|

访问脚本中的"_index"字段 "_index"字段是虚拟公开的 - 它不会作为真实字段添加到 Lucene 索引中。这意味着您可以在"term"或"terms"查询(或重写为"term"查询的任何查询，例如"match"、"query_string"或"simple_query_string"查询)以及"前缀"和"通配符"查询中使用"_index"字段。但是，它不支持"正则表达式"和"模糊"查询。

对"_index"字段的查询除了接受具体的索引名称外，还接受索引别名。

指定远程索引名称(如"cluster_1：index_3")时，查询必须包含分隔符"："。例如，对"cluster_*：index_3"的"通配符"查询将匹配远程索引中的文档。但是，"cluster*index_1"上的查询仅与本地索引匹配，因为存在noseparator。此行为与远程索引名称的常规解析规则一致。

[« `_id` field](mapping-id-field.md) [`_meta` field »](mapping-meta-
field.md)
