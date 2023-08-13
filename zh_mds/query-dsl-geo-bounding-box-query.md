

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Geo queries](geo-queries.md)

[« Geo queries](geo-queries.md) [Geo-distance query »](query-dsl-geo-
distance-query.md)

## 地理边界框查询

匹配与大量框相交的"geo_point"和"geo_shape"值。

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

使用"geo_bounding_box"筛选器匹配与无限框相交的"geo_point"值。要定义该框，请为两个相对的拐角提供地理点值。

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_bounding_box: {
                "pin.location": {
                  top_left: {
                    lat: 40.73,
                    lon: -74.1
                  },
                  bottom_right: {
                    lat: 40.01,
                    lon: -71.12
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_bounding_box": {
              "pin.location": {
                "top_left": {
                  "lat": 40.73,
                  "lon": -74.1
                },
                "bottom_right": {
                  "lat": 40.01,
                  "lon": -71.12
                }
              }
            }
          }
        }
      }
    }

使用相同的过滤器匹配与边界框相交的"geo_shape"值：

    
    
    response = client.search(
      index: 'my_geoshapes',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_bounding_box: {
                "pin.location": {
                  top_left: {
                    lat: 40.73,
                    lon: -74.1
                  },
                  bottom_right: {
                    lat: 40.01,
                    lon: -71.12
                  }
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
            "geo_bounding_box": {
              "pin.location": {
                "top_left": {
                  "lat": 40.73,
                  "lon": -74.1
                },
                "bottom_right": {
                  "lat": 40.01,
                  "lon": -71.12
                }
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
              geo_bounding_box: {
                "pin.location": {
                  top_left: {
                    lat: 40.73,
                    lon: -74.1
                  },
                  bottom_right: {
                    lat: 40.01,
                    lon: -71.12
                  }
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
            "geo_bounding_box": {
              "pin.location": {
                "top_left": {
                  "lat": 40.73,
                  "lon": -74.1
                },
                "bottom_right": {
                  "lat": 40.01,
                  "lon": -71.12
                }
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

设置为"IGNORE_MALFORMED"以接受纬度或经度无效的地理点，设置为"COERCE"以尝试推断正确的纬度或经度。(默认值为"严格")。   #### 接受格式编辑

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
              geo_bounding_box: {
                "pin.location": {
                  top_left: {
                    lat: 40.73,
                    lon: -74.1
                  },
                  bottom_right: {
                    lat: 40.01,
                    lon: -71.12
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_bounding_box": {
              "pin.location": {
                "top_left": {
                  "lat": 40.73,
                  "lon": -74.1
                },
                "bottom_right": {
                  "lat": 40.01,
                  "lon": -71.12
                }
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
              geo_bounding_box: {
                "pin.location": {
                  top_left: [
                    -74.1,
                    40.73
                  ],
                  bottom_right: [
                    -71.12,
                    40.01
                  ]
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_bounding_box": {
              "pin.location": {
                "top_left": [ -74.1, 40.73 ],
                "bottom_right": [ -71.12, 40.01 ]
              }
            }
          }
        }
      }
    }

##### Lat lon asstring

格式为"纬度，伦敦"。

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_bounding_box: {
                "pin.location": {
                  top_left: 'POINT (-74.1 40.73)',
                  bottom_right: 'POINT (-71.12 40.01)'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_bounding_box": {
              "pin.location": {
                "top_left": "POINT (-74.1 40.73)",
                "bottom_right": "POINT (-71.12 40.01)"
              }
            }
          }
        }
      }
    }

##### 边界框作为已知文本 (WKT)

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_bounding_box: {
                "pin.location": {
                  wkt: 'BBOX (-74.1, -71.12, 40.73, 40.01)'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_bounding_box": {
              "pin.location": {
                "wkt": "BBOX (-74.1, -71.12, 40.73, 40.01)"
              }
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
              geo_bounding_box: {
                "pin.location": {
                  top_left: 'dr5r9ydj2y73',
                  bottom_right: 'drj7teegpus6'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_bounding_box": {
              "pin.location": {
                "top_left": "dr5r9ydj2y73",
                "bottom_right": "drj7teegpus6"
              }
            }
          }
        }
      }
    }

当使用地理哈希指定边界框边缘的边界时，地理哈希被视为矩形。边界框的定义是，其左上角对应于 'top_left' 参数中指定的地理哈希的左上角，其右下角定义为 'bottom_right' 参数中指定的地理哈希的右下角。

为了指定一个与地理哈希的整个区域匹配的边界框可以在"top_left"和"bottom_right"参数中指定地理哈希：

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          geo_bounding_box: {
            "pin.location": {
              top_left: 'dr',
              bottom_right: 'dr'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "geo_bounding_box": {
          "pin.location": {
            "top_left": "dr",
            "bottom_right": "dr"
          }
        }
      }
    }

在此示例中，geohash 'dr' 将生成边界框查询，其中左上角为 '45.0，-78.75'，右下角为 '39.375，-67.5'。

####Vertices

边界框的顶点可以通过"top_left"和"bottom_right"或"top_right"和"bottom_left"参数进行设置。可以使用简单的名称"top"、"left"、"bottom"和"right"来分别设置值，而不是成对设置值。

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              geo_bounding_box: {
                "pin.location": {
                  top: 40.73,
                  left: -74.1,
                  bottom: 40.01,
                  right: -71.12
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my_locations/_search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "geo_bounding_box": {
              "pin.location": {
                "top": 40.73,
                "left": -74.1,
                "bottom": 40.01,
                "right": -71.12
              }
            }
          }
        }
      }
    }

#### 每个文档的多位置

过滤器可以处理每个文档的多个位置/点。一旦单个位置/点与过滤器匹配，文档将包含在过滤器中

#### 忽略未映射

当设置为"true"时，"ignore_unmapped"选项将忽略未映射的字段，并且不会匹配此查询的任何文档。这在查询可能具有不同映射的多个索引时非常有用。当设置为"false"(默认值)时，如果未映射字段，查询将引发异常。

#### 精度注意事项

地理点的精度有限，在索引时间内始终向下舍入。在查询期间，边界框的上边界向下舍入，而下边界向上舍入。因此，由于舍入误差，下边界(边界框的底部和左边缘)上的点可能不会进入边界框。查询可能会选择与上限(上边缘和右边缘)相邻的相同时间点，即使它们位于边缘之外。纬度上的舍入误差应小于 4.20e-8 度，经度上的舍入误差应小于 8.39e-8 度，这意味着即使在赤道上也小于 1 厘米的误差。

由于舍入，地理形状的精度也有限。沿边界框的底部和左侧边缘的地理形状边缘可能与"geo_bounding_box"查询不匹配。略高于框顶部和右侧边缘的地理形状边缘可能仍与查询匹配。

[« Geo queries](geo-queries.md) [Geo-distance query »](query-dsl-geo-
distance-query.md)
