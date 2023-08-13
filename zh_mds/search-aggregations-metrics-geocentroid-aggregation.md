

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Geo-bounds aggregation](search-aggregations-metrics-geobounds-
aggregation.md) [Geo-line aggregation »](search-aggregations-metrics-geo-
line.md)

## 地理质心聚合

一种指标聚合，用于根据地理字段的所有坐标值计算加权质心。

Example:

    
    
    response = client.indices.create(
      index: 'museums',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'geo_point'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'museums',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          location: 'POINT (4.912350 52.374081)',
          city: 'Amsterdam',
          name: 'NEMO Science Museum'
        },
        {
          index: {
            _id: 2
          }
        },
        {
          location: 'POINT (4.901618 52.369219)',
          city: 'Amsterdam',
          name: 'Museum Het Rembrandthuis'
        },
        {
          index: {
            _id: 3
          }
        },
        {
          location: 'POINT (4.914722 52.371667)',
          city: 'Amsterdam',
          name: 'Nederlands Scheepvaartmuseum'
        },
        {
          index: {
            _id: 4
          }
        },
        {
          location: 'POINT (4.405200 51.222900)',
          city: 'Antwerp',
          name: 'Letterenhuis'
        },
        {
          index: {
            _id: 5
          }
        },
        {
          location: 'POINT (2.336389 48.861111)',
          city: 'Paris',
          name: 'Musée du Louvre'
        },
        {
          index: {
            _id: 6
          }
        },
        {
          location: 'POINT (2.327000 48.860000)',
          city: 'Paris',
          name: "Musée d'Orsay"
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          centroid: {
            geo_centroid: {
              field: 'location'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /museums
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_point"
          }
        }
      }
    }
    
    POST /museums/_bulk?refresh
    {"index":{"_id":1}}
    {"location": "POINT (4.912350 52.374081)", "city": "Amsterdam", "name": "NEMO Science Museum"}
    {"index":{"_id":2}}
    {"location": "POINT (4.901618 52.369219)", "city": "Amsterdam", "name": "Museum Het Rembrandthuis"}
    {"index":{"_id":3}}
    {"location": "POINT (4.914722 52.371667)", "city": "Amsterdam", "name": "Nederlands Scheepvaartmuseum"}
    {"index":{"_id":4}}
    {"location": "POINT (4.405200 51.222900)", "city": "Antwerp", "name": "Letterenhuis"}
    {"index":{"_id":5}}
    {"location": "POINT (2.336389 48.861111)", "city": "Paris", "name": "Musée du Louvre"}
    {"index":{"_id":6}}
    {"location": "POINT (2.327000 48.860000)", "city": "Paris", "name": "Musée d'Orsay"}
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "centroid": {
          "geo_centroid": {
            "field": "location" __}
        }
      }
    }

__

|

"geo_centroid"聚合指定用于计算质心的字段。(注意：字段必须是地理点类型) ---|--- 上面的聚合演示了如何计算所有博物馆文档的位置字段的质心。

上述聚合的响应：

    
    
    {
      ...
      "aggregations": {
        "centroid": {
          "location": {
            "lat": 51.00982965203002,
            "lon": 3.9662131341174245
          },
          "count": 6
        }
      }
    }

当"geo_centroid"聚合作为子聚合与其他存储桶聚合组合时更有趣。

