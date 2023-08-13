

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_ignored` field](mapping-ignored-field.md) [`_index` field »](mapping-
index-field.md)

## '_id'字段

每个文档都有一个唯一标识它的"_id"，该被索引，以便可以使用 GET API 或"ids"查询查找文档。"_id"可以在索引时分配，也可以由Elasticsearch生成唯一的"_id"。此字段在映射中不可配置。

"_id"字段的值可在"术语"、"术语"、"匹配"和"query_string"等查询中访问。

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        text: 'Document with ID 1'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      refresh: true,
      body: {
        text: 'Document with ID 2'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          terms: {
            _id: [
              '1',
              '2'
            ]
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "text": "Document with ID 1"
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "text": "Document with ID 2"
    	}`),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "terms": {
    	      "_id": [
    	        "1",
    	        "2"
    	      ]
    	    }
    	  }
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    # Example documents
    PUT my-index-000001/_doc/1
    {
      "text": "Document with ID 1"
    }
    
    PUT my-index-000001/_doc/2?refresh=true
    {
      "text": "Document with ID 2"
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "terms": {
          "_id": [ "1", "2" ] __}
      }
    }

__

|

对"_id"字段进行查询(另请参阅"ids"查询) ---|--- "_id"字段被限制用于聚合、排序和脚本编写。如果需要对"_id"字段进行排序或聚合，建议将"_id"字段的内容复制到启用了"doc_values"的另一个字段中。

"_id"的大小限制为 512 字节，较大的值将被拒绝。

[« `_ignored` field](mapping-ignored-field.md) [`_index` field »](mapping-
index-field.md)
