

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Search-as-you-type field type](search-as-you-type.md) [Text type family
»](text.md)

## 形状字段类型

"shape"数据类型有助于使用任意的"x，y"笛卡尔形状(如矩形和多边形)进行索引和搜索。它可用于索引和查询坐标落在二维平面坐标系中的几何。

您可以使用形状查询使用此类型查询文档。

#### 映射选项

与"geo_shape"字段类型一样，"形状"字段映射将 GeoJSON 或已知文本 (WKT) 几何对象映射到形状类型。若要启用它，用户必须将字段显式映射到形状类型。

选项 |描述 |默认---|---|---"方向"

|

(可选)定义如何解释多边形/多多边形的顶点顺序。此参数定义两个坐标系规则(右侧或左侧)之一，每个坐标系规则都可以通过三种不同的方式指定。1. 右手尺："右"、"逆时针"、"逆时针"，2\。左手规则："左"，"cw"，"顺时针"。默认方向("逆时针")符合OGC标准，该标准按逆时针顺序定义外环顶点，内环顶点(孔)按顺时针顺序定义。在"geo_shape"映射中设置此参数会显式设置"geo_shape"字段坐标列表的顶点顺序，但可以在每个单独的 GeoJSON 或 WKT文档中覆盖。

|

"CCW" "ignore_malformed"

|

如果为 true，则忽略格式错误的 GeoJSON 或 WKT 形状。如果为 false(默认值)，则格式错误的 GeoJSON 和 WKT 形状将引发异常并拒绝整个文档。

|

"假""ignore_z_value"

|

如果"true"(默认值)将接受三个维度点(存储在源中)，但仅索引纬度和经度值;第三个维度被忽略。如果为"false"，则包含超过纬度和经度(二维)值的地理点将引发异常并拒绝整个文档。

|

"真""胁迫"

|

如果多边形中的未闭合线性环为"真"，则会自动闭合。

|

'false' #### 索引方法编辑

与"geo_shape"一样，"shape"字段类型通过将几何分解为三角形网格并将每个三角形索引为 aBKD 树中的 7 维点来编制索引。提供给索引器的坐标是单精度浮点值，因此该字段保证与 Java 虚拟机(通常为"1E-38")提供的相同精度。对于多边形/多多边形，曲面细分器的性能主要取决于定义几何图形的顶点数。

**重要事项**

"CONTAINS"关系查询 - 使用 ElasticSearch 7.5.0 或更高版本创建的索引支持将"关系"定义为"包含"的"形状"查询。

#####Example

    
    
    response = client.indices.create(
      index: 'example',
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
    
    
    PUT /example
    {
      "mappings": {
        "properties": {
          "geometry": {
            "type": "shape"
          }
        }
      }
    }

此映射定义将几何字段映射到形状类型。索引器对顶点值使用单精度浮点数，因此保证精度与 Java 虚拟机提供的"浮点数"值大致(通常为 1E-38)相同。

#### 输入结构

可以使用GeoJSON或已知文本(WKT)格式表示形状。下表提供了GeoJSON和WKT到Elasticsearch类型的映射：

地理数据类型 |WKT 类型 |弹性搜索类型 |描述 ---|---|---|--- '点'

|

`POINT`

|

`point`

|

单个"x， y"坐标。   "线字符串"

|

`LINESTRING`

|

`linestring`

|

给定两个或更多点的任意线。   "多边形"

|

`POLYGON`

|

`polygon`

|

一个 _closed_ 多边形，其第一个和最后一个点必须匹配，因此需要"n +1"顶点来创建"n"边多边形和至少"4"顶点。   "多点"

|

`MULTIPOINT`

|

`multipoint`

|

一组未连接但可能相关的点。   '多线字符串'

|

`MULTILINESTRING`

|

`multilinestring`

|

单独线串的数组。   "多多边形"

|

`MULTIPOLYGON`

|

`multipolygon`

|

独立多边形的数组。   "几何收藏"

|

`GEOMETRYCOLLECTION`

|

`geometrycollection`

|

类似于"multi*"形状的形状集合，但多个类型可以共存(例如，点和线字符串)。   "不适用"

|

`BBOX`

|

`envelope`

|

通过仅指定左上角和右下角点来指定的边框或封套。   对于所有类型，内部"类型"和"坐标"字段都是必需的。

在GeoJSON和WKT以及Elasticsearch中，正确的坐标顺序是坐标数组中的(X，Y)**。这与通常使用口语纬度、经度(Y、X)排序的许多地理空间API(例如"geo_shape")不同。

##### 点

点是笛卡尔"x，y"空间中的单个坐标。它可以表示感兴趣的项目在虚拟世界或投影空间中的位置。以下是 GeoJSON 中一个点的示例。

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "point",
        "coordinates" : [-377.03653, 389.897676]
      }
    }

