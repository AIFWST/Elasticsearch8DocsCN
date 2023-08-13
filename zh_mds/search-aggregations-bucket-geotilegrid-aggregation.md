

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Geohex grid aggregation](search-aggregations-bucket-geohexgrid-
aggregation.md) [Global aggregation »](search-aggregations-bucket-global-
aggregation.md)

## 地理图块网格聚合

一种多存储桶聚合，将"geo_point"和"geo_shape"值分组到表示网格的存储桶中。生成的网格可以是稀疏的，并且仅包含具有匹配数据的单元格。每个单元格对应于许多在线地图站点使用的地图图块。每个单元格都使用"{zoom}/{x}/{y}"格式进行标记，其中缩放等于用户指定的精度。

* 高精度键的 x 和 y 范围更大，表示仅覆盖小面积的磁贴。  * 低精度键的 x 和 y 范围较小，表示每个键覆盖较大区域的磁贴。

请参阅缩放级别文档，了解精度(缩放)如何与地面尺寸相关联。此聚合的精度可以介于 0 和 29 之间(包括 0 和 29)。

长度为 29 的最高精度土工磁贴产生的单元覆盖不到 10 厘米 x 10 厘米的土地，因此高精度请求在 RAM 和结果大小方面可能非常昂贵。请参阅下面的示例，了解如何在请求高级别详细信息之前先将聚合筛选到较小的地理区域。

您只能使用"geotile_grid"来聚合显式映射的"geo_point"或"geo_shape"字段。如果"geo_point"字段包含数组，则"geotile_grid"聚合所有数组值。

### 简单的低精度请求

    
    
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
          "large-grid": {
            geotile_grid: {
              field: 'location',
              precision: 8
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
      "aggregations": {
        "large-grid": {
          "geotile_grid": {
            "field": "location",
            "precision": 8
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "large-grid": {
          "buckets": [
            {
              "key": "8/131/84",
              "doc_count": 3
            },
            {
              "key": "8/129/88",
              "doc_count": 2
            },
            {
              "key": "8/131/85",
              "doc_count": 1
            }
          ]
        }
      }
    }

### 高精度请求

当请求详细的存储桶(通常用于显示"放大"地图)时，应应用类似geo_bounding_box的过滤器来缩小主题区域。否则，可能会创建并返回数百万个存储桶。

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          "zoomed-in": {
            filter: {
              geo_bounding_box: {
                location: {
                  top_left: 'POINT (4.9 52.4)',
                  bottom_right: 'POINT (5.0 52.3)'
                }
              }
            },
            aggregations: {
              "zoom1": {
                geotile_grid: {
                  field: 'location',
                  precision: 22
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
      "aggregations": {
        "zoomed-in": {
          "filter": {
            "geo_bounding_box": {
              "location": {
                "top_left": "POINT (4.9 52.4)",
                "bottom_right": "POINT (5.0 52.3)"
              }
            }
          },
          "aggregations": {
            "zoom1": {
              "geotile_grid": {
                "field": "location",
                "precision": 22
              }
            }
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "zoomed-in": {
          "doc_count": 3,
          "zoom1": {
            "buckets": [
              {
                "key": "22/2154412/1378379",
                "doc_count": 1
              },
              {
                "key": "22/2154385/1378332",
                "doc_count": 1
              },
              {
                "key": "22/2154259/1378425",
                "doc_count": 1
              }
            ]
          }
        }
      }
    }

### 具有附加边界框筛选的请求

"geotile_grid"聚合支持可选的"边界"参数，该参数将考虑的单元格限制为与提供的边界相交的单元格。"bounds"参数接受与地理边界框查询相同的边界框格式。此边界框可以与或不带有额外的"geo_bounding_box"查询一起使用，以便在聚合之前过滤点。它是一个独立的边界框，可以与聚合上下文中定义的任何其他"geo_bounding_box"查询相交、相等或不相交。

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          "tiles-in-bounds": {
            geotile_grid: {
              field: 'location',
              precision: 22,
              bounds: {
                top_left: 'POINT (4.9 52.4)',
                bottom_right: 'POINT (5.0 52.3)'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /museums/_search?size=0
    {
      "aggregations": {
        "tiles-in-bounds": {
          "geotile_grid": {
            "field": "location",
            "precision": 22,
            "bounds": {
              "top_left": "POINT (4.9 52.4)",
              "bottom_right": "POINT (5.0 52.3)"
            }
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "tiles-in-bounds": {
          "buckets": [
            {
              "key": "22/2154412/1378379",
              "doc_count": 1
            },
            {
              "key": "22/2154385/1378332",
              "doc_count": 1
            },
            {
              "key": "22/2154259/1378425",
              "doc_count": 1
            }
          ]
        }
      }
    }

#### 聚合"geo_shape"字段

在 Geoshape 字段上进行聚合几乎与对点进行聚合一样，只是可以为多个切片计算单个形状。如果形状的任何部分与该磁贴相交，则形状将计入匹配值的计数。下图演示了这一点：

！地理形状网格

###Options

field

|

(必需，字符串)包含索引地理点或地理形状值的字段。必须显式映射为"geo_point"或"geo_shape"字段。如果字段包含数组，则"geotile_grid"聚合所有数组值。   ---|---精度

|

(可选，整数)用于在结果中定义单元格/存储桶的键的整数缩放。默认为"7"。['0'，'29'] 之外的值将被拒绝。   边界

|

(可选，对象)用于筛选每个存储桶中的地理点或地理形状的边界框。接受与地理边界框查询相同的边界框格式。   大小

|

(可选，整数)要返回的最大存储桶数。默认值为 10，000。修剪结果时，将根据存储桶包含的文档量确定存储桶的优先级。   shard_size

|

(可选，整数)从每个分片返回的存储桶数。默认为"max(10，(大小 x 分片数))"，以便在最终结果中更准确地计数顶部单元格。由于每个分片可能具有不同的 topresult 顺序，因此在此处使用较大的数字可以降低计数不准确的风险，但会产生性能成本。   « Geohex 网格聚合 全球聚合 »