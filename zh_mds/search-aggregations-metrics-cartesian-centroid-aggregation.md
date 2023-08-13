

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Cartesian-bounds aggregation](search-aggregations-metrics-cartesian-bounds-
aggregation.md) [Matrix stats aggregation »](search-aggregations-matrix-
stats-aggregation.md)

## 笛卡尔质心聚合

一种度量聚合，用于根据点和形状字段的所有坐标值计算加权质心。

Example:

    
    
    response = client.indices.create(
      index: 'museums',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'point'
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
          location: 'POINT (491.2350 5237.4081)',
          city: 'Amsterdam',
          name: 'NEMO Science Museum'
        },
        {
          index: {
            _id: 2
          }
        },
        {
          location: 'POINT (490.1618 5236.9219)',
          city: 'Amsterdam',
          name: 'Museum Het Rembrandthuis'
        },
        {
          index: {
            _id: 3
          }
        },
        {
          location: 'POINT (491.4722 5237.1667)',
          city: 'Amsterdam',
          name: 'Nederlands Scheepvaartmuseum'
        },
        {
          index: {
            _id: 4
          }
        },
        {
          location: 'POINT (440.5200 5122.2900)',
          city: 'Antwerp',
          name: 'Letterenhuis'
        },
        {
          index: {
            _id: 5
          }
        },
        {
          location: 'POINT (233.6389 4886.1111)',
          city: 'Paris',
          name: 'Musée du Louvre'
        },
        {
          index: {
            _id: 6
          }
        },
        {
          location: 'POINT (232.7000 4886.0000)',
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
            cartesian_centroid: {
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
            "type": "point"
          }
        }
      }
    }
    
    POST /museums/_bulk?refresh
    {"index":{"_id":1}}
    {"location": "POINT (491.2350 5237.4081)", "city": "Amsterdam", "name": "NEMO Science Museum"}
    {"index":{"_id":2}}
    {"location": "POINT (490.1618 5236.9219)", "city": "Amsterdam", "name": "Museum Het Rembrandthuis"}
    {"index":{"_id":3}}
    {"location": "POINT (491.4722 5237.1667)", "city": "Amsterdam", "name": "Nederlands Scheepvaartmuseum"}
    {"index":{"_id":4}}
    {"location": "POINT (440.5200 5122.2900)", "city": "Antwerp", "name": "Letterenhuis"}
    {"index":{"_id":5}}
    {"location": "POINT (233.6389 4886.1111)", "city": "Paris", "name": "Musée du Louvre"}
    {"index":{"_id":6}}
    {"location": "POINT (232.7000 4886.0000)", "city": "Paris", "name": "Musée d'Orsay"}
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "centroid": {
          "cartesian_centroid": {
            "field": "location" __}
        }
      }
    }

__

|

"cartesian_centroid"聚合指定用于计算质心的字段，该字段必须是点或 aShape 类型。   ---|--- 上面的聚合演示了如何计算所有博物馆文档的位置字段的质心。

上述聚合的响应：

    
    
    {
      ...
      "aggregations": {
        "centroid": {
          "location": {
            "x": 396.6213124593099,
            "y": 5100.982991536458
          },
          "count": 6
        }
      }
    }

当"cartesian_centroid"聚合作为子聚合与其他存储桶聚合组合时更有趣。

Example:

    
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "cities": {
          "terms": { "field": "city.keyword" },
          "aggs": {
            "centroid": {
              "cartesian_centroid": { "field": "location" }
            }
          }
        }
      }
    }

上面的例子使用"cartesian_centroid"作为atermsbucket聚合的子聚合，用于查找每个城市中博物馆的中心位置。

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
                  "x": 490.9563293457031,
                  "y": 5237.16552734375
                },
                "count": 3
              }
            },
            {
              "key": "Paris",
              "doc_count": 2,
              "centroid": {
                "location": {
                  "x": 233.16944885253906,
                  "y": 4886.0556640625
                },
                "count": 2
              }
            },
            {
              "key": "Antwerp",
              "doc_count": 1,
              "centroid": {
                "location": {
                  "x": 440.5199890136719,
                  "y": 5122.2900390625
                },
                "count": 1
              }
            }
          ]
        }
      }
    }

#### "形状"字段上的笛卡尔质心聚合

形状的质心度量比点的质心度量更细微。包含形状的特定聚合存储桶的质心是存储桶中维度最高的形状类型的质心。例如，如果存储桶包含由多边形和线条组成的形状，则线条对质心指标没有贡献。每种形状的质心的计算方式都不同。通过圆引入的信封和圆被视为多边形。

几何类型 |质心计算 ---|--- [多]点

|

所有坐标 [Multi] LineString 的等加权平均值

|

每个线段的所有质心的加权平均值，其中每个线段的权重是其长度，单位与坐标 [多]多边形相同

|

多边形的所有三角形的所有质心的加权平均值其中三角形由每两个连续的顶点和起点形成。孔的权重为负。权重表示三角形的面积以坐标单位的平方计算 几何集合

|

具有最高维度的所有基础几何图形的质心。如果面和线和/或点，则忽略线和/或点。如果线和点，则忽略点 示例：

    
    
    response = client.indices.create(
      index: 'places',
      body: {
        mappings: {
          properties: {
            geometry: {
              type: 'shape'
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
          geometry: 'POINT(491.2350 5237.4081)'
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
                  496.5305328369141,
                  5239.347642069457
                ],
                [
                  496.6979026794433,
                  5239.172175893484
                ],
                [
                  496.9425201416015,
                  5239.238958618537
                ],
                [
                  496.7944622039794,
                  5239.420969150824
                ],
                [
                  496.5305328369141,
                  5239.347642069457
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
            cartesian_centroid: {
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
            "type": "shape"
          }
        }
      }
    }
    
    POST /places/_bulk?refresh
    {"index":{"_id":1}}
    {"name": "NEMO Science Museum", "geometry": "POINT(491.2350 5237.4081)" }
    {"index":{"_id":2}}
    {"name": "Sportpark De Weeren", "geometry": { "type": "Polygon", "coordinates": [ [ [ 496.5305328369141, 5239.347642069457 ], [ 496.6979026794433, 5239.1721758934835 ], [ 496.9425201416015, 5239.238958618537 ], [ 496.7944622039794, 5239.420969150824 ], [ 496.5305328369141, 5239.347642069457 ] ] ] } }
    
    POST /places/_search?size=0
    {
      "aggs": {
        "centroid": {
          "cartesian_centroid": {
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
            "x": 496.74041748046875,
            "y": 5239.29638671875
          },
          "count": 2
        }
      }
    }

[« Cartesian-bounds aggregation](search-aggregations-metrics-cartesian-bounds-
aggregation.md) [Matrix stats aggregation »](search-aggregations-matrix-
stats-aggregation.md)
