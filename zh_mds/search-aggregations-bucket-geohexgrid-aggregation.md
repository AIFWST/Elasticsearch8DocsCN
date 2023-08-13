

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Geohash grid aggregation](search-aggregations-bucket-geohashgrid-
aggregation.md) [Geotile grid aggregation »](search-aggregations-bucket-
geotilegrid-aggregation.md)

## 地理十六进制网格聚合

一种多存储桶聚合，将"geo_point"和"geo_shape"值分组到表示网格的存储桶中。生成的网格可以是稀疏的，并且仅包含具有匹配数据的单元格。每个单元格对应于一个 H3 单元格索引，并使用 H3Index 表示形式进行标记。

有关 H3 分辨率，请参阅单元格区域表，了解精度(缩放)与地面大小的关联关系。此聚合的精度可以介于 0 和 15 之间(包括 0 和 15)。

高精度请求在 RAM 和结果大小方面可能非常昂贵。例如，精度为 15 的最高精度 geohex 生成的单元覆盖面积小于 1 平方米。建议使用 afilter 将高精度请求限制在较小的地理区域。有关示例，请参阅高精度请求。

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
            geohex_grid: {
              field: 'location',
              precision: 4
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
          "geohex_grid": {
            "field": "location",
            "precision": 4
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
              "key": "841969dffffffff",
              "doc_count": 3
            },
            {
              "key": "841fb47ffffffff",
              "doc_count": 2
            },
            {
              "key": "841fa4dffffffff",
              "doc_count": 1
            }
          ]
        }
      }
    }

### 高精度请求

当请求详细的存储桶(通常用于显示"放大"地图)时，应应用类似geo_bounding_box的过滤器来缩小主题区域。否则，可能会创建并返回数百万个存储桶。

    
    
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
              "geohex_grid": {
                "field": "location",
                "precision": 12
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
                "key": "8c1969c9b2617ff",
                "doc_count": 1
              },
              {
                "key": "8c1969526d753ff",
                "doc_count": 1
              },
              {
                "key": "8c1969526d26dff",
                "doc_count": 1
              }
            ]
          }
        }
      }
    }

### 具有附加边界框筛选的请求

"geohex_grid"聚合支持可选的"边界"参数，该参数将考虑的像元限制为与提供的边界相交的像元。"bounds"参数接受与地理边界框查询相同的边界框格式。此边界框可以与或不带有额外的"geo_bounding_box"查询一起使用，以便在聚合之前过滤点。它是一个独立的边界框，可以与聚合上下文中定义的任何其他"geo_bounding_box"查询相交、相等或不相交。

    
    
    POST /museums/_search?size=0
    {
      "aggregations": {
        "tiles-in-bounds": {
          "geohex_grid": {
            "field": "location",
            "precision": 12,
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
              "key": "8c1969c9b2617ff",
              "doc_count": 1
            },
            {
              "key": "8c1969526d753ff",
              "doc_count": 1
            },
            {
              "key": "8c1969526d26dff",
              "doc_count": 1
            }
          ]
        }
      }
    }

#### 聚合"geo_shape"字段

在Geoshape字段上进行聚合几乎与对点进行聚合一样。有两个主要区别：

* 聚合"geo_point"数据时，如果点位于由大圆定义的边内，则考虑在六边形图块内。换句话说，计算是使用球面坐标完成的。但是，在聚合"geo_shape"数据时，如果形状位于等距柱状投影上定义为直线的边内，则将其视为六边形内。原因是 Elasticsearch 和 Lucene 在索引和搜索时使用等距柱线投影来处理边缘。因此，为了确保搜索结果和聚合结果保持一致，我们还在聚合中使用等距柱状投影。对于大多数数据，差异是微妙的或没有注意到的。但是，对于低缩放级别(低精度)，尤其是远离赤道，这可能会很明显。例如，如果将同一点数据索引为"geo_point"和"geo_shape"，则在以较低分辨率聚合时可能会获得不同的结果。  * 与"geotile_grid"的情况一样，单个形状可以在多个磁贴中计数。如果形状的任何部分与该磁贴相交，则形状将计入匹配值的计数。下图演示了这一点：

！地形六角形网格

###Options

field

|

(必需，字符串)包含索引地理点或地理形状值的字段。必须显式映射为"geo_point"或"geo_shape"字段。如果字段包含数组，则"geohex_grid"聚合所有数组值。   ---|---精度

|

(可选，整数)用于在结果中定义单元格/存储桶的键的整数缩放。默认为"6"。['0'，'15'] 之外的值将被拒绝。   边界

|

(可选，对象)用于筛选每个存储桶中的地理点或地理形状的边界框。接受与地理边界框查询相同的边界框格式。   大小

|

(可选，整数)要返回的最大存储桶数。默认值为 10，000。修剪结果时，将根据存储桶包含的文档量确定存储桶的优先级。   shard_size

|

(可选，整数)从每个分片返回的存储桶数。默认为"max(10，(大小 x 分片数))"，以便在最终结果中更准确地计数顶部单元格。由于每个分片可能具有不同的 topresult 顺序，因此在此处使用较大的数字可以降低计数不准确的风险，但会产生性能成本。   « 地理哈希网格聚合 地理瓦网格聚合 »