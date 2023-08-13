

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Frequent item sets aggregation](search-aggregations-bucket-frequent-item-
sets-aggregation.md) [Geohash grid aggregation »](search-aggregations-
bucket-geohashgrid-aggregation.md)

## 地理距离聚合

一种多存储桶聚合，适用于"geo_point"字段，在概念上的工作方式与范围聚合非常相似。用户可以定义原点和一组距离范围桶。聚合评估每个文档值与原点的距离，并根据范围确定其所属的存储桶(如果文档与原点之间的距离在存储桶的距离范围内，则文档属于存储桶)。

    
    
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
        aggregations: {
          rings_around_amsterdam: {
            geo_distance: {
              field: 'location',
              origin: 'POINT (4.894 52.3760)',
              ranges: [
                {
                  to: 100_000
                },
                {
                  from: 100_000,
                  to: 300_000
                },
                {
                  from: 300_000
                }
              ]
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
      "aggs": {
        "rings_around_amsterdam": {
          "geo_distance": {
            "field": "location",
            "origin": "POINT (4.894 52.3760)",
            "ranges": [
              { "to": 100000 },
              { "from": 100000, "to": 300000 },
              { "from": 300000 }
            ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "rings_around_amsterdam": {
          "buckets": [
            {
              "key": "*-100000.0",
              "from": 0.0,
              "to": 100000.0,
              "doc_count": 3
            },
            {
              "key": "100000.0-300000.0",
              "from": 100000.0,
              "to": 300000.0,
              "doc_count": 1
            },
            {
              "key": "300000.0-*",
              "from": 300000.0,
              "doc_count": 2
            }
          ]
        }
      }
    }

指定的字段必须为"geo_point"类型(只能在映射中显式设置)。它还可以保存一个"geo_point"字段数组，在这种情况下，在聚合过程中将考虑所有字段。原点可以接受"geo_point"类型支持的所有格式：

* 对象格式： '{ "lat" ： 52.3760， "lon" ： 4.894 }' \- 这是最安全的格式，因为它对"lat"和"lon"值最明确 * 字符串格式："52.3760， 4.894"' \- 其中第一个数字是"lat"，第二个是 'lon' * 数组格式： '[4.894， 52.3760]' \- 基于 GeoJSON 标准，其中第一个数字是 'lon'，第二个是 'lat'

默认情况下，距离单位为"m"(米)，但它也可以接受："mi"(英里)、"in"(英寸)、"yd"(码)、"km"(公里)、"cm"(厘米)、"mm"(毫米)。

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          rings: {
            geo_distance: {
              field: 'location',
              origin: 'POINT (4.894 52.3760)',
              unit: 'km',
              ranges: [
                {
                  to: 100
                },
                {
                  from: 100,
                  to: 300
                },
                {
                  from: 300
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "rings": {
          "geo_distance": {
            "field": "location",
            "origin": "POINT (4.894 52.3760)",
            "unit": "km", __"ranges": [
              { "to": 100 },
              { "from": 100, "to": 300 },
              { "from": 300 }
            ]
          }
        }
      }
    }

__

|

距离将以公里为单位计算 ---|--- 有两种距离计算模式："弧"(默认值)和"平面"。"弧"计算是最准确的。"飞机"是最快的，但最不准确。当您的搜索上下文"狭窄"且跨越较小的地理区域(~5公里)时，请考虑使用"平面"。"plane"将为跨非常大区域的搜索(例如跨大陆搜索)返回更高的误差幅度。可以使用"distance_type"参数设置距离计算类型：

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          rings: {
            geo_distance: {
              field: 'location',
              origin: 'POINT (4.894 52.3760)',
              unit: 'km',
              distance_type: 'plane',
              ranges: [
                {
                  to: 100
                },
                {
                  from: 100,
                  to: 300
                },
                {
                  from: 300
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "rings": {
          "geo_distance": {
            "field": "location",
            "origin": "POINT (4.894 52.3760)",
            "unit": "km",
            "distance_type": "plane",
            "ranges": [
              { "to": 100 },
              { "from": 100, "to": 300 },
              { "from": 300 }
            ]
          }
        }
      }
    }

### 键控响应

将"keyed"标志设置为"true"会将一个唯一的字符串键与每个存储桶相关联，并将范围作为哈希而不是数组返回：

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          rings_around_amsterdam: {
            geo_distance: {
              field: 'location',
              origin: 'POINT (4.894 52.3760)',
              ranges: [
                {
                  to: 100_000
                },
                {
                  from: 100_000,
                  to: 300_000
                },
                {
                  from: 300_000
                }
              ],
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "rings_around_amsterdam": {
          "geo_distance": {
            "field": "location",
            "origin": "POINT (4.894 52.3760)",
            "ranges": [
              { "to": 100000 },
              { "from": 100000, "to": 300000 },
              { "from": 300000 }
            ],
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "rings_around_amsterdam": {
          "buckets": {
            "*-100000.0": {
              "from": 0.0,
              "to": 100000.0,
              "doc_count": 3
            },
            "100000.0-300000.0": {
              "from": 100000.0,
              "to": 300000.0,
              "doc_count": 1
            },
            "300000.0-*": {
              "from": 300000.0,
              "doc_count": 2
            }
          }
        }
      }
    }

还可以为每个范围自定义键：

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          rings_around_amsterdam: {
            geo_distance: {
              field: 'location',
              origin: 'POINT (4.894 52.3760)',
              ranges: [
                {
                  to: 100_000,
                  key: 'first_ring'
                },
                {
                  from: 100_000,
                  to: 300_000,
                  key: 'second_ring'
                },
                {
                  from: 300_000,
                  key: 'third_ring'
                }
              ],
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    POST /museums/_search?size=0
    {
      "aggs": {
        "rings_around_amsterdam": {
          "geo_distance": {
            "field": "location",
            "origin": "POINT (4.894 52.3760)",
            "ranges": [
              { "to": 100000, "key": "first_ring" },
              { "from": 100000, "to": 300000, "key": "second_ring" },
              { "from": 300000, "key": "third_ring" }
            ],
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "rings_around_amsterdam": {
          "buckets": {
            "first_ring": {
              "from": 0.0,
              "to": 100000.0,
              "doc_count": 3
            },
            "second_ring": {
              "from": 100000.0,
              "to": 300000.0,
              "doc_count": 1
            },
            "third_ring": {
              "from": 300000.0,
              "doc_count": 2
            }
          }
        }
      }
    }

[« Frequent item sets aggregation](search-aggregations-bucket-frequent-item-
sets-aggregation.md) [Geohash grid aggregation »](search-aggregations-
bucket-geohashgrid-aggregation.md)
