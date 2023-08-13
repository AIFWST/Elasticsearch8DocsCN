

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Geo queries](geo-queries.md)

[« Geo-polygon query](query-dsl-geo-polygon-query.md) [Shape queries
»](shape-queries.md)

## 地理形状查询

筛选使用"geo_shape"或"geo_point"类型编制索引的文档。

"geo_shape"查询使用与"geo_shape"或"geo_point"映射相同的索引来查找具有与查询形状相关的形状的文档，使用指定的空间关系：相交、包含、内部或不相交。

查询支持两种定义查询形状的方法，一种是通过提供整体形状定义，另一种是通过引用在另一个索引中预先编制索引的形状的名称。下面通过示例定义了这两种格式。

### 内联形状定义

与"geo_point"类型类似，"geo_shape"查询使用 GeoJSON 来表示形状。

给定以下索引，其中位置为"geo_shape"字段：

    
    
    response = client.indices.create(
      index: 'example',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'geo_shape'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'example',
      refresh: true,
      body: {
        name: 'Wind & Wetter, Berlin, Germany',
        location: {
          type: 'point',
          coordinates: [
            13.400544,
            52.530286
          ]
        }
      }
    )
    puts response
    
    
    PUT /example
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_shape"
          }
        }
      }
    }
    
    POST /example/_doc?refresh
    {
      "name": "Wind & Wetter, Berlin, Germany",
      "location": {
        "type": "point",
        "coordinates": [ 13.400544, 52.530286 ]
      }
    }

以下查询将使用Elasticsearch的'envelope'GeoJSON扩展找到要点：

    
    
    response = client.search(
      index: 'example',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_shape: {
                location: {
                  shape: {
                    type: 'envelope',
                    coordinates: [
                      [
                        13,
                        53
                      ],
                      [
                        14,
                        52
                      ]
                    ]
                  },
                  relation: 'within'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /example/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_shape": {
              "location": {
                "shape": {
                  "type": "envelope",
                  "coordinates": [ [ 13.0, 53.0 ], [ 14.0, 52.0 ] ]
                },
                "relation": "within"
              }
            }
          }
        }
      }
    }

同样，可以在"geo_point"字段中查询上述查询。

    
    
    PUT /example_points
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_point"
          }
        }
      }
    }
    
    PUT /example_points/_doc/1?refresh
    {
      "name": "Wind & Wetter, Berlin, Germany",
      "location": [13.400544, 52.530286]
    }

使用相同的查询，将返回具有匹配"geo_point"字段的文档。

    
    
    response = client.search(
      index: 'example_points',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_shape: {
                location: {
                  shape: {
                    type: 'envelope',
                    coordinates: [
                      [
                        13,
                        53
                      ],
                      [
                        14,
                        52
                      ]
                    ]
                  },
                  relation: 'intersects'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /example_points/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_shape": {
              "location": {
                "shape": {
                  "type": "envelope",
                  "coordinates": [ [ 13.0, 53.0 ], [ 14.0, 52.0 ] ]
                },
                "relation": "intersects"
              }
            }
          }
        }
      }
    }
    
    
    {
      "took" : 17,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "example_points",
            "_id" : "1",
            "_score" : 1.0,
            "_source" : {
              "name": "Wind & Wetter, Berlin, Germany",
              "location": [13.400544, 52.530286]
            }
          }
        ]
      }
    }

### 预索引形状

该查询还支持使用已在另一个索引中编制索引的形状。当您有一个预定义的形状列表并且您希望使用逻辑名称(例如 _New Zealand_ )引用该列表而不必每次都提供坐标时，这特别有用。在这种情况下，只需要提供：

* 'id' \- 包含预索引形状的文档的 ID。  * 'index' \- 预索引形状所在的索引的名称。默认为 _shapes_。  * 'path' \- 指定为包含预索引形状的路径的字段。默认为 _shape_。  * "路由" \- 形状文档的路由(如果需要)。

以下是将筛选器与预先编制索引的形状一起使用的示例：

    
    
    response = client.indices.create(
      index: 'shapes',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'geo_shape'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'shapes',
      id: 'deu',
      body: {
        location: {
          type: 'envelope',
          coordinates: [
            [
              13,
              53
            ],
            [
              14,
              52
            ]
          ]
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'example',
      body: {
        query: {
          bool: {
            filter: {
              geo_shape: {
                location: {
                  indexed_shape: {
                    index: 'shapes',
                    id: 'deu',
                    path: 'location'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /shapes
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_shape"
          }
        }
      }
    }
    
    PUT /shapes/_doc/deu
    {
      "location": {
        "type": "envelope",
        "coordinates" : [[13.0, 53.0], [14.0, 52.0]]
      }
    }
    
    GET /example/_search
    {
      "query": {
        "bool": {
          "filter": {
            "geo_shape": {
              "location": {
                "indexed_shape": {
                  "index": "shapes",
                  "id": "deu",
                  "path": "location"
                }
              }
            }
          }
        }
      }
    }

### 空间关系

以下是搜索地理字段时可用的空间关系运算符的完整列表：

* "INTERSECTS" \-(默认)返回其"geo_shape"或"geo_point"字段与查询几何相交的所有文档。  * "DISJOINT" \- 返回其"geo_shape"或"geo_point"字段与查询几何没有任何共同点的所有文档。  * "WITHIN" \- 返回其"geo_shape"或"geo_point"字段在查询几何中的所有文档。不支持线几何。  * "包含" \- 返回其"geo_shape"或"geo_point"字段包含查询几何的所有文档。

#### 忽略未映射

当设置为"true"时，"ignore_unmapped"选项将忽略未映射的字段，并且不会匹配此查询的任何文档。这在查询可能具有不同映射的多个索引时非常有用。当设置为"false"(默认值)时，如果未映射字段，查询将引发异常。

###Notes

* 当数据在"geo_shape"字段中作为形状数组编制索引时，数组将被视为一个形状。因此，以下请求是等效的。

    
    
    response = client.index(
      index: 'test',
      id: 1,
      body: {
        location: [
          {
            coordinates: [
              46.25,
              20.14
            ],
            type: 'point'
          },
          {
            coordinates: [
              47.49,
              19.04
            ],
            type: 'point'
          }
        ]
      }
    )
    puts response
    
    
    PUT /test/_doc/1
    {
      "location": [
        {
          "coordinates": [46.25,20.14],
          "type": "point"
        },
        {
          "coordinates": [47.49,19.04],
          "type": "point"
        }
      ]
    }
    
    
    response = client.index(
      index: 'test',
      id: 1,
      body: {
        location: {
          coordinates: [
            [
              46.25,
              20.14
            ],
            [
              47.49,
              19.04
            ]
          ],
          type: 'multipoint'
        }
      }
    )
    puts response
    
    
    PUT /test/_doc/1
    {
      "location":
        {
          "coordinates": [[46.25,20.14],[47.49,19.04]],
          "type": "multipoint"
        }
    }

* "geo_shape"查询假定"geo_shape"字段使用默认的"方向""RIGHT"(逆时针)。请参阅多边形方向。

[« Geo-polygon query](query-dsl-geo-polygon-query.md) [Shape queries
»](shape-queries.md)
