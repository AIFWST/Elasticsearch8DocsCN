

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Histogram field type](histogram.md) [Join field type »](parent-join.md)

## IP 字段类型

"ip"字段可以索引/存储IPv4或IPv6地址。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            ip_addr: {
              type: 'ip'
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
        ip_addr: '192.168.1.1'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            ip_addr: '192.168.0.0/16'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "ip_addr": {
            "type": "ip"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "ip_addr": "192.168.1.1"
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "term": {
          "ip_addr": "192.168.0.0/16"
        }
      }
    }

您还可以使用 ip_range 数据类型将 ip 范围存储在单个字段中。

### "ip"字段的参数

"ip"字段接受以下参数：

"doc_values"

     Should the field be stored on disk in a column-stride fashion, so that it can later be used for sorting, aggregations, or scripting? Accepts `true` (default) or `false`. 
[`ignore_malformed`](ignore-malformed.html "ignore_malformed")

     If `true`, malformed IP addresses are ignored. If `false` (default), malformed IP addresses throw an exception and reject the whole document. Note that this cannot be set if the `script` parameter is used. 
[`index`](mapping-index.html "index")

     Should the field be quickly searchable? Accepts `true` (default) and `false`. Fields that only have [`doc_values`](doc-values.html "doc_values") enabled can still be queried using term or range-based queries, albeit slower. 
[`null_value`](null-value.html "null_value")

     Accepts an IPv4 or IPv6 value which is substituted for any explicit `null` values. Defaults to `null`, which means the field is treated as missing. Note that this cannot be set if the `script` parameter is used. 
`on_script_error`

     Defines what to do if the script defined by the `script` parameter throws an error at indexing time. Accepts `reject` (default), which will cause the entire document to be rejected, and `ignore`, which will register the field in the document's [`_ignored`](mapping-ignored-field.html "_ignored field") metadata field and continue indexing. This parameter can only be set if the `script` field is also set. 
`script`

     If this parameter is set, then the field will index values generated by this script, rather than reading the values directly from the source. If a value is set for this field on the input document, then the document will be rejected with an error. Scripts are in the same format as their [runtime equivalent](runtime-mapping-fields.html "Map a runtime field"), and should emit strings containing IPv4 or IPv6 formatted addresses. 
[`store`](mapping-store.html "store")

     Whether the field value should be stored and retrievable separately from the [`_source`](mapping-source-field.html "_source field") field. Accepts `true` or `false` (default). 
`time_series_dimension`

    

(可选，布尔值)

将字段标记为时序维度。默认为"假"。

"index.mapping.dimension_fields.limit"索引设置可限制索引中的维度数。

维度字段具有以下约束：

* "doc_values"和"索引"映射参数必须为"true"。  * 字段值不能是数组或多值。

### 查询"ip"字段

查询 IP 地址的最常见方法是使用 CIDR 表示法："[ip_address]/[prefix_length]"。例如：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            ip_addr: '192.168.0.0/16'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "term": {
          "ip_addr": "192.168.0.0/16"
        }
      }
    }

or

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            ip_addr: '2001:db8::/48'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "term": {
          "ip_addr": "2001:db8::/48"
        }
      }
    }

另请注意，冒号是"query_string"查询的特殊字符，因此需要对 ipv6 地址进行转义。最简单的方法是在搜索值周围加上引号：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          query_string: {
            query: 'ip_addr:"2001:db8::/48"'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "query_string" : {
          "query": "ip_addr:\"2001:db8::/48\""
        }
      }
    }

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"ip"字段在其默认配置中支持合成的"_source"。合成"_source"不能与"copy_to"一起使用，也不能禁用"doc_values"。

合成源始终对"ip"字段进行排序并删除重复项。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            ip: {
              type: 'ip'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        ip: [
          '192.168.0.1',
          '192.168.0.1',
          '10.10.12.123',
          '2001:db8::1:0:0:1',
          '::afff:4567:890a'
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "ip": { "type": "ip" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "ip": ["192.168.0.1", "192.168.0.1", "10.10.12.123",
             "2001:db8::1:0:0:1", "::afff:4567:890a"]
    }

将成为：

    
    
    {
      "ip": ["::afff:4567:890a", "10.10.12.123", "192.168.0.1", "2001:db8::1:0:0:1"]
    }

IPv4 地址的排序就像它们是前缀为 '：：ffff：0：0：0/96' 的 IPv6 地址，如指定的 byrfc6144 一样。

[« Histogram field type](histogram.md) [Join field type »](parent-join.md)