Example:

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          cities: {
            terms: {
              field: 'city.keyword'
            },
            aggregations: {
              centroid: {
                geo_centroid: {
                  field: 'location'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "cities": {
          "terms": { "field": "city.keyword" },
          "aggs": {
            "centroid": {
              "geo_centroid": { "field": "location" }
            }
          }
        }
      }
    }

上面的示例使用"geo_centroid"作为 atermsbucket 聚合的子聚合，用于查找每个城市中博物馆的中心位置。

上述聚合的响应：

    
    
    {
      ...
      "aggregations": {
        "cities": {
          "sum_other_doc_count": 0,
          "doc_count_error_upper_bound": 0,
          "buckets": [
            {
              "key": "Amsterdam",
              "doc_count": 3,
              "centroid": {
                "location": {
                  "lat": 52.371655656024814,
                  "lon": 4.909563297405839
                },
                "count": 3
              }
            },
            {
              "key": "Paris",
              "doc_count": 2,
              "centroid": {
                "location": {
                  "lat": 48.86055548675358,
                  "lon": 2.3316944623366
                },
                "count": 2
              }
            },
            {
              "key": "Antwerp",
              "doc_count": 1,
              "centroid": {
                "location": {
                  "lat": 51.22289997059852,
                  "lon": 4.40519998781383
                },
                "count": 1
              }
            }
          ]
        }
      }
    }

#### "geo_shape"字段上的地理质心聚合

地理形状的质心度量比点的质心度量更细微。包含形状的特定聚合存储桶的质心是存储桶中维度最高的形状类型的质心。例如，如果存储桶包含由多边形和线组成的形状，则线对质心度量没有贡献。每种形状的质心的计算方式都不同。通过圆引入的信封和圆被视为多边形。

几何类型 |质心计算 ---|--- [多]点

|

所有坐标 [Multi] LineString 的等加权平均值

|

每个线段的所有质心的加权平均值，其中每个线段的权重是其长度(以度为单位) [多多边形]

|

多边形的所有三角形的所有质心的加权平均值其中三角形由每两个连续的顶点和起点形成。孔的权重为负。权重表示三角形的面积，以 deg^2 计算的几何集合

|

具有最高维度的所有基础几何图形的质心。如果面和线和/或点，则忽略线和/或点。如果线和点，则忽略点 示例：

    
    
    response = client.indices.create(
      index: 'places',
      body: {
        mappings: {
          properties: {
            geometry: {
              type: 'geo_shape'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'places',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          name: 'NEMO Science Museum',
          geometry: 'POINT(4.912350 52.374081)'
        },
        {
          index: {
            _id: 2
          }
        },
        {
          name: 'Sportpark De Weeren',
          geometry: {
            type: 'Polygon',
            coordinates: [
              [
                [
                  4.965305328369141,
                  52.39347642069457
                ],
                [
                  4.966979026794433,
                  52.391721758934835
                ],
                [
                  4.969425201416015,
                  52.39238958618537
                ],
                [
                  4.967944622039794,
                  52.39420969150824
                ],
                [
                  4.965305328369141,
                  52.39347642069457
                ]
              ]
            ]
          }
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'places',
      size: 0,
      body: {
        aggregations: {
          centroid: {
            geo_centroid: {
              field: 'geometry'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /places
    {
      "mappings": {
        "properties": {
          "geometry": {
            "type": "geo_shape"
          }
        }
      }
    }
    
    POST /places/_bulk?refresh
    {"index":{"_id":1}}
    {"name": "NEMO Science Museum", "geometry": "POINT(4.912350 52.374081)" }
    {"index":{"_id":2}}
    {"name": "Sportpark De Weeren", "geometry": { "type": "Polygon", "coordinates": [ [ [ 4.965305328369141, 52.39347642069457 ], [ 4.966979026794433, 52.391721758934835 ], [ 4.969425201416015, 52.39238958618537 ], [ 4.967944622039794, 52.39420969150824 ], [ 4.965305328369141, 52.39347642069457 ] ] ] } }
    
    POST /places/_search?size=0
    {
      "aggs": {
        "centroid": {
          "geo_centroid": {
            "field": "geometry"
          }
        }
      }
    }
    
    
    {
      ...
      "aggregations": {
        "centroid": {
          "location": {
            "lat": 52.39296147599816,
            "lon": 4.967404240742326
          },
          "count": 2
        }
      }
    }

### 使用"geo_centroid"作为"geohash_grid"的子聚合

"geohash_grid"聚合将文档(而不是单个地理点)放入存储桶中。如果文档的"geo_point"字段包含多个值，则可以将文档分配给多个存储桶，即使其一个或多个地理点位于存储桶边界之外也是如此。

如果还使用"地质心"子聚合，则使用存储桶中的所有地理点(包括存储桶边界外的地理点)计算每个质心。这可能会导致质心超出存储桶边界。

[« Geo-bounds aggregation](search-aggregations-metrics-geobounds-
aggregation.md) [Geo-line aggregation »](search-aggregations-metrics-geo-
line.md)
