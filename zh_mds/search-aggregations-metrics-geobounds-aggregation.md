

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Extended stats aggregation](search-aggregations-metrics-extendedstats-
aggregation.md) [Geo-centroid aggregation »](search-aggregations-metrics-
geocentroid-aggregation.md)

## 地理边界聚合

一种指标聚合，用于计算包含 Geopoint 或 Geoshape 字段的所有值的地理边界框。

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
          name: 'NEMO Science Museum'
        },
        {
          index: {
            _id: 2
          }
        },
        {
          location: 'POINT (4.901618 52.369219)',
          name: 'Museum Het Rembrandthuis'
        },
        {
          index: {
            _id: 3
          }
        },
        {
          location: 'POINT (4.914722 52.371667)',
          name: 'Nederlands Scheepvaartmuseum'
        },
        {
          index: {
            _id: 4
          }
        },
        {
          location: 'POINT (4.405200 51.222900)',
          name: 'Letterenhuis'
        },
        {
          index: {
            _id: 5
          }
        },
        {
          location: 'POINT (2.336389 48.861111)',
          name: 'Musée du Louvre'
        },
        {
          index: {
            _id: 6
          }
        },
        {
          location: 'POINT (2.327000 48.860000)',
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
            geo_bounds: {
              field: 'location',
              wrap_longitude: true
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
    {"location": "POINT (4.912350 52.374081)", "name": "NEMO Science Museum"}
    {"index":{"_id":2}}
    {"location": "POINT (4.901618 52.369219)", "name": "Museum Het Rembrandthuis"}
    {"index":{"_id":3}}
    {"location": "POINT (4.914722 52.371667)", "name": "Nederlands Scheepvaartmuseum"}
    {"index":{"_id":4}}
    {"location": "POINT (4.405200 51.222900)", "name": "Letterenhuis"}
    {"index":{"_id":5}}
    {"location": "POINT (2.336389 48.861111)", "name": "Musée du Louvre"}
    {"index":{"_id":6}}
    {"location": "POINT (2.327000 48.860000)", "name": "Musée d'Orsay"}
    
    POST /museums/_search?size=0
    {
      "query": {
        "match": { "name": "musée" }
      },
      "aggs": {
        "viewport": {
          "geo_bounds": {
            "field": "location",    __"wrap_longitude": true __}
        }
      }
    }

__

|

"geo_bounds"聚合指定用于获取边界的字段，该字段必须是 Geopoint 或 aGeoshape 类型。   ---|---    __

|

"wrap_longitude"是一个可选参数，用于指定是否应允许边界框与国际日期变更线重叠。默认值为"true"。   上面的聚合演示了如何计算名称与"musée"匹配的所有文档的位置字段的边界框。

上述聚合的响应：

    
    
    {
      ...
      "aggregations": {
        "viewport": {
          "bounds": {
            "top_left": {
              "lat": 48.86111099738628,
              "lon": 2.3269999679178
            },
            "bottom_right": {
              "lat": 48.85999997612089,
              "lon": 2.3363889567553997
            }
          }
        }
      }
    }

#### "geo_shape"字段上的地理边界聚合

"geo_shape"字段也支持地理边界聚合。

如果"wrap_longitude"设置为"true"(默认值)，则边界框可以与国际日期变更线重叠并返回"top_left"经度大于"top_right"经度的边界。

例如，右上经度通常大于地理边界框的左下经度。但是，当面积与 180° 经线交叉时，左下经度的值将大于右上经度的值。有关详细信息，请参阅 OpenGeospatial Consortium 网站上的地理边界框。

Example:

    
    
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
          viewport: {
            geo_bounds: {
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
        "viewport": {
          "geo_bounds": {
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
              "lat": 52.39420966710895,
              "lon": 4.912349972873926
            },
            "bottom_right": {
              "lat": 52.374080987647176,
              "lon": 4.969425117596984
            }
          }
        }
      }
    }

[« Extended stats aggregation](search-aggregations-metrics-extendedstats-
aggregation.md) [Geo-centroid aggregation »](search-aggregations-metrics-
geocentroid-aggregation.md)
