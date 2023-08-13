

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Geo-line aggregation](search-aggregations-metrics-geo-line.md)
[Cartesian-centroid aggregation »](search-aggregations-metrics-cartesian-
centroid-aggregation.md)

## 笛卡尔边界聚合

一种指标聚合，用于计算包含"点"或"形状"字段的所有值的空间边界框。

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
        query: {
          match: {
            name: 'musée'
          }
        },
        aggregations: {
          viewport: {
            cartesian_bounds: {
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
      "query": {
        "match": { "name": "musée" }
      },
      "aggs": {
        "viewport": {
          "cartesian_bounds": {
            "field": "location"    __}
        }
      }
    }

__

|

"cartesian_bounds"聚合指定用于获取边界的字段，该字段必须是点或形状类型。   ---|--- 与"geo_bounds"聚合的情况不同，没有设置"wrap_longitude"的选项。这是因为笛卡尔空间是欧几里得空间，不会自行回绕。因此，边界将始终具有小于或等于最大值 x 值的最小 x 值。

上面的聚合演示了如何计算名称与"musée"匹配的所有文档的位置字段的边界框。

上述聚合的响应：

    
    
    {
      ...
      "aggregations": {
        "viewport": {
          "bounds": {
            "top_left": {
              "x": 232.6999969482422,
              "y": 4886.111328125
            },
            "bottom_right": {
              "x": 233.63890075683594,
              "y": 4886.0
            }
          }
        }
      }
    }

#### "形状"字段上的笛卡尔边界聚合

笛卡尔边界聚合在"cartesian_shape"字段上也受支持。

Example:

    
    
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
          viewport: {
            cartesian_bounds: {
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
        "viewport": {
          "cartesian_bounds": {
            "field": "geometry"
          }
        }
      }
    }
    
    
    {
      ...
      "aggregations": {
        "viewport": {
          "bounds": {
            "top_left": {
              "x": 491.2349853515625,
              "y": 5239.4208984375
            },
            "bottom_right": {
              "x": 496.9425048828125,
              "y": 5237.408203125
            }
          }
        }
      }
    }

[« Geo-line aggregation](search-aggregations-metrics-geo-line.md)
[Cartesian-centroid aggregation »](search-aggregations-metrics-cartesian-
centroid-aggregation.md)
