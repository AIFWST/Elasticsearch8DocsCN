

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Aggregate metric field type](aggregate-metric-double.md) [Arrays
»](array.md)

## 别名字段类型

"别名"映射定义索引中字段的备用名称。别名可用于代替搜索请求中的目标字段，以及选定的其他 API，如字段功能。

    
    
    response = client.indices.create(
      index: 'trips',
      body: {
        mappings: {
          properties: {
            distance: {
              type: 'long'
            },
            route_length_miles: {
              type: 'alias',
              path: 'distance'
            },
            transit_mode: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    response = client.search(
      body: {
        query: {
          range: {
            route_length_miles: {
              gte: 39
            }
          }
        }
      }
    )
    puts response
    
    
    PUT trips
    {
      "mappings": {
        "properties": {
          "distance": {
            "type": "long"
          },
          "route_length_miles": {
            "type": "alias",
            "path": "distance" __},
          "transit_mode": {
            "type": "keyword"
          }
        }
      }
    }
    
    GET _search
    {
      "query": {
        "range" : {
          "route_length_miles" : {
            "gte" : 39
          }
        }
      }
    }

__

|

目标字段的路径。请注意，这必须是完整路径，包括任何父对象(例如'object1.object2.field')。   ---|--- 搜索请求的几乎所有组件都接受字段别名。特别是，别名可用于查询、聚合和排序字段，以及请求"docvalue_fields"、"stored_fields"、建议和突出显示时。脚本在访问字段值时还支持别名。有关例外情况，请参阅有关不受支持的 API 的部分。

在搜索请求的某些部分以及请求字段功能时，可以提供字段通配符模式。在这些情况下，通配符模式除了匹配具体字段外，还将匹配字段别名：

    
    
    response = client.field_caps(
      index: 'trips',
      fields: 'route_*,transit_mode'
    )
    puts response
    
    
    GET trips/_field_caps?fields=route_*,transit_mode

### 别名目标

别名的目标有一些限制：

* 目标必须是具体字段，而不是对象或其他字段别名。  * 创建别名时目标字段必须存在。  * 如果定义了嵌套对象，则字段别名必须与其目标具有相同的嵌套范围。

此外，字段别名只能有一个目标。这意味着不能使用字段别名在单个子句中查询多个目标字段。

可以通过映射更新更改别名以引用新目标。已知的限制是，如果任何存储的渗滤器查询包含字段别名，它们仍将引用其原始目标。更多信息可以在渗滤器文档中找到。

### 不支持的接口

不支持写入字段别名：尝试在索引或更新请求中使用别名将导致失败。同样，别名不能用作"copy_to"的目标或多字段。

由于文档源中不存在别名，因此在执行源筛选时无法使用别名。例如，以下请求将返回"_source"的空结果：

    
    
    response = client.search(
      body: {
        query: {
          match_all: {}
        },
        _source: 'route_length_miles'
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match_all": {}
      },
      "_source": "route_length_miles"
    }

目前，只有搜索和字段功能 API 将接受和解析字段别名。其他接受字段名称的 API(例如术语向量)不能与字段别名一起使用。

最后，某些查询(如"terms"、"geo_shape"和"more_like_this")允许从索引文档中获取查询信息。由于提取文档时不支持字段别名，因此指定查找路径的查询部分不能通过字段的别名引用字段。

[« Aggregate metric field type](aggregate-metric-double.md) [Arrays
»](array.md)
