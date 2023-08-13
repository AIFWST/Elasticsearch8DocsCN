

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Histogram aggregation](search-aggregations-bucket-histogram-
aggregation.md) [IP range aggregation »](search-aggregations-bucket-iprange-
aggregation.md)

## IP 前缀聚合

根据 IP 地址的网络或子网对文档进行分组的存储桶聚合。IP 地址由两组位组成：表示网络前缀的最有效位和表示主机的最低有效位。

###Example

例如，请考虑以下索引：

    
    
    response = client.indices.create(
      index: 'network-traffic',
      body: {
        mappings: {
          properties: {
            "ipv4": {
              type: 'ip'
            },
            "ipv6": {
              type: 'ip'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'network-traffic',
      refresh: true,
      body: [
        {
          index: {
            _id: 0
          }
        },
        {
          "ipv4": '192.168.1.10',
          "ipv6": '2001:db8:a4f8:112a:6001:0:12:7f10'
        },
        {
          index: {
            _id: 1
          }
        },
        {
          "ipv4": '192.168.1.12',
          "ipv6": '2001:db8:a4f8:112a:6001:0:12:7f12'
        },
        {
          index: {
            _id: 2
          }
        },
        {
          "ipv4": '192.168.1.33',
          "ipv6": '2001:db8:a4f8:112a:6001:0:12:7f33'
        },
        {
          index: {
            _id: 3
          }
        },
        {
          "ipv4": '192.168.1.10',
          "ipv6": '2001:db8:a4f8:112a:6001:0:12:7f10'
        },
        {
          index: {
            _id: 4
          }
        },
        {
          "ipv4": '192.168.2.41',
          "ipv6": '2001:db8:a4f8:112c:6001:0:12:7f41'
        },
        {
          index: {
            _id: 5
          }
        },
        {
          "ipv4": '192.168.2.10',
          "ipv6": '2001:db8:a4f8:112c:6001:0:12:7f10'
        },
        {
          index: {
            _id: 6
          }
        },
        {
          "ipv4": '192.168.2.23',
          "ipv6": '2001:db8:a4f8:112c:6001:0:12:7f23'
        },
        {
          index: {
            _id: 7
          }
        },
        {
          "ipv4": '192.168.3.201',
          "ipv6": '2001:db8:a4f8:114f:6001:0:12:7201'
        },
        {
          index: {
            _id: 8
          }
        },
        {
          "ipv4": '192.168.3.107',
          "ipv6": '2001:db8:a4f8:114f:6001:0:12:7307'
        }
      ]
    )
    puts response
    
    
    PUT network-traffic
    {
        "mappings": {
            "properties": {
                "ipv4": { "type": "ip" },
                "ipv6": { "type": "ip" }
            }
        }
    }
    
    POST /network-traffic/_bulk?refresh
    {"index":{"_id":0}}
    {"ipv4":"192.168.1.10","ipv6":"2001:db8:a4f8:112a:6001:0:12:7f10"}
    {"index":{"_id":1}}
    {"ipv4":"192.168.1.12","ipv6":"2001:db8:a4f8:112a:6001:0:12:7f12"}
    {"index":{"_id":2}}
    { "ipv4":"192.168.1.33","ipv6":"2001:db8:a4f8:112a:6001:0:12:7f33"}
    {"index":{"_id":3}}
    {"ipv4":"192.168.1.10","ipv6":"2001:db8:a4f8:112a:6001:0:12:7f10"}
    {"index":{"_id":4}}
    {"ipv4":"192.168.2.41","ipv6":"2001:db8:a4f8:112c:6001:0:12:7f41"}
    {"index":{"_id":5}}
    {"ipv4":"192.168.2.10","ipv6":"2001:db8:a4f8:112c:6001:0:12:7f10"}
    {"index":{"_id":6}}
    {"ipv4":"192.168.2.23","ipv6":"2001:db8:a4f8:112c:6001:0:12:7f23"}
    {"index":{"_id":7}}
    {"ipv4":"192.168.3.201","ipv6":"2001:db8:a4f8:114f:6001:0:12:7201"}
    {"index":{"_id":8}}
    {"ipv4":"192.168.3.107","ipv6":"2001:db8:a4f8:114f:6001:0:12:7307"}

以下聚合将文档分组到存储桶中。每个存储桶标识不同的子网。子网的计算方法是将前缀长度为"24"的网络掩码应用于"ipv4"字段中的每个 IP 地址：

    
    
    response = client.search(
      index: 'network-traffic',
      body: {
        size: 0,
        aggregations: {
          "ipv4-subnets": {
            ip_prefix: {
              field: 'ipv4',
              prefix_length: 24
            }
          }
        }
      }
    )
    puts response
    
    
    GET /network-traffic/_search
    {
      "size": 0,
      "aggs": {
        "ipv4-subnets": {
          "ip_prefix": {
            "field": "ipv4",
            "prefix_length": 24
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ipv4-subnets": {
          "buckets": [
            {
              "key": "192.168.1.0",
              "is_ipv6": false,
              "doc_count": 4,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            },
            {
              "key": "192.168.2.0",
              "is_ipv6": false,
              "doc_count": 3,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            },
            {
               "key": "192.168.3.0",
               "is_ipv6": false,
               "doc_count": 2,
               "prefix_length": 24,
               "netmask": "255.255.255.0"
            }
          ]
        }
      }
    }

要聚合 IPv6 地址，请将"is_ipv6"设置为"true"。

    
    
    response = client.search(
      index: 'network-traffic',
      body: {
        size: 0,
        aggregations: {
          "ipv6-subnets": {
            ip_prefix: {
              field: 'ipv6',
              prefix_length: 64,
              "is_ipv6": true
            }
          }
        }
      }
    )
    puts response
    
    
    GET /network-traffic/_search
    {
      "size": 0,
      "aggs": {
        "ipv6-subnets": {
          "ip_prefix": {
            "field": "ipv6",
            "prefix_length": 64,
            "is_ipv6": true
          }
        }
      }
    }

如果"is_ipv6"为"true"，则响应不包含每个存储桶的"网络掩码"。

    
    
    {
      ...
    
      "aggregations": {
        "ipv6-subnets": {
          "buckets": [
            {
              "key": "2001:db8:a4f8:112a::",
              "is_ipv6": true,
              "doc_count": 4,
              "prefix_length": 64
            },
            {
              "key": "2001:db8:a4f8:112c::",
              "is_ipv6": true,
              "doc_count": 3,
              "prefix_length": 64
            },
            {
              "key": "2001:db8:a4f8:114f::",
              "is_ipv6": true,
              "doc_count": 2,
              "prefix_length": 64
            }
          ]
        }
      }
    }

###Parameters

`field`

     (Required, string) The document IP address field to aggregate on. The field mapping type must be [`ip`](ip.html "IP field type"). 
`prefix_length`

     (Required, integer) Length of the network prefix. For IPv4 addresses, the accepted range is `[0, 32]`. For IPv6 addresses, the accepted range is `[0, 128]`. 
`is_ipv6`

     (Optional, boolean) Defines whether the prefix applies to IPv6 addresses. Just specifying the `prefix_length` parameter is not enough to know if an IP prefix applies to IPv4 or IPv6 addresses. Defaults to `false`. 
`append_prefix_length`

     (Optional, boolean) Defines whether the prefix length is appended to IP address keys in the response. Defaults to `false`. 
`keyed`

     (Optional, boolean) Defines whether buckets are returned as a hash rather than an array in the response. Defaults to `false`. 
`min_doc_count`

     (Optional, integer) Defines the minimum number of documents for buckets to be included in the response. Defaults to `1`. 

### 响应正文

`key`

     (string) The IPv6 or IPv4 subnet. 
`prefix_length`

     (integer) The length of the prefix used to aggregate the bucket. 
`doc_count`

     (integer) Number of documents matching a specific IP prefix. 
`is_ipv6`

     (boolean) Defines whether the netmask is an IPv6 netmask. 
`netmask`

     (string) The IPv4 netmask. If `is_ipv6` is `true` in the request, this field is missing in the response. 

### 键控响应

将"keyed"标志设置为"true"，将唯一的 IP 地址密钥与每个存储桶相关联，并以哈希而不是数组的形式返回子网。

Example:

    
    
    response = client.search(
      index: 'network-traffic',
      body: {
        size: 0,
        aggregations: {
          "ipv4-subnets": {
            ip_prefix: {
              field: 'ipv4',
              prefix_length: 24,
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    GET /network-traffic/_search
    {
      "size": 0,
      "aggs": {
        "ipv4-subnets": {
          "ip_prefix": {
            "field": "ipv4",
            "prefix_length": 24,
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ipv4-subnets": {
          "buckets": {
            "192.168.1.0": {
              "is_ipv6": false,
              "doc_count": 4,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            },
            "192.168.2.0": {
              "is_ipv6": false,
              "doc_count": 3,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            },
            "192.168.3.0": {
              "is_ipv6": false,
              "doc_count": 2,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            }
          }
        }
      }
    }

### 将前缀长度附加到 IP 地址密钥

将"append_prefix_length"标志设置为"true"，以将 IP 地址密钥与子网的前缀长度连接起来。

Example:

    
    
    response = client.search(
      index: 'network-traffic',
      body: {
        size: 0,
        aggregations: {
          "ipv4-subnets": {
            ip_prefix: {
              field: 'ipv4',
              prefix_length: 24,
              append_prefix_length: true
            }
          }
        }
      }
    )
    puts response
    
    
    GET /network-traffic/_search
    {
      "size": 0,
      "aggs": {
        "ipv4-subnets": {
          "ip_prefix": {
            "field": "ipv4",
            "prefix_length": 24,
            "append_prefix_length": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ipv4-subnets": {
          "buckets": [
            {
              "key": "192.168.1.0/24",
              "is_ipv6": false,
              "doc_count": 4,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            },
            {
              "key": "192.168.2.0/24",
              "is_ipv6": false,
              "doc_count": 3,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            },
            {
              "key": "192.168.3.0/24",
              "is_ipv6": false,
              "doc_count": 2,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            }
          ]
        }
      }
    }

### 最小文档计数

使用 'min_doc_count' 参数仅返回文档数量最少的存储桶。

    
    
    response = client.search(
      index: 'network-traffic',
      body: {
        size: 0,
        aggregations: {
          "ipv4-subnets": {
            ip_prefix: {
              field: 'ipv4',
              prefix_length: 24,
              min_doc_count: 3
            }
          }
        }
      }
    )
    puts response
    
    
    GET /network-traffic/_search
    {
      "size": 0,
      "aggs": {
        "ipv4-subnets": {
          "ip_prefix": {
            "field": "ipv4",
            "prefix_length": 24,
            "min_doc_count": 3
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "ipv4-subnets": {
          "buckets": [
            {
              "key": "192.168.1.0",
              "is_ipv6": false,
              "doc_count": 4,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            },
            {
              "key": "192.168.2.0",
              "is_ipv6": false,
              "doc_count": 3,
              "prefix_length": 24,
              "netmask": "255.255.255.0"
            }
          ]
        }
      }
    }

[« Histogram aggregation](search-aggregations-bucket-histogram-
aggregation.md) [IP range aggregation »](search-aggregations-bucket-iprange-
aggregation.md)
