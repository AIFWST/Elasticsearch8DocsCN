

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Geo queries](geo-queries.md)

[« Geo-grid query](query-dsl-geo-grid-query.md) [Geoshape query »](query-
dsl-geo-shape-query.md)

## 地理多边形查询

### 在 7.12 中已弃用。

改用地理形状，其中多边形在GeoJSON或已知文本(WKT)中定义。

返回仅落在点面内的命中的查询。下面是一个示例：

    
    
    GET /_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_polygon": {
              "person.location": {
                "points": [
                  { "lat": 40, "lon": -70 },
                  { "lat": 30, "lon": -80 },
                  { "lat": 20, "lon": -90 }
                ]
              }
            }
          }
        }
      }
    }

#### 查询选项

选项 |描述 ---|--- '_name'

|

用于标识过滤器"validation_method"的可选名称字段

|

设置为"IGNORE_MALFORMED"以接受纬度或经度无效的地理点，设置为"COERCE"以尝试推断正确的纬度或经度，或设置为"严格"(默认值为"严格")。   #### 允许的格式编辑

##### 拉长

格式为"[lon， lat]"

注意：此处 lon/lat 的顺序必须符合 GeoJSON。

    
    
    GET /_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_polygon": {
              "person.location": {
                "points": [
                  [ -70, 40 ],
                  [ -80, 30 ],
                  [ -90, 20 ]
                ]
              }
            }
          }
        }
      }
    }

##### Lat lon asstring

格式为"纬度，伦敦"。

    
    
    GET /_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_polygon": {
              "person.location": {
                "points": [
                  "40, -70",
                  "30, -80",
                  "20, -90"
                ]
              }
            }
          }
        }
      }
    }

#####Geohash

    
    
    GET /_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_polygon": {
              "person.location": {
                "points": [
                  "drn5x1g8cu2y",
                  "30, -80",
                  "20, -90"
                ]
              }
            }
          }
        }
      }
    }

#### 'geo_point'类型

查询**需要**在相关字段上设置"geo_point"类型。

#### 忽略未映射

当设置为"true"时，"ignore_unmapped"选项将忽略未映射的字段，并且不会匹配此查询的任何文档。这在查询可能具有不同映射的多个索引时非常有用。当设置为"false"(默认值)时，如果未映射字段，查询将引发异常。

[« Geo-grid query](query-dsl-geo-grid-query.md) [Geoshape query »](query-
dsl-geo-shape-query.md)
