

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Variable width histogram aggregation](search-aggregations-bucket-
variablewidthhistogram-aggregation.md) [Metrics aggregations »](search-
aggregations-metrics.md)

## 分桶范围字段的微妙之处

### 文档按它们放入的每个存储桶进行计数

由于一个范围表示多个值，因此对范围字段运行存储桶聚合可能会导致同一文档登陆多个存储桶。这可能会导致令人惊讶的行为，例如存储桶计数的总和高于匹配的文档数。例如，请考虑以下索引：

    
    
    response = client.indices.create(
      index: 'range_index',
      body: {
        settings: {
          number_of_shards: 2
        },
        mappings: {
          properties: {
            expected_attendees: {
              type: 'integer_range'
            },
            time_frame: {
              type: 'date_range',
              format: 'yyyy-MM-dd||epoch_millis'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'range_index',
      id: 1,
      refresh: true,
      body: {
        expected_attendees: {
          gte: 10,
          lte: 20
        },
        time_frame: {
          gte: '2019-10-28',
          lte: '2019-11-04'
        }
      }
    )
    puts response
    
    
    PUT range_index
    {
      "settings": {
        "number_of_shards": 2
      },
      "mappings": {
        "properties": {
          "expected_attendees": {
            "type": "integer_range"
          },
          "time_frame": {
            "type": "date_range",
            "format": "yyyy-MM-dd||epoch_millis"
          }
        }
      }
    }
    
    PUT range_index/_doc/1?refresh
    {
      "expected_attendees" : {
        "gte" : 10,
        "lte" : 20
      },
      "time_frame" : {
        "gte" : "2019-10-28",
        "lte" : "2019-11-04"
      }
    }

范围比以下聚合中的间隔更宽，因此文档将登陆多个存储桶。

    
    
    response = client.search(
      index: 'range_index',
      size: 0,
      body: {
        aggregations: {
          range_histo: {
            histogram: {
              field: 'expected_attendees',
              interval: 5
            }
          }
        }
      }
    )
    puts response
    
    
    POST /range_index/_search?size=0
    {
      "aggs": {
        "range_histo": {
          "histogram": {
            "field": "expected_attendees",
            "interval": 5
          }
        }
      }
    }

由于间隔为"5"(默认情况下偏移量为"0")，因此我们期望存储桶为"10"、"15"和"20"。我们的范围文档将属于所有这三个类别。

    
    
    {
      ...
      "aggregations" : {
        "range_histo" : {
          "buckets" : [
            {
              "key" : 10.0,
              "doc_count" : 1
            },
            {
              "key" : 15.0,
              "doc_count" : 1
            },
            {
              "key" : 20.0,
              "doc_count" : 1
            }
          ]
        }
      }
    }

文档不能部分存在于存储桶中;例如，上述文档不能在上述三个存储桶中分别计为三分之一。在此示例中，由于文档的范围位于多个存储桶中，因此该文档的完整值也将计入每个存储桶的任何子聚合中。

### 查询边界不是聚合筛选器

当使用查询筛选要聚合的字段时，可能会出现另一种意外行为。在这种情况下，文档可以与查询匹配，但仍具有查询之外的范围的一个或两个终结点。请考虑上述文档的以下聚合：

    
    
    response = client.search(
      index: 'range_index',
      size: 0,
      body: {
        query: {
          range: {
            time_frame: {
              gte: '2019-11-01',
              format: 'yyyy-MM-dd'
            }
          }
        },
        aggregations: {
          november_data: {
            date_histogram: {
              field: 'time_frame',
              calendar_interval: 'day',
              format: 'yyyy-MM-dd'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /range_index/_search?size=0
    {
      "query": {
        "range": {
          "time_frame": {
            "gte": "2019-11-01",
            "format": "yyyy-MM-dd"
          }
        }
      },
      "aggs": {
        "november_data": {
          "date_histogram": {
            "field": "time_frame",
            "calendar_interval": "day",
            "format": "yyyy-MM-dd"
          }
        }
      }
    }

即使查询仅考虑 11 月的天数，聚合也会生成 8 个存储桶(10 月为 4 个，11 月为 4 个)，因为聚合是根据所有匹配文档的范围计算的。

    
    
    {
      ...
      "aggregations" : {
        "november_data" : {
          "buckets" : [
                  {
              "key_as_string" : "2019-10-28",
              "key" : 1572220800000,
              "doc_count" : 1
            },
            {
              "key_as_string" : "2019-10-29",
              "key" : 1572307200000,
              "doc_count" : 1
            },
            {
              "key_as_string" : "2019-10-30",
              "key" : 1572393600000,
              "doc_count" : 1
            },
            {
              "key_as_string" : "2019-10-31",
              "key" : 1572480000000,
              "doc_count" : 1
            },
            {
              "key_as_string" : "2019-11-01",
              "key" : 1572566400000,
              "doc_count" : 1
            },
            {
              "key_as_string" : "2019-11-02",
              "key" : 1572652800000,
              "doc_count" : 1
            },
            {
              "key_as_string" : "2019-11-03",
              "key" : 1572739200000,
              "doc_count" : 1
            },
            {
              "key_as_string" : "2019-11-04",
              "key" : 1572825600000,
              "doc_count" : 1
            }
          ]
        }
      }
    }

根据用例，"CONTAINS"查询可以将文档限制为仅那些完全属于查询范围内的文档。在此示例中，将不包括 onedocument，聚合将为空。在聚合后过滤存储桶也是一种选择，适用于应计算文档但可以安全地忽略越界数据的使用案例。

[« Variable width histogram aggregation](search-aggregations-bucket-
variablewidthhistogram-aggregation.md) [Metrics aggregations »](search-
aggregations-metrics.md)
