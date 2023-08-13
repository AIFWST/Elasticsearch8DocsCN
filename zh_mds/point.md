

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Percolator field type](percolator.md) [Range field types »](range.md)

## 点字段类型

"点"数据类型有助于索引和搜索落在二维平面坐标系中的任意"x，y"对。

您可以使用形状查询使用此类型查询文档。

与geo_shape和geo_point一样，可以在GeoJSON和No-KnownText格式中指定"点"。但是，出于方便和历史原因，还支持许多其他格式。总共有五种方式可以指定笛卡尔点，如下所示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
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
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        text: 'Point as an object using GeoJSON format',
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
        text: 'Point as a WKT POINT primitive',
        location: 'POINT (-71.34 41.12)'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 3,
      body: {
        text: "Point as an object with 'x' and 'y' keys",
        location: {
          x: -71.34,
          y: 41.12
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 4,
      body: {
        text: 'Point as an array',
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
        text: 'Point as a string',
        location: '-71.34,41.12'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "point"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "text": "Point as an object using GeoJSON format",
      "location": { __"type": "Point",
        "coordinates": [-71.34, 41.12]
      }
    }
    
    PUT my-index-000001/_doc/2
    {
      "text": "Point as a WKT POINT primitive",
      "location" : "POINT (-71.34 41.12)" __}
    
    PUT my-index-000001/_doc/3
    {
      "text": "Point as an object with 'x' and 'y' keys",
      "location": { __"x": -71.34,
        "y": 41.12
      }
    }
    
    PUT my-index-000001/_doc/4
    {
      "text": "Point as an array",
      "location": [ -71.34, 41.12 ] __}
    
    PUT my-index-000001/_doc/5
    {
      "text": "Point as a string",
      "location": "-71.34,41.12" __}

__

|

点表示为对象，采用 GeoJSON 格式，带有"类型"和"坐标"键。   ---|---    __

|

点表示为已知文本点，格式为："POINT(x y)"__

|

点表示为对象，带有"x"和"y"键。   __

|

点表示为数组，格式为：[ 'x'， 'y'] __

|

点表示为字符串，格式为："x，y"。   与地理点字段类型的情况不同，坐标"x"和"y"的顺序对于上述所有格式都是相同的。

提供给索引器的坐标是单精度浮点值，因此该字段保证与 Java 虚拟机(通常为"1E-38")提供的相同精度。

### "点"字段的参数

"点"字段接受以下参数：

"ignore_malformed"

|

如果为"true"，则忽略格式错误的点。如果为"false"(默认值)，则格式错误的点将引发异常并拒绝整个文档。   ---|--- "ignore_z_value"

|

如果"true"(默认值)将接受三个维度点(存储在源中)，但只会索引 x 和 y 值;第三个维度被忽略。如果 'false'，则包含任何超过 x 和 y(二维)值的点将引发异常并拒绝整个文档。   "null_value"

|

接受替换任何显式"null"值的点值。默认为"null"，表示该字段被视为缺失。   ### 排序和检索点编辑

目前无法直接对点进行排序或检索其字段。"点"值只能通过"_source"字段检索。

[« Percolator field type](percolator.md) [Range field types »](range.md)
