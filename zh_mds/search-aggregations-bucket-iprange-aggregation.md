

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« IP prefix aggregation](search-aggregations-bucket-ipprefix-
aggregation.md) [Missing aggregation »](search-aggregations-bucket-missing-
aggregation.md)

## IP 范围聚合

就像专用日期范围聚合一样，IP 类型字段也有专用范围聚合：

Example:

    
    
    response = client.search(
      index: 'ip_addresses',
      body: {
        size: 10,
        aggregations: {
          ip_ranges: {
            ip_range: {
              field: 'ip',
              ranges: [
                {
                  to: '10.0.0.5'
                },
                {
                  from: '10.0.0.5'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /ip_addresses/_search
    {
      "size": 10,
      "aggs": {
        "ip_ranges": {
          "ip_range": {
            "field": "ip",
            "ranges": [
              { "to": "10.0.0.5" },
              { "from": "10.0.0.5" }
            ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ip_ranges": {
          "buckets": [
            {
              "key": "*-10.0.0.5",
              "to": "10.0.0.5",
              "doc_count": 10
            },
            {
              "key": "10.0.0.5-*",
              "from": "10.0.0.5",
              "doc_count": 260
            }
          ]
        }
      }
    }

IP 范围也可以定义为 CIDR 掩码：

    
    
    response = client.search(
      index: 'ip_addresses',
      body: {
        size: 0,
        aggregations: {
          ip_ranges: {
            ip_range: {
              field: 'ip',
              ranges: [
                {
                  mask: '10.0.0.0/25'
                },
                {
                  mask: '10.0.0.127/25'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /ip_addresses/_search
    {
      "size": 0,
      "aggs": {
        "ip_ranges": {
          "ip_range": {
            "field": "ip",
            "ranges": [
              { "mask": "10.0.0.0/25" },
              { "mask": "10.0.0.127/25" }
            ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ip_ranges": {
          "buckets": [
            {
              "key": "10.0.0.0/25",
              "from": "10.0.0.0",
              "to": "10.0.0.128",
              "doc_count": 128
            },
            {
              "key": "10.0.0.127/25",
              "from": "10.0.0.0",
              "to": "10.0.0.128",
              "doc_count": 128
            }
          ]
        }
      }
    }

### 键控响应

将"keyed"标志设置为"true"会将一个唯一的字符串键与每个存储桶相关联，并将范围作为哈希而不是数组返回：

    
    
    response = client.search(
      index: 'ip_addresses',
      body: {
        size: 0,
        aggregations: {
          ip_ranges: {
            ip_range: {
              field: 'ip',
              ranges: [
                {
                  to: '10.0.0.5'
                },
                {
                  from: '10.0.0.5'
                }
              ],
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    GET /ip_addresses/_search
    {
      "size": 0,
      "aggs": {
        "ip_ranges": {
          "ip_range": {
            "field": "ip",
            "ranges": [
              { "to": "10.0.0.5" },
              { "from": "10.0.0.5" }
            ],
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ip_ranges": {
          "buckets": {
            "*-10.0.0.5": {
              "to": "10.0.0.5",
              "doc_count": 10
            },
            "10.0.0.5-*": {
              "from": "10.0.0.5",
              "doc_count": 260
            }
          }
        }
      }
    }

还可以为每个范围自定义键：

    
    
    response = client.search(
      index: 'ip_addresses',
      body: {
        size: 0,
        aggregations: {
          ip_ranges: {
            ip_range: {
              field: 'ip',
              ranges: [
                {
                  key: 'infinity',
                  to: '10.0.0.5'
                },
                {
                  key: 'and-beyond',
                  from: '10.0.0.5'
                }
              ],
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    GET /ip_addresses/_search
    {
      "size": 0,
      "aggs": {
        "ip_ranges": {
          "ip_range": {
            "field": "ip",
            "ranges": [
              { "key": "infinity", "to": "10.0.0.5" },
              { "key": "and-beyond", "from": "10.0.0.5" }
            ],
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ip_ranges": {
          "buckets": {
            "infinity": {
              "to": "10.0.0.5",
              "doc_count": 10
            },
            "and-beyond": {
              "from": "10.0.0.5",
              "doc_count": 260
            }
          }
        }
      }
    }

[« IP prefix aggregation](search-aggregations-bucket-ipprefix-
aggregation.md) [Missing aggregation »](search-aggregations-bucket-missing-
aggregation.md)
