

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Geo queries](geo-queries.md)

[« Geo-bounding box query](query-dsl-geo-bounding-box-query.md) [Geo-grid
query »](query-dsl-geo-grid-query.md)

## 地理距离查询

匹配地理点给定距离内的"geo_point"和"geo_shape"值。

####Example

假设以下文档已编制索引：

    
    
    response = client.indices.create(
      index: 'my_locations',
      body: {
        mappings: {
          properties: {
            pin: {
              properties: {
                location: {
                  type: 'geo_point'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my_locations',
      id: 1,
      body: {
        pin: {
          location: {
            lat: 40.12,
            lon: -71.34
          }
        }
      }
    )
    puts response
    
    response = client.indices.create(
      index: 'my_geoshapes',
      body: {
        mappings: {
          properties: {
            pin: {
              properties: {
                location: {
                  type: 'geo_shape'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my_geoshapes',
      id: 1,
      body: {
        pin: {
          location: {
            type: 'polygon',
            coordinates: [
              [
                [
                  13,
                  51.5
                ],
                [
                  15,
                  51.5
                ],
                [
                  15,
                  54
                ],
                [
                  13,
                  54
                ],
                [
                  13,
                  51.5
                ]
              ]
            ]
          }
        }
      }
    )
    puts response
    
    
    PUT /my_locations
    {
      "mappings": {
        "properties": {
          "pin": {
            "properties": {
              "location": {
                "type": "geo_point"
              }
            }
          }
        }
      }
    }
    
    PUT /my_locations/_doc/1
    {
      "pin": {
        "location": {
          "lat": 40.12,
          "lon": -71.34
        }
      }
    }
    
    PUT /my_geoshapes
    {
      "mappings": {
        "properties": {
          "pin": {
            "properties": {
              "location": {
                "type": "geo_shape"
              }
            }
          }
        }
      }
    }
    
    PUT /my_geoshapes/_doc/1
    {
      "pin": {
        "location": {
          "type" : "polygon",
          "coordinates" : [[[13.0 ,51.5], [15.0, 51.5], [15.0, 54.0], [13.0, 54.0], [13.0 ,51.5]]]
        }
      }
    }

使用"geo_distance"过滤器匹配另一个地理点指定距离内的"geo_point"值：

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_distance: {
                distance: '200km',
                "pin.location": {
                  lat: 40,
                  lon: -70
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": "200km",
              "pin.location": {
                "lat": 40,
                "lon": -70
              }
            }
          }
        }
      }
    }

使用相同的过滤器匹配给定距离内的"geo_shape"值：

    
    
    response = client.search(
      index: 'my_geoshapes',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_distance: {
                distance: '200km',
                "pin.location": {
                  lat: 40,
                  lon: -70
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_geoshapes/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": "200km",
              "pin.location": {
                "lat": 40,
                "lon": -70
              }
            }
          }
        }
      }
    }

要同时匹配"geo_point"和"geo_shape"值，请搜索两个索引：

    
    
    response = client.search(
      index: 'my_locations,my_geoshapes',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_distance: {
                distance: '200km',
                "pin.location": {
                  lat: 40,
                  lon: -70
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations,my_geoshapes/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": "200km",
              "pin.location": {
                "lat": 40,
                "lon": -70
              }
            }
          }
        }
      }
    }

#### 接受的格式

与"geo_point"类型可以接受地理点的不同表示形式大致相同，过滤器也可以接受它：

##### Lat lon asproperties

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_distance: {
                distance: '12km',
                "pin.location": {
                  lat: 40,
                  lon: -70
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": "12km",
              "pin.location": {
                "lat": 40,
                "lon": -70
              }
            }
          }
        }
      }
    }

##### Lat lon asarray

格式为"lon， lat]"，请注意，此处的 lon/lat 顺序以符合 [GeoJSON.

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_distance: {
                distance: '12km',
                "pin.location": [
                  -70,
                  40
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": "12km",
              "pin.location": [ -70, 40 ]
            }
          }
        }
      }
    }

##### Lat lon 饰 WKTstring

以已知文本格式。

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_distance: {
                distance: '12km',
                "pin.location": 'POINT (-70 40)'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": "12km",
              "pin.location": "POINT (-70 40)"
            }
          }
        }
      }
    }

#####Geohash

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_distance: {
                distance: '12km',
                "pin.location": 'drm3btev3e86'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_distance": {
              "distance": "12km",
              "pin.location": "drm3btev3e86"
            }
          }
        }
      }
    }

####Options

以下是筛选器上允许的选项：

`distance`

|

以指定位置为中心的圆的半径。落入此圆圈的点被视为匹配。"距离"可以用各种单位指定。请参阅距离单位。   ---|--- "distance_type"

|

如何计算距离。可以是"弧"(默认)或"平面"(更快，但在长距离和靠近极点时不准确)。   "_name"

|

用于标识查询"validation_method"的可选名称字段

|

设置为"IGNORE_MALFORMED"以接受纬度或经度无效的地理点，设置为"COERCE"以另外尝试推断正确的坐标(默认值为"严格")。   #### 多位置每文档编辑

"geo_distance"过滤器可以处理每个文档的多个位置/点。一旦单个位置/点与过滤器匹配，文档将包含在过滤器中。

#### 忽略未映射

当设置为"true"时，"ignore_unmapped"选项将忽略未映射的字段，并且不会匹配此查询的任何文档。这在查询可能具有不同映射的多个索引时非常有用。当设置为"false"(默认值)时，如果未映射字段，查询将引发异常。

[« Geo-bounding box query](query-dsl-geo-bounding-box-query.md) [Geo-grid
query »](query-dsl-geo-grid-query.md)
