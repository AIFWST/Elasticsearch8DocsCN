

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« Specialized queries](specialized-queries.md) [More like this query
»](query-dsl-mlt-query.md)

## 距离要素查询

提高更接近提供的"来源"日期或点的文档的相关度分数。例如，您可以使用此查询为接近特定日期或位置的文档赋予更多权重。

您可以使用"distance_feature"查询来查找离位置最近的邻居。您还可以在"布尔"搜索的"应该"筛选器中使用查询，将提升的相关性分数添加到"布尔"查询的分数中。

### 示例请求

#### 索引设置

要使用"distance_feature"查询，索引必须包含"日期"、"date_nanos"或"geo_point"字段。

若要了解如何为"distance_feature"查询设置索引，请尝试以下示例。

1. 使用以下字段映射创建"项目"索引：

    * `name`, a [`keyword`](keyword.html "Keyword type family") field 
    * `production_date`, a [`date`](date.html "Date field type") field 
    * `location`, a [`geo_point`](geo-point.html "Geopoint field type") field 
    
        response = client.indices.create(
      index: 'items',
      body: {
        mappings: {
          properties: {
            name: {
              type: 'keyword'
            },
            production_date: {
              type: 'date'
            },
            location: {
              type: 'geo_point'
            }
          }
        }
      }
    )
    puts response
    
        PUT /items
    {
      "mappings": {
        "properties": {
          "name": {
            "type": "keyword"
          },
          "production_date": {
            "type": "date"
          },
          "location": {
            "type": "geo_point"
          }
        }
      }
    }

2. 将多个文档索引到此索引。           PUT /items/_doc/1？refresh { "name" ： "chocolate"， "production_date"： "2018-02-01"， "location"： [-71.34， 41.12] } PUT /items/_doc/2？refresh { "name" ： "chocolate"， "production_date"： "2018-01-01"， "location"： [-71.3， 41.15] } PUT /items/_doc/3？refresh { "name" ： "chocolate"， "production_date"： "2017-12-01"， "location"： [-71.3， 41.12] }

#### 示例查询

##### 基于日期提升文档

以下"bool"搜索返回"名称"值为"巧克力"的文档。搜索还使用"distance_feature"查询来提高"production_date"值更接近"现在"的文档的相关性分数。

    
    
    response = client.search(
      index: 'items',
      body: {
        query: {
          bool: {
            must: {
              match: {
                name: 'chocolate'
              }
            },
            should: {
              distance_feature: {
                field: 'production_date',
                pivot: '7d',
                origin: 'now'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /items/_search
    {
      "query": {
        "bool": {
          "must": {
            "match": {
              "name": "chocolate"
            }
          },
          "should": {
            "distance_feature": {
              "field": "production_date",
              "pivot": "7d",
              "origin": "now"
            }
          }
        }
      }
    }

##### 根据位置提升文档

以下"bool"搜索返回"名称"值为"巧克力"的文档。搜索还使用"distance_feature"查询来提高"位置"值接近"[-71.3，41.15]"的文档的相关性分数。

    
    
    response = client.search(
      index: 'items',
      body: {
        query: {
          bool: {
            must: {
              match: {
                name: 'chocolate'
              }
            },
            should: {
              distance_feature: {
                field: 'location',
                pivot: '1000m',
                origin: [
                  -71.3,
                  41.15
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /items/_search
    {
      "query": {
        "bool": {
          "must": {
            "match": {
              "name": "chocolate"
            }
          },
          "should": {
            "distance_feature": {
              "field": "location",
              "pivot": "1000m",
              "origin": [-71.3, 41.15]
            }
          }
        }
      }
    }

### distance_feature"的顶级参数

`field`

    

(必需，字符串)用于计算距离的字段的名称。此字段必须满足以下条件：

* 是"日期"、"date_nanos"或"geo_point"字段 * 具有默认值"true"的"索引"映射参数值 doc_values"true"，这是默认值

`origin`

    

(必需，字符串)用于计算距离的日期或原点。

如果"字段"值是"日期"或"date_nanos"字段，则"原点"值必须是日期。支持DateMath，例如"now-1h"。

如果"字段"值为"geo_point"字段，则"原点"值必须是地理点。

`pivot`

    

(必需，时间单位或距离单位)与相关性分数获得"提升"值一半的"原点"的距离。

如果"字段"值是"日期"或"date_nanos"字段，则"透视"值必须是时间单位，例如"1h"或"10d"。

如果"字段"值为"geo_point"字段，则"枢轴"值必须是距离单位，例如"1km"或"12m"。

`boost`

    

(可选，浮动)浮点数，用于将匹配文档的相关性分数相乘。此值不能为负数。默认为"1.0"。

###Notes

#### "distance_feature"查询如何计算相关性分数

"distance_feature"查询动态计算"origin"值与文档字段值之间的距离。然后，它使用此距离作为一项功能来提高较近文档的相关度分数。

"distance_feature"查询按如下方式计算文档的相关性分数：

    
    
    relevance score = boost * pivot / (pivot + distance)

"距离"是"原点"值与文档字段值之间的绝对差值。

#### 跳过非竞争性命中

与"function_score"查询或其他更改相关性分数的方法不同，当"distance_feature"参数"不**"true"时，""查询会有效地跳过非竞争性匹配track_total_hits。

[« Specialized queries](specialized-queries.md) [More like this query
»](query-dsl-mlt-query.md)
