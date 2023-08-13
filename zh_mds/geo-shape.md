

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Geopoint field type](geo-point.md) [Histogram field type
»](histogram.md)

## 地形字段类型

"geo_shape"数据类型有助于索引和搜索任意地理形状，例如矩形、线和多边形。如果正在编制索引的数据包含的形状不仅仅是点，则必须使用此映射。如果数据仅包含点，则可以将其索引为"geo_point"或"geo_shape"。

可以使用使用此类型的文档：

* 查找以下位置的地理形状：

    * a [bounding box](query-dsl-geo-bounding-box-query.html "Geo-bounding box query")
    * a certain [distance](query-dsl-geo-distance-query.html "Geo-distance query") of a central point 
    * a [`geo_shape` query](query-dsl-geo-shape-query.html "Geoshape query") (for example, intersecting polygons). 

* 按地理网格汇总文件：

    * either [`geo_hash`](search-aggregations-bucket-geohashgrid-aggregation.html "Geohash grid aggregation")
    * or [`geo_tile`](search-aggregations-bucket-geotilegrid-aggregation.html "Geotile grid aggregation"). 

"geo_shape"字段不支持"geo_hex"网格上的网格聚合。

#### 映射选项

"geo_shape"映射将GeoJSON或WKT几何对象映射到"geo_shape"类型。若要启用它，用户必须将字段显式映射到"geo_shape"类型。

选项 |描述 |默认---|---|---"方向"

|

自选。字段的 WKT 面的默认方向。

此参数仅设置并返回"RIGHT"(逆时针)或"LEFT"(顺时针)值。但是，您可以通过多种方式指定任一值。

要设置"RIGHT"，请使用以下参数之一或其大写变体：

* "右" * "逆时针" * "CCW"

要设置"LEFT"，请使用以下参数之一或其大写变体：

* "左" * "顺时针" * "CW"

|

"对" "ignore_malformed"

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

"假""索引"

|

该字段是否应该快速搜索？接受"真"(默认值)和"假"。仅启用了"doc_values"的字段仍然可以查询，尽管速度较慢。

|

"真" "doc_values"

|

是否应以列步幅方式将字段存储在磁盘上，以便以后可用于聚合或脚本编写？

|

'true' #### 索引方法编辑

通过将形状分解为三角形网格并将每个三角形索引为 BKD 树中的 7 维点来索引地理形状类型。这提供了近乎完美的空间分辨率(精度低至 1e-7 十进制度度)，因为所有空间关系都是使用原始形状的编码矢量表示来计算的。细分器的性能主要取决于定义多边形/多多边形的顶点数。

#####Example

    
    
    response = client.indices.create(
      index: 'example',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'geo_shape'
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
          "location": {
            "type": "geo_shape"
          }
        }
      }
    }

#### 输入结构

可以使用GeoJSON或已知文本(WKT)格式表示形状。下表提供了GeoJSON和WKT到Elasticsearch类型的映射：

地理数据类型 |WKT 类型 |弹性搜索类型 |描述 ---|---|---|--- '点'

|

`POINT`

|

`point`

|

单个地理坐标。注意：Elasticsearch 仅使用 WGS-84 坐标。   "线字符串"

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

类似于"multi*"形状的 GeoJSON 形状，但多个类型可以共存(例如，点和线字符串)。   "不适用"

|

`BBOX`

|

`envelope`

|

通过仅指定左上角和右下角点来指定的边框或封套。   对于所有类型，内部"类型"和"坐标"字段都是必需的。

在GeoJSON和WKT以及Elasticsearch中，正确的坐标顺序是坐标数组中的经度，纬度(X，Y)**。这与许多地理空间API(例如，谷歌地图)不同，后者通常使用口语化的纬度，经度(Y，X)。

##### 点

点是单个地理坐标，例如建筑物的位置或智能手机的地理位置 API 给出的当前位置。下面是 GeoJSON 中一个点的示例。

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "Point",
        "coordinates" : [-77.03653, 38.897676]
      }
    }

以下是 WKT 中一个点的示例：

    
    
    POST /example/_doc
    {
      "location" : "POINT (-77.03653 38.897676)"
    }

##### 行字符串

由两个或多个位置的数组定义的线串。通过仅指定两个点，线串将表示一条直线。指定两个以上的点将创建任意路径。以下是 GeoJSON 中的行字符串示例。

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "LineString",
        "coordinates" : [[-77.03653, 38.897676], [-77.009051, 38.889939]]
      }
    }

以下是 WKT 中的线串示例：

    
    
    POST /example/_doc
    {
      "location" : "LINESTRING (-77.03653 38.897676, -77.009051 38.889939)"
    }

上面的线串将绘制一条从白宫到美国国会大厦的直线。

##### 多边形

面由点列表的列表定义。每个(外部)列表中的第一个点和最后一个点必须相同(面必须闭合)。以下是 GeoJSON 中多边形的示例。

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "Polygon",
        "coordinates" : [
          [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]
        ]
      }
    }

以下是 WKT 中多边形的示例：

    
    
    POST /example/_doc
    {
      "location" : "POLYGON ((100.0 0.0, 101.0 0.0, 101.0 1.0, 100.0 1.0, 100.0 0.0))"
    }

第一个数组表示多边形的外部边界，其他数组表示内部形状("孔")。以下是带有孔的多边形的 GeoJSON 示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "Polygon",
        "coordinates" : [
          [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ],
          [ [100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2] ]
        ]
      }
    }

