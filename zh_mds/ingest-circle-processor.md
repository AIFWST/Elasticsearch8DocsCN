

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Bytes processor](bytes-processor.md) [Community ID processor
»](community-id-processor.md)

## 圆处理器

将形状的圆形定义转换为近似形状的常规多边形。

**表 6.圆形处理器选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要解释为圆的字段。WKT 格式的字符串或 GeoJSON 的映射。   "target_field"

|

no

|

`field`

|

要将多边形形状分配到的字段(默认情况下为"字段")将就地更新为"ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将静默退出，而不修改文档"error_distance"

|

yes

|

-

|

从中心到侧面的内切距离与圆的半径(对于"geo_shape"以米为单位，对于"形状"以无单位为单位)"shape_type"之间的差值

|

yes

|

-

|

处理圆时要使用哪种字段映射类型："geo_shape"或"形状""描述"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。   ！错误距离

    
    
    response = client.indices.create(
      index: 'circles',
      body: {
        mappings: {
          properties: {
            circle: {
              type: 'geo_shape'
            }
          }
        }
      }
    )
    puts response
    
    response = client.ingest.put_pipeline(
      id: 'polygonize_circles',
      body: {
        description: 'translate circle to polygon',
        processors: [
          {
            circle: {
              field: 'circle',
              error_distance: 28,
              shape_type: 'geo_shape'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT circles
    {
      "mappings": {
        "properties": {
          "circle": {
            "type": "geo_shape"
          }
        }
      }
    }
    
    PUT _ingest/pipeline/polygonize_circles
    {
      "description": "translate circle to polygon",
      "processors": [
        {
          "circle": {
            "field": "circle",
            "error_distance": 28.0,
            "shape_type": "geo_shape"
          }
        }
      ]
    }

使用上面的管道，我们可以尝试将文档索引到"circles"索引中。该圆可以表示为 WKT 圆或 GeoJSON 圆。生成的面将使用与输入圆相同的格式进行表示和索引。WKT将被转换为WKT多边形，GeoJSON圆圈将被转换为GeoJSON多边形。

不支持包含极点的圆。

### 示例：在已知文本中定义的圆

在此示例中，以 WKT 格式定义的圆被索引

    
    
    response = client.index(
      index: 'circles',
      id: 1,
      pipeline: 'polygonize_circles',
      body: {
        circle: 'CIRCLE (30 10 40)'
      }
    )
    puts response
    
    response = client.get(
      index: 'circles',
      id: 1
    )
    puts response
    
    
    PUT circles/_doc/1?pipeline=polygonize_circles
    {
      "circle": "CIRCLE (30 10 40)"
    }
    
    GET circles/_doc/1

来自上述索引请求的响应：

    
    
    {
      "found": true,
      "_index": "circles",
      "_id": "1",
      "_version": 1,
      "_seq_no": 22,
      "_primary_term": 1,
      "_source": {
        "circle": "POLYGON ((30.000365257263184 10.0, 30.000111397193788 10.00034284530941, 29.999706043744222 10.000213571721195, 29.999706043744222 9.999786428278805, 30.000111397193788 9.99965715469059, 30.000365257263184 10.0))"
      }
    }

### 示例：在 GeoJSON 中定义的圆圈

在此示例中，以 GeoJSON 格式定义的圆圈已编制索引

    
    
    response = client.index(
      index: 'circles',
      id: 2,
      pipeline: 'polygonize_circles',
      body: {
        circle: {
          type: 'circle',
          radius: '40m',
          coordinates: [
            30,
            10
          ]
        }
      }
    )
    puts response
    
    response = client.get(
      index: 'circles',
      id: 2
    )
    puts response
    
    
    PUT circles/_doc/2?pipeline=polygonize_circles
    {
      "circle": {
        "type": "circle",
        "radius": "40m",
        "coordinates": [30, 10]
      }
    }
    
    GET circles/_doc/2

来自上述索引请求的响应：

    
    
    {
      "found": true,
      "_index": "circles",
      "_id": "2",
      "_version": 1,
      "_seq_no": 22,
      "_primary_term": 1,
      "_source": {
        "circle": {
          "coordinates": [
            [
              [30.000365257263184, 10.0],
              [30.000111397193788, 10.00034284530941],
              [29.999706043744222, 10.000213571721195],
              [29.999706043744222, 9.999786428278805],
              [30.000111397193788, 9.99965715469059],
              [30.000365257263184, 10.0]
            ]
          ],
          "type": "Polygon"
        }
      }
    }

### 准确性注意事项

表示圆的面的精度定义为"error_distance"。此差值越小，多边形越接近完美圆。

下表旨在帮助捕获圆的半径如何影响给定不同输入的多边形的结果边数。

最小边数为"4"，最大为"1000"。

**表 7.圆形处理器精度**

error_distance |半径(米) |多边形边数 ---|---|--- 1.00

|

1.0

|

4    1.00

|

10.0

|

14    1.00

|

100.0

|

45    1.00

|

1000.0

|

141    1.00

|

10000.0

|

445    1.00

|

100000.0

|

1000 « 字节处理器 社区 ID 处理器»