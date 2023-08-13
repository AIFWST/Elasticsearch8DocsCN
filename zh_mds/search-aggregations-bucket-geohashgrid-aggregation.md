

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Geo-distance aggregation](search-aggregations-bucket-geodistance-
aggregation.md) [Geohex grid aggregation »](search-aggregations-bucket-
geohexgrid-aggregation.md)

## 地理哈希网格聚合

一种多存储桶聚合，将"geo_point"和"geo_shape"值分组到表示网格的存储桶中。生成的网格可以是稀疏的，并且仅包含具有匹配数据的单元格。每个单元格都使用具有用户可定义精度的 ageohash 进行标记。

* 高精度地理哈希具有较长的字符串长度，表示仅覆盖小区域的单元格。  * 低精度地理哈希的字符串长度较短，表示每个单元格覆盖较大区域的单元格。

此聚合中使用的地理哈希可以选择介于 1 和 12 之间的精度。

长度为 12 的高精度 geohash 生成的单元覆盖不到一平方米的土地，因此高精度请求在 RAM 和结果大小方面可能非常昂贵。请参阅下面的示例，了解如何在请求高级别详细信息之前先将聚合筛选到较小的地理区域。

您只能使用"geohash_grid"来聚合显式映射的"geo_point"或"geo_shape"字段。如果"geo_point"字段包含数组，则"geohash_grid"将聚合所有数组值。

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
            geohash_grid: {
              field: 'location',
              precision: 3
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
          "geohash_grid": {
            "field": "location",
            "precision": 3
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
            "key": "u17",
            "doc_count": 3
          },
          {
            "key": "u09",
            "doc_count": 2
          },
          {
            "key": "u15",
            "doc_count": 1
          }
        ]
      }
    }
    }

### 高精度请求

当请求详细的存储桶(通常用于显示"放大"地图)时，应应用像geo_bounding_box这样的过滤器来缩小主题区域，否则可能会创建和返回数百万个存储桶。

    
    
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
                geohash_grid: {
                  field: 'location',
                  precision: 8
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
              "geohash_grid": {
                "field": "location",
                "precision": 8
              }
            }
          }
        }
      }
    }

"geohash_grid"聚合返回的地理哈希也可用于放大。要放大上一个示例中返回的第一个地理哈希"u17"，应将其指定为"top_left"和"bottom_right"角：

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          "zoomed-in": {
            filter: {
              geo_bounding_box: {
                location: {
                  top_left: 'u17',
                  bottom_right: 'u17'
                }
              }
            },
            aggregations: {
              "zoom1": {
                geohash_grid: {
                  field: 'location',
                  precision: 8
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
                "top_left": "u17",
                "bottom_right": "u17"
              }
            }
          },
          "aggregations": {
            "zoom1": {
              "geohash_grid": {
                "field": "location",
                "precision": 8
              }
            }
          }
        }
      }
    }
    
    
    {
      ...
      "aggregations": {
        "zoomed-in": {
          "doc_count": 3,
          "zoom1": {
            "buckets": [
              {
                "key": "u173zy3j",
                "doc_count": 1
              },
              {
                "key": "u173zvfz",
                "doc_count": 1
              },
              {
                "key": "u173zt90",
                "doc_count": 1
              }
            ]
          }
        }
      }
    }

对于不支持地理哈希的系统"放大"，应使用可用的地理哈希库之一将存储桶键转换为边界框。例如，对于javascript，可以使用node-geohash库：

    
    
    var geohash = require('ngeohash');
    
    // bbox will contain [ 52.03125, 4.21875, 53.4375, 5.625 ]
    //                   [   minlat,  minlon,  maxlat, maxlon]
    var bbox = geohash.decode_bbox('u17');

### 具有附加边界框筛选的请求

"geohash_grid"聚合支持可选的"边界"参数，该参数将考虑的像元限制为与提供的边界相交的像元。"bounds"参数接受地理边界框查询中指定的边界的所有相同接受格式的边界框。此边界框可以与或不带有额外的"geo_bounding_box"查询一起使用，以便在聚合之前筛选点。它是一个独立的边界框，可以与聚合上下文中定义的任何其他"geo_bounding_box"查询相交、相等或不相交。

    
    
    response = client.search(
      index: 'museums',
      size: 0,
      body: {
        aggregations: {
          "tiles-in-bounds": {
            geohash_grid: {
              field: 'location',
              precision: 8,
              bounds: {
                top_left: 'POINT (4.21875 53.4375)',
                bottom_right: 'POINT (5.625 52.03125)'
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
          "geohash_grid": {
            "field": "location",
            "precision": 8,
            "bounds": {
              "top_left": "POINT (4.21875 53.4375)",
              "bottom_right": "POINT (5.625 52.03125)"
            }
          }
        }
      }
    }
    
    
    {
      ...
      "aggregations": {
        "tiles-in-bounds": {
          "buckets": [
            {
              "key": "u173zy3j",
              "doc_count": 1
            },
            {
              "key": "u173zvfz",
              "doc_count": 1
            },
            {
              "key": "u173zt90",
              "doc_count": 1
            }
          ]
        }
      }
    }

### 赤道处的单元格尺寸

下表显示了各种字符串长度的地理哈希所覆盖的单元格的指标维度。像元尺寸随纬度而变化，因此该表适用于赤道的最坏情况。

**地理哈希长度**

|

**区域宽度 x 高度** ---|--- 1

|

5，009.4公里 x 4，992.6公里 2

|

1，252.3公里 x 624.1公里 3

|

156.5公里 x 156公里 4

|

39.1公里 x 19.5公里 5

|

4.9公里 x 4.9公里 6

|

1.2公里 x 609.4米 7

|

152.9米 x 152.4米 8

|

38.2米 x 19米 9

|

4.8m x 4.8m 10

|

1.2米 x 59.5厘米 11

|

14.9厘米 x 14.9厘米 12

|

3.7 厘米 x 1.9 厘米 #### 聚合"geo_shape"字段编辑

在 Geoshape 字段上进行聚合的工作方式与对点的聚合方式相同，只是可以为多个切片计算单个形状。如果形状的任何部分与该磁贴相交，则形状将计入匹配值的计数。下图演示了这一点：

！地理形状网格

###Options

field

|

命令的。使用 GeoPoint 编制索引的字段的名称。   ---|---精度

|

自选。用于定义结果中的单元格/存储桶的地理哈希的字符串长度。默认值为 5。精度可以根据上述整数精度级别进行定义。[1，12] 之外的值将被拒绝。或者，精度水平可以从距离测量值(如"1km"、"10m")近似值。计算精度级别时，单元格不会超过所需精度的指定大小(对角线)。当这会导致精度级别高于支持的 12 个级别时(例如，对于距离 <5.6cm)，该值将被拒绝。   边界

|

自选。用于筛选存储桶中的点的边界框。   大小

|

自选。要返回的最大地理哈希存储桶数(默认为 10，000)。修剪结果时，将根据存储桶包含的文档量确定存储桶的优先级。   shard_size

|

自选。为了更准确地计算最终结果中返回的顶级单元格，聚合默认为每个分片返回"max(10，(大小 x 分片数))"存储桶。如果这种启发式是不可取的，则可以使用此参数覆盖从每个分片考虑的数字。   « 地理距离聚合 Geohex 网格聚合 »