以下是在 WKT 中带有孔的多边形的示例：

    
    
    POST /example/_doc
    {
      "location" : "POLYGON ((100.0 0.0, 101.0 0.0, 101.0 1.0, 100.0 1.0, 100.0 0.0), (100.2 0.2, 100.8 0.2, 100.8 0.8, 100.2 0.8, 100.2 0.2))"
    }

##### 多边形方向

多边形的方向指示其顶点的顺序："RIGHT"(逆时针)或"LEFT"(顺时针)。Elasticsearch 使用多边形的方向来确定它是否穿过国际日期变更线(+/-180°经度)。

您可以使用"方向"映射参数为 WKT 多边形设置默认方向。这是因为 WKT 规范未指定或强制实施默认方向。

GeoJSON 多边形使用默认方向"RIGHT"，而不考虑"方向"映射参数的值。这是因为 GeoJSON 规范要求外部多边形使用逆时针方向，内部形状使用顺时针方向。

您可以使用文档级"方向"参数覆盖 GeoJSON 多边形的默认方向。例如，以下索引请求指定文档级"方向"为"LEFT"。

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "Polygon",
        "orientation" : "LEFT",
        "coordinates" : [
          [ [-177.0, 10.0], [176.0, 15.0], [172.0, 0.0], [176.0, -15.0], [-177.0, -10.0], [-177.0, 10.0] ]
        ]
      }
    }

Elasticsearch 仅使用多边形的方向来确定它是否越过国际日期变更线。如果面的最小经度与最大经度之间的差异小于 180°，则面不会穿过日期变更线，并且其方向不起作用。

如果多边形的最小经度和最大经度之间的差异为 180° 或更大，Elasticsearch 会检查多边形的文档级"方向"是否与默认方向不同。如果方向不同，Elasticsearch 会认为多边形与国际日期变更线相交，并在日期变更线上分割多边形。

##### 多点

以下是 GeoJSON 点列表的示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "MultiPoint",
        "coordinates" : [
          [102.0, 2.0], [103.0, 2.0]
        ]
      }
    }

以下是 WKT 点列表的示例：

    
    
    POST /example/_doc
    {
      "location" : "MULTIPOINT (102.0 2.0, 103.0 2.0)"
    }

##### 多行字符串

以下是 GeoJSON 线串列表的示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "MultiLineString",
        "coordinates" : [
          [ [102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0] ],
          [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0] ],
          [ [100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8] ]
        ]
      }
    }

以下是 WKT 线串列表的示例：

    
    
    POST /example/_doc
    {
      "location" : "MULTILINESTRING ((102.0 2.0, 103.0 2.0, 103.0 3.0, 102.0 3.0), (100.0 0.0, 101.0 0.0, 101.0 1.0, 100.0 1.0), (100.2 0.2, 100.8 0.2, 100.8 0.8, 100.2 0.8))"
    }

##### 多多边形

以下是 GeoJSON 多边形列表的示例(第二个多边形包含一个洞)：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "MultiPolygon",
        "coordinates" : [
          [ [[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]] ],
          [ [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
            [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]] ]
        ]
      }
    }

以下是 WKT 多边形列表的示例(第二个多边形包含孔)：

    
    
    POST /example/_doc
    {
      "location" : "MULTIPOLYGON (((102.0 2.0, 103.0 2.0, 103.0 3.0, 102.0 3.0, 102.0 2.0)), ((100.0 0.0, 101.0 0.0, 101.0 1.0, 100.0 1.0, 100.0 0.0), (100.2 0.2, 100.8 0.2, 100.8 0.8, 100.2 0.8, 100.2 0.2)))"
    }

##### 几何集合

以下是 GeoJSON 几何对象集合的示例：

    
    
    POST /example/_doc
    {
      "location" : {
        "type": "GeometryCollection",
        "geometries": [
          {
            "type": "Point",
            "coordinates": [100.0, 0.0]
          },
          {
            "type": "LineString",
            "coordinates": [ [101.0, 0.0], [102.0, 1.0] ]
          }
        ]
      }
    }

以下是 WKT 几何对象集合的示例：

    
    
    POST /example/_doc
    {
      "location" : "GEOMETRYCOLLECTION (POINT (100.0 0.0), LINESTRING (101.0 0.0, 102.0 1.0))"
    }

#####Envelope

Elasticsearch 支持"包络"类型，该类型由形状左上角和右下角的坐标组成，以表示格式为"[[minLon， maxLat]， [maxLon， minLat]]"的边界矩形：

    
    
    POST /example/_doc
    {
      "location" : {
        "type" : "envelope",
        "coordinates" : [ [100.0, 1.0], [101.0, 0.0] ]
      }
    }

以下是使用 WKT BBOX 格式的信封示例：

**注：** WKT 规范要求以下顺序：minLon、maxLon、maxLat、minLat。

    
    
    POST /example/_doc
    {
      "location" : "BBOX (100.0, 102.0, 2.0, 0.0)"
    }

#####Circle

GeoJSON 和 WKT 都不支持点半径圆类型。相反，请使用 acircle 采集处理器将圆近似为"多边形"。

#### 排序和检索索引形状

由于形状的输入结构和索引表示形式复杂，目前无法对形状进行排序或直接检索其字段。"geo_shape"值只能通过"_source"字段检索。

[« Geopoint field type](geo-point.md) [Histogram field type
»](histogram.md)