以下是 WKT 中一个点的示例：

    
    
    POST /example/_doc
    {
      "location" : "POINT (-377.03653 389.897676)"
    }

##### 行字符串

由两个或多个位置的数组定义的"线串"。通过仅指定两个点，"线串"将表示一条直线。指定两个以上的点将创建任意路径。以下是 GeoJSON 中 LineString 的示例。

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "linestring",
        "coordinates" : [[-377.03653, 389.897676], [-377.009051, 389.889939]]
      }
    }

以下是 WKT 中的 LineString 示例：

    
    
    POST /example/_doc
    {
      "location" : "LINESTRING (-377.03653 389.897676, -377.009051 389.889939)"
    }

##### 多边形

面由点列表的列表定义。每个(外部)列表中的第一个点和最后一个点必须相同(面必须闭合)。以下是 GeoJSON 中多边形的示例。

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "polygon",
        "coordinates" : [
          [ [1000.0, -1001.0], [1001.0, -1001.0], [1001.0, -1000.0], [1000.0, -1000.0], [1000.0, -1001.0] ]
        ]
      }
    }

以下是 WKT 中多边形的示例：

    
    
    POST /example/_doc
    {
      "location" : "POLYGON ((1000.0 -1001.0, 1001.0 -1001.0, 1001.0 -1000.0, 1000.0 -1000.0, 1000.0 -1001.0))"
    }

第一个数组表示多边形的外部边界，其他数组表示内部形状("孔")。以下是带有孔的多边形的 GeoJSON 示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "polygon",
        "coordinates" : [
          [ [1000.0, -1001.0], [1001.0, -1001.0], [1001.0, -1000.0], [1000.0, -1000.0], [1000.0, -1001.0] ],
          [ [1000.2, -1001.2], [1000.8, -1001.2], [1000.8, -1001.8], [1000.2, -1001.8], [1000.2, -1001.2] ]
        ]
      }
    }

以下是在 WKT 中带有孔的多边形的示例：

    
    
    POST /example/_doc
    {
      "location" : "POLYGON ((1000.0 1000.0, 1001.0 1000.0, 1001.0 1001.0, 1000.0 1001.0, 1000.0 1000.0), (1000.2 1000.2, 1000.8 1000.2, 1000.8 1000.8, 1000.2 1000.8, 1000.2 1000.2))"
    }

**重要提示：** WKT 不强制执行顶点的特定顺序。GeoJSON 要求外部多边形必须逆时针，内部形状必须顺时针，这符合开放地理空间联盟 (OGC) 简单特征访问的顶点排序规范。

默认情况下，Elasticsearch 需要按逆时针(右手尺)顺序排列顶点。如果数据按顺时针顺序(左手规则)提供，用户可以在字段映射中更改"方向"参数，也可以作为随文档提供的参数进行更改。

以下是覆盖文档上的"方向"参数的示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "polygon",
        "orientation" : "clockwise",
        "coordinates" : [
          [ [1000.0, 1000.0], [1000.0, 1001.0], [1001.0, 1001.0], [1001.0, 1000.0], [1000.0, 1000.0] ]
        ]
      }
    }

##### 多点

