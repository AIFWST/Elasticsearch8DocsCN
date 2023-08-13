

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `similarity`](similarity.md) [`subobjects` »](subobjects.md)

##'商店'

默认情况下，对字段值编制索引以使其可搜索，但它们不是 _存储_。这意味着可以查询字段，但无法检索原始字段值。

通常这并不重要。字段值已经是默认存储的"_source"字段的一部分。如果您只想检索单个字段或几个字段的值，而不是整个"_source"的值，那么这可以通过源过滤来实现。

在某些情况下，"存储"字段是有意义的。例如，如果您有一个包含"标题"、"日期"和非常大的"内容"字段的文档，您可能只想检索"标题"和"日期"，而无需从大的"_source"字段中提取这些字段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            title: {
              type: 'text',
              store: true
            },
            date: {
              type: 'date',
              store: true
            },
            content: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        title: 'Some short title',
        date: '2015-01-01',
        content: 'A very long content field...'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        stored_fields: [
          'title',
          'date'
        ]
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "store": true __},
          "date": {
            "type": "date",
            "store": true __},
          "content": {
            "type": "text"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "title":   "Some short title",
      "date":    "2015-01-01",
      "content": "A very long content field..."
    }
    
    GET my-index-000001/_search
    {
      "stored_fields": [ "title", "date" ] __}

__

|

存储"标题"和"日期"字段。   ---|---    __

|

此请求将检索"标题"和"日期"字段的值。   ### 以数组形式返回的存储字段

为了保持一致性，存储的字段始终以 _array_ 的形式返回，因为无法知道原始字段值是单个值、多个值还是空数组。

如果需要原始值，则应从"_source"字段中检索它。

[« `similarity`](similarity.md) [`subobjects` »](subobjects.md)
