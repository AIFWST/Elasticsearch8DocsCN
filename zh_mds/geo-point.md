

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Flattened field type](flattened.md) [Geoshape field type »](geo-
shape.md)

## 地理点字段类型

类型为"geo_point"的字段接受经纬度对，可用于：

* 查找边界框内、中心点一定距离内或"geo_shape"查询(例如，多边形中的点)内的地理点。  * 按距中心点的距离聚合文档。  * 按地理网格汇总文件："geo_hash"、"geo_tile"或"geo_hex"。  * 使用指标聚合"geo_line"将地理点聚合到轨迹中。  * 将距离整合到文档的相关度分数中。  * 按距离对文档进行排序。

与geo_shape和点一样，可以在GeoJSON和No-KnownText格式中指定"geo_point"。但是，出于方便和历史原因，还支持许多其他格式。总共有六种方法可以指定 ageopoint，如下所示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
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
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        text: 'Geopoint as an object using GeoJSON format',
        location: {
          type: 'Point',
          coordinates: [
            -71.34,
            41.12
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        text: 'Geopoint as a WKT POINT primitive',
        location: 'POINT (-71.34 41.12)'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 3,
      body: {
        text: "Geopoint as an object with 'lat' and 'lon' keys",
        location: {
          lat: 41.12,
          lon: -71.34
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 4,
      body: {
        text: 'Geopoint as an array',
        location: [
          -71.34,
          41.12
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 5,
      body: {
        text: 'Geopoint as a string',
        location: '41.12,-71.34'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 6,
      body: {
        text: 'Geopoint as a geohash',
        location: 'drm3btev3e86'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          geo_bounding_box: {
            location: {
              top_left: {
                lat: 42,
                lon: -72
              },
              bottom_right: {
                lat: 40,
                lon: -74
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_point"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "text": "Geopoint as an object using GeoJSON format",
      "location": { __"type": "Point",
        "coordinates": [-71.34, 41.12]
      }
    }
    
    PUT my-index-000001/_doc/2
    {
      "text": "Geopoint as a WKT POINT primitive",
      "location" : "POINT (-71.34 41.12)" __}
    
    PUT my-index-000001/_doc/3
    {
      "text": "Geopoint as an object with 'lat' and 'lon' keys",
      "location": { __"lat": 41.12,
        "lon": -71.34
      }
    }
    
    PUT my-index-000001/_doc/4
    {
      "text": "Geopoint as an array",
      "location": [ -71.34, 41.12 ] __}
    
    PUT my-index-000001/_doc/5
    {
      "text": "Geopoint as a string",
      "location": "41.12,-71.34" __}
    
    PUT my-index-000001/_doc/6
    {
      "text": "Geopoint as a geohash",
      "location": "drm3btev3e86" __}
    
    GET my-index-000001/_search
    {
      "query": {
        "geo_bounding_box": { __"location": {
            "top_left": {
              "lat": 42,
              "lon": -72
            },
            "bottom_right": {
              "lat": 40,
              "lon": -74
            }
          }
        }
      }
    }

__

|

Geopoint表示为对象，采用GeoJSON格式，带有"类型"和"坐标"键。   ---|---    __

|

Geopoint表示为已知文本POINT，格式为："POINT(lon lat)"__

|

Geopoint表示为一个对象，带有"lat"和"lon"键。   __

|

Geopoint 表示为数组，格式为： [ 'lon'， 'lat'] __

|

Geopoint 表示为格式为"lat，lon"的字符串。   __

|

地理点表示为地理哈希。   __

|

一个地理边界框查询，用于查找框内的所有地理点。   ### 以数组或字符串表示的地理点

请注意，字符串geopoints的排序顺序为"lat，lon"，而arraygeopoints，GeoJSON和WKT的顺序相反："lon，lat"。

其原因是历史性的。地理学家传统上在"经度"之前写"纬度"，而最近为地理数据指定的格式，如GeoJSON和众所周知的文本，将"经度"排序在"纬度"之前(东向先于北)，以匹配在"y"之前对"x"进行排序的数学惯例。

一个点可以表示为ageohash。地理哈希是纬度和经度交错位的base32编码字符串。地理哈希中的每个字符都会将额外的 5 位添加到精度上。因此，哈希值越长，它就越精确。对于索引目的，地理哈希被转换为纬度 - 经度对。在此过程中，仅使用前 12 个字符，因此在地理哈希中指定超过 12 个字符不会提高精度。这 12 个字符提供 60 位，这应该将可能的错误减少到 2 厘米以下。

### "geo_point"字段的参数

"geo_point"字段接受以下参数：

"ignore_malformed"

|

如果为"true"，则忽略格式错误的地理点。如果为"false"(默认值)，则格式错误的地理点将引发异常并拒绝整个文档。如果地理点的纬度在纬度 -90 ⇐纬度 ⇐ 90 的范围之外，或者其经度在 -180 ⇐经度⇐ 180\ 范围之外，则认为地理点格式不正确。请注意，如果使用"script"参数，则无法设置此选项。   ---|--- "ignore_z_value"

|

如果"true"(默认值)将接受三个维度点(存储在源中)，但仅索引纬度和经度值;第三个维度被忽略。如果为"false"，则包含超过纬度和经度(二维)值的地理点将引发异常并拒绝整个文档。请注意，如果使用"script"参数，则无法设置此选项。   "索引"

|

该字段是否应该快速搜索？接受"真"(默认值)和"假"。仅启用了"doc_values"的字段仍然可以查询，尽管速度较慢。   "null_value"

|

接受替换任何显式"空"值的地理点值。默认为"null"，表示该字段被视为缺失。请注意，如果使用"script"参数，则无法设置此选项。   "on_script_error"

|

定义当由"script"参数定义的脚本在索引时引发错误时要执行的操作。接受"fail"(默认)，这将导致整个文档被拒绝，以及"继续"，这将在文档的"_ignored"元数据字段中注册字段并继续索引。仅当还设置了"脚本"字段时，才能设置此参数。   "脚本"

|

如果设置了此参数，则字段将索引此脚本生成的值，而不是直接从源读取值。如果在输入文档上为此字段设置了值，则该文档将被拒绝并显示错误。脚本的格式与其运行时等效的格式相同，并且应以一对(纬度，纬度)双精度值的形式发出点。   ### 使用地理点铭文编辑

在脚本中访问地理点的值时，该值将作为"GeoPoint"对象返回，该对象允许分别访问".lat"和".lon"值：

    
    
    def geopoint = doc['location'].value;
    def lat      = geopoint.lat;
    def lon      = geopoint.lon;

出于性能原因，最好直接访问纬度/纬度值：

    
    
    def lat      = doc['location'].lat;
    def lon      = doc['location'].lon;

### 合成源

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"geo_point"字段在其默认配置中支持合成"_source"。合成"_source"不能与"ignore_malformed"、"copy_to"一起使用，也不能禁用"doc_values"。

合成源始终对"geo_point"字段进行排序(首先按纬度，然后按经度)，并将它们降低到存储的精度。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            point: {
              type: 'geo_point'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        point: [
          {
            lat: -90,
            lon: -80
          },
          {
            lat: 10,
            lon: 30
          }
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "point": { "type": "geo_point" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "point": [
        {"lat":-90, "lon":-80},
        {"lat":10, "lon":30}
      ]
    }

将成为：

    
    
    {
      "point": [
        {"lat":-90.0, "lon":-80.00000000931323},
        {"lat":9.999999990686774, "lon":29.999999972060323}
       ]
    }

[« Flattened field type](flattened.md) [Geoshape field type »](geo-
shape.md)