以下是 GeoJSON 点列表的示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "multipoint",
        "coordinates" : [
          [1002.0, 1002.0], [1003.0, 2000.0]
        ]
      }
    }

以下是 WKT 点列表的示例：

    
    
    POST /example/_doc
    {
      "location" : "MULTIPOINT (1002.0 2000.0, 1003.0 2000.0)"
    }

##### 多行字符串

以下是 GeoJSON 线串列表的示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "multilinestring",
        "coordinates" : [
          [ [1002.0, 200.0], [1003.0, 200.0], [1003.0, 300.0], [1002.0, 300.0] ],
          [ [1000.0, 100.0], [1001.0, 100.0], [1001.0, 100.0], [1000.0, 100.0] ],
          [ [1000.2, 100.2], [1000.8, 100.2], [1000.8, 100.8], [1000.2, 100.8] ]
        ]
      }
    }

以下是 WKT 线串列表的示例：

    
    
    POST /example/_doc
    {
      "location" : "MULTILINESTRING ((1002.0 200.0, 1003.0 200.0, 1003.0 300.0, 1002.0 300.0), (1000.0 100.0, 1001.0 100.0, 1001.0 100.0, 1000.0 100.0), (1000.2 0.2, 1000.8 100.2, 1000.8 100.8, 1000.2 100.8))"
    }

##### 多多边形

以下是 GeoJSON 多边形列表的示例(第二个多边形包含一个洞)：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "multipolygon",
        "coordinates" : [
          [ [[1002.0, 200.0], [1003.0, 200.0], [1003.0, 300.0], [1002.0, 300.0], [1002.0, 200.0]] ],
          [ [[1000.0, 200.0], [1001.0, 100.0], [1001.0, 100.0], [1000.0, 100.0], [1000.0, 100.0]],
            [[1000.2, 200.2], [1000.8, 100.2], [1000.8, 100.8], [1000.2, 100.8], [1000.2, 100.2]] ]
        ]
      }
    }

以下是 WKT 多边形列表的示例(第二个多边形包含孔)：

    
    
    POST /example/_doc
    {
      "location" : "MULTIPOLYGON (((1002.0 200.0, 1003.0 200.0, 1003.0 300.0, 1002.0 300.0, 102.0 200.0)), ((1000.0 100.0, 1001.0 100.0, 1001.0 100.0, 1000.0 100.0, 1000.0 100.0), (1000.2 100.2, 1000.8 100.2, 1000.8 100.8, 1000.2 100.8, 1000.2 100.2)))"
    }

##### 几何集合

以下是 GeoJSON 几何对象集合的示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type": "geometrycollection",
        "geometries": [
          {
            "type": "point",
            "coordinates": [1000.0, 100.0]
          },
          {
            "type": "linestring",
            "coordinates": [ [1001.0, 100.0], [1002.0, 100.0] ]
          }
        ]
      }
    }

以下是 WKT 几何对象集合的示例：

    
    
    POST /example/_doc
    {
      "location" : "GEOMETRYCOLLECTION (POINT (1000.0 100.0), LINESTRING (1001.0 100.0, 1002.0 100.0))"
    }

#####Envelope

Elasticsearch 支持"包络"类型，该类型由形状左上角和右下角的坐标组成，以表示格式为"[[minX， maxY]， [maxX， minY]]"的边界矩形：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "envelope",
        "coordinates" : [ [1000.0, 100.0], [1001.0, 100.0] ]
      }
    }

以下是使用 WKT BBOX 格式的信封示例：

**注：** WKT 规范要求以下顺序：minLon、maxLon、maxLat、minLat。

    
    
    POST /example/_doc
    {
      "location" : "BBOX (1000.0, 1002.0, 2000.0, 1000.0)"
    }

#### 排序和检索索引形状

由于形状的输入结构和索引表示形式复杂，目前无法对形状进行排序或直接检索其字段。"形状"值只能通过"_source"字段检索。

[« Search-as-you-type field type](search-as-you-type.md) [Text type family
»](text.md)
