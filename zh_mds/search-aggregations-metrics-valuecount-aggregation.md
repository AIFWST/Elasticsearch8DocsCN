

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Top metrics aggregation](search-aggregations-metrics-top-metrics.md)
[Weighted avg aggregation »](search-aggregations-metrics-weight-avg-
aggregation.md)

## 值计数聚合

一种"单值"指标聚合，用于计算从聚合文档中提取的值数。这些值可以从文档中的特定字段中提取，也可以由提供的脚本生成。通常，此聚合器将与其他单值聚合结合使用。例如，在计算"avg"时，人们可能对计算平均值的值数量感兴趣。

"value_count"不会删除重复值，因此即使字段有重复项，每个值也会单独计数。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          types_count: {
            value_count: {
              field: 'type'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "types_count": {
    	      "value_count": {
    	        "field": "type"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs" : {
        "types_count" : { "value_count" : { "field" : "type" } }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "types_count": {
          "value": 7
        }
      }
    }

聚合的名称(上面的"types_count")也用作可以从返回的响应中检索聚合结果的键。

###Script

如果需要计算比单个字段中的值更复杂的内容，则应在运行时字段上运行聚合。

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        runtime_mappings: {
          tags: {
            type: 'keyword',
            script: "\n        emit(doc['type'].value);\n        if (doc['promoted'].value) {\n          emit('hot');\n        }\n      "
          }
        },
        aggregations: {
          tags_count: {
            value_count: {
              field: 'tags'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "size": 0,
      "runtime_mappings": {
        "tags": {
          "type": "keyword",
          "script": """
            emit(doc['type'].value);
            if (doc['promoted'].value) {
              emit('hot');
            }
          """
        }
      },
      "aggs": {
        "tags_count": {
          "value_count": {
            "field": "tags"
          }
        }
      }
    }

### 直方图字段

当在直方图字段上计算"value_count"聚合时，聚合的结果是直方图的"counts"数组中所有数字的总和。

例如，对于以下索引，该索引存储了预聚合的直方图以及不同网络的延迟指标：

    
    
    response = client.index(
      index: 'metrics_index',
      id: 1,
      body: {
        "network.name": 'net-1',
        latency_histo: {
          values: [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5
          ],
          counts: [
            3,
            7,
            23,
            12,
            6
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'metrics_index',
      id: 2,
      body: {
        "network.name": 'net-2',
        latency_histo: {
          values: [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5
          ],
          counts: [
            8,
            17,
            8,
            7,
            6
          ]
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'metrics_index',
      size: 0,
      body: {
        aggregations: {
          total_requests: {
            value_count: {
              field: 'latency_histo'
            }
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"metrics_index",
    		strings.NewReader(`{
    	  "network.name": "net-1",
    	  "latency_histo": {
    	    "values": [
    	      0.1,
    	      0.2,
    	      0.3,
    	      0.4,
    	      0.5
    	    ],
    	    "counts": [
    	      3,
    	      7,
    	      23,
    	      12,
    	      6
    	    ]
    	  }
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"metrics_index",
    		strings.NewReader(`{
    	  "network.name": "net-2",
    	  "latency_histo": {
    	    "values": [
    	      0.1,
    	      0.2,
    	      0.3,
    	      0.4,
    	      0.5
    	    ],
    	    "counts": [
    	      8,
    	      17,
    	      8,
    	      7,
    	      6
    	    ]
    	  }
    	}`),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("metrics_index"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "total_requests": {
    	      "value_count": {
    	        "field": "latency_histo"
    	      }
    	    }
    	  }
    	}`)),
    		es.Search.WithSize(0),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT metrics_index/_doc/1
    {
      "network.name" : "net-1",
      "latency_histo" : {
          "values" : [0.1, 0.2, 0.3, 0.4, 0.5],
          "counts" : [3, 7, 23, 12, 6] __}
    }
    
    PUT metrics_index/_doc/2
    {
      "network.name" : "net-2",
      "latency_histo" : {
          "values" :  [0.1, 0.2, 0.3, 0.4, 0.5],
          "counts" : [8, 17, 8, 7, 6] __}
    }
    
    POST /metrics_index/_search?size=0
    {
      "aggs": {
        "total_requests": {
          "value_count": { "field": "latency_histo" }
        }
      }
    }

对于每个直方图字段，"value_count"聚合将"counts"数组 <1> 中的所有数字相加。最终，它将添加所有直方图的所有值并返回以下结果：

    
    
    {
      ...
      "aggregations": {
        "total_requests": {
          "value": 97
        }
      }
    }

[« Top metrics aggregation](search-aggregations-metrics-top-metrics.md)
[Weighted avg aggregation »](search-aggregations-metrics-weight-avg-
aggregation.md)
