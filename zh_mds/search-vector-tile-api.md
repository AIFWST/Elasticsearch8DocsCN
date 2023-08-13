

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Ranking evaluation API](search-rank-eval.md) [Search Application APIs
»](search-application-apis.md)

## 矢量图块搜索API

在矢量切片中搜索地理空间值。以二进制地图框矢量图块的形式返回结果。

    
    
    GET my-index/_mvt/my-geo-field/15/5271/12710

###Request

'获取 <target>/_mvt/<field>/<zoom><x>/<y>/'

'发布 <target>/_mvt/<field>/<zoom>/<x><y>/'

###Prerequisites

* 在使用此 API 之前，您应该熟悉 Mapbox 矢量图块规范。  * 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。有关跨集群搜索，请参阅配置具有安全性的远程集群。

### 路径参数

`<target>`

    

(必需，字符串)以逗号分隔的数据流、索引或别名列表进行搜索。支持通配符 ("*")。要搜索所有数据流和索引，请省略此参数或使用"*"或"_all"。

要搜索远程群集，请使用"<cluster>："<target>语法。请参阅_Searchacross clusters_。

`<field>`

    

(必需，字符串)包含要返回的地理空间值的字段。必须是"geo_point"或"geo_shape"字段。该字段必须启用文档值。不能是嵌套字段。

矢量切片本身不支持几何集合。对于"geo_shape"字段中的"几何集合"值，API 会为集合的每个元素返回"命中"图层要素。此行为可能会在将来的版本中更改。

`<zoom>`

     (Required, integer) Zoom level for the vector tile to search. Accepts `0`-`29`. 
`<x>`

     (Required, integer) X coordinate for the vector tile to search. 
`<y>`

     (Required, integer) Y coordinate for the vector tile to search. 

###Description

在内部，Elasticsearch 将矢量图块搜索 API 请求转换为包含以下内容的搜索：

* 对""的"geo_bounding_box"查询<field>。查询使用"/<zoom><x>/<y>"磁贴作为边界框。  * ""上的"geotile_grid"或"geohex_grid"聚合<field>。"grid_agg"参数确定聚合类型。聚合使用"/<zoom><x>/<y>"磁贴作为边界框。  * (可选)在""上聚合"geo_bounds<field>"。仅当"exact_bounds"参数为"true"时，搜索才包括此聚合。  * 如果可选参数"with_labels"为真，则内部搜索将包括一个动态运行时字段，该字段调用几何文档值的"getLabelPosition"函数。这样就可以生成包含建议几何标注的新点要素，例如，多面将只有一个标注。

例如，Elasticsearch 可以将带有"geotile"的"grid_agg"参数和"true"参数的"exact_bounds"参数的矢量切片搜索 API 请求转换为以下搜索：

    
    
    GET my-index/_search
    {
      "size": 10000,
      "query": {
        "geo_bounding_box": {
          "my-geo-field": {
            "top_left": {
              "lat": -40.979898069620134,
              "lon": -45
            },
            "bottom_right": {
              "lat": -66.51326044311186,
              "lon": 0
            }
          }
        }
      },
      "aggregations": {
        "grid": {
          "geotile_grid": {
            "field": "my-geo-field",
            "precision": 11,
            "size": 65536,
            "bounds": {
              "top_left": {
                "lat": -40.979898069620134,
                "lon": -45
              },
              "bottom_right": {
                "lat": -66.51326044311186,
                "lon": 0
              }
            }
          }
        },
        "bounds": {
          "geo_bounds": {
            "field": "my-geo-field",
            "wrap_longitude": false
          }
        }
      }
    }

API 以二进制映射框矢量块的形式返回结果。Mapbox矢量图块被编码为Google Protobufs(PBF)。默认情况下，切片包含三个图层：

* 一个"命中"图层，其中包含<field>与"geo_bounding_box"查询匹配的每个""值的要素。  * 一个"aggs"图层，其中包含"geotile_grid"或"geohex_grid"的每个单元格的特征。该图层仅包含具有匹配数据的像元的要素。  * 一个"元"层，包含：

    * A feature containing a bounding box. By default, this is the bounding box of the tile. 
    * Value ranges for any sub-aggregations on the `geotile_grid` or `geohex_grid`. 
    * Metadata for the search. 

API 仅返回可在其缩放级别显示的功能。例如，如果面要素的缩放级别没有区域，则 API 会省略该区域。

API 以 UTF-8 编码的 JSON 形式返回错误。

### 查询参数

您可以为此 API 指定多个选项作为查询参数或请求正文参数。如果同时指定这两个参数，则查询参数优先。

`exact_bounds`

    

(可选，布尔值)如果为"false"，则"元"层的特征是图块的边界框。默认为"假"。

如果为"true"，则"元"层的特征是由"geo_bounds"聚合生成的边界框。聚合在与"//"<field>磁贴相交的"/<zoom><x>/"值上运行，并将<y>"wrap_longitude"设置为"false"。生成的边界框可能大于矢量图块。

`extent`

     (Optional, integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. Defaults to `4096`. 

`buffer`

     (Optional, integer) Size, in pixels, of a clipping buffer outside the tile. This allows renderers to avoid outline artifacts from geometries that extend past the extent of the tile. Defaults to `5`. 

`grid_agg`

    

(可选，字符串)用于为 '' 创建网格的聚合<field>。

"grid_agg"的有效值

"地理图"(默认)

     [`geotile_grid`](search-aggregations-bucket-geotilegrid-aggregation.html "Geotile grid aggregation") aggregation. 
`geohex`

     [`geohex_grid`](search-aggregations-bucket-geohexgrid-aggregation.html "Geohex grid aggregation") aggregation. 

`grid_precision`

    

(可选，整数)"grid_agg"中单元格的精度级别。接受"0"-"8"。默认为"8"。如果为"0"，则结果不包括"aggs"图层。

"地理"的网格精度

对于"地理图块"的"grid_agg"，您可以使用"aggs"图层中的单元格作为较低缩放级别的切片。"grid_precision"表示通过这些单元格提供的其他缩放级别。最终精度的计算公式如下：

'<zoom> + grid_precision'

例如，如果""<zoom>为"7"，grid_precision"为"8"，则"geotile_grid"聚合将使用精度"15"。最大最终精度为"29"。

"grid_precision"还确定网格的单元格数量，如下所示：

'(2^grid_precision) x (2^grid_precision)'

例如，值"8"将磁贴划分为 256 x 256 个单元格的网格。"aggs"图层仅包含具有匹配数据的像元的特征。

"地质六角"的网格精度

对于"geohex"的"grid_agg"，Elasticsearch使用<zoom>""和"grid_precision"来计算最终精度，如下所示：

'<zoom> + grid_precision'

该精度决定了由"geohex"聚合产生的六边形单元的 H3 分辨率。下表映射了每个精度的 H3 分辨率。

例如，如果"<zoom>"为"3"，grid_precision"为"3"，则精度为"6"。在精度为"6"时，六边形单元格的 H3 分辨率为"2"。如果"<zoom>"为"3"，grid_precision"为"4"，则精度为"7"。在精度为"7"时，六边形单元格的 H3 分辨率为"3"。

精度 |独特的瓷砖箱 |H3 分辨率 |独特的六角箱 |比率 ---|---|---|---|--- 1

|

4

|

0

|

122

|

30.5    2

|

16

|

0

|

122

|

7.625    3

|

64

|

1

|

842

|

13.15625    4

|

256

|

1

|

842

|

3.2890625    5

|

1024

|

2

|

5882

|

5.744140625    6

|

4096

|

2

|

5882

|

1.436035156    7

|

16384

|

3

|

41162

|

2.512329102    8

|

65536

|

3

|

41162

|

0.6280822754    9

|

262144

|

4

|

288122

|

1.099098206    10

|

1048576

|

4

|

288122

|

0.2747745514    11

|

4194304

|

5

|

2016842

|

0.4808526039    12

|

16777216

|

6

|

14117882

|

0.8414913416    13

|

67108864

|

6

|

14117882

|

0.2103728354    14

|

268435456

|

7

|

98825162

|

0.3681524172    15

|

1073741824

|

8

|

691776122

|

0.644266719    16

|

4294967296

|

8

|

691776122

|

0.1610666797    17

|

17179869184

|

9

|

4842432842

|

0.2818666889    18

|

68719476736

|

10

|

33897029882

|

0.4932667053    19

|

274877906944

|

11

|

237279209162

|

0.8632167343    20

|

1099511627776

|

11

|

237279209162

|

0.2158041836    21

|

4398046511104

|

12

|

1660954464122

|

0.3776573213    22

|

17592186044416

|

13

|

11626681248842

|

0.6609003122    23

|

70368744177664

|

13

|

11626681248842

|

0.165225078    24

|

281474976710656

|

14

|

81386768741882

|

0.2891438866    25

|

1125899906842620

|

15

|

569707381193162

|

0.5060018015    26

|

4503599627370500

|

15

|

569707381193162

|

0.1265004504    27

|

18014398509482000

|

15

|

569707381193162

|

0.03162511259    28

|

72057594037927900

|

15

|

569707381193162

|

0.007906278149    29

|

288230376151712000

|

15

|

569707381193162

|

0.001976569537 六边形单元格在矢量图块上不完全对齐。某些单元格可能与多个矢量图块相交。为了计算每个精度的 H3 分辨率，Elasticsearch 将每个分辨率的六边形图格的平均密度与每个缩放级别的图块箱的平均密度进行比较。Elasticsearch使用最接近相应"地理分布"密度的H3分辨率。

`grid_type`

    

(可选，字符串)确定"aggs"图层中要素的几何类型。在"aggs"图层中，每个要素表示格网中的一个像元。

"grid_type"的有效值

"网格"(默认)

     Each feature is a `Polygon` of the cell's geometry. For a `grid_agg` of `geotile`, the feature is the cell's bounding box. For a `grid_agg` of `geohex`, the feature is the hexagonal cell's boundaries. 
`point`

     Each feature is a `Point` that's the centroid of the cell. 
`centroid`

     Each feature is a `Point` that's the centroid of the data within the cell. For complex geometries, the actual centroid may be outside the cell. In these cases, the feature is set to the closest point to the centroid inside the cell. 

`size`

     (Optional, integer) Maximum number of features to return in the `hits` layer. Accepts `0`-`10000`. Defaults to `10000`. If `0`, results don't include the `hits` layer. 

`track_total_hits`

    

(可选，整数或布尔值)与查询匹配的命中数准确计数。默认为"10000"。

如果为"true"，则以牺牲某些性能为代价返回确切的命中数。如果为"false"，则响应不包括与查询匹配的命中总数。

`with_labels`

    

(可选，布尔值)如果为 true，则命中图层和 aggs 图层将包含表示原始要素建议标注位置的附加点要素。

* "点"和"多点"要素将选择其中一个点。  * "面"和"多面"要素将生成一个点，即质心(如果位于面内)或从排序的三角形树中选择的面内的另一个点。  * "LineString"功能同样将提供一个从三角树中选择的大致中心点。  * 聚合结果将为每个聚合存储桶提供一个中心点。

原始要素中的所有属性也将复制到新标注要素。此外，可以使用标签"_mvt_label_position"来区分新功能。

### 请求正文

`aggs`

    

(可选，聚合对象)"grid_agg"的子聚合。支持以下聚合类型：

* "平均" * "箱线图" * "基数" * "扩展统计" * "最大值" * "中位数绝对偏差" * "最小" * "百分位数" * "百分位排名" * "统计" * "总和" * "值计数"

聚合名称不能以"_mvt_"开头。"_mvt_"前缀是为内部聚合保留的。

`exact_bounds`

    

(可选，布尔值)如果为"false"，则"元"层的特征是图块的边界框。默认为"假"。

如果为"true"，则"元"层的特征是由"geo_bounds"聚合生成的边界框。聚合在与"//"<field>磁贴相交的"/<zoom><x>/"值上运行，并将<y>"wrap_longitude"设置为"false"。生成的边界框可能大于矢量图块。

`extent`

     (Optional, integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. Defaults to `4096`. 
`buffer`

     (Optional, integer) Size, in pixels, of a clipping buffer outside the tile. This allows renderers to avoid outline artifacts from geometries that extend past the extent of the tile. Defaults to `5`. 
`fields`

    

(可选，字符串和对象的数组)要在"命中"图层中返回的字段。支持通配符 ("*")。

此参数不支持具有数组值的字段。具有数组值的字段可能会返回不一致的结果。

您可以将数组中的字段指定为字符串或对象。

"字段"对象的属性

`field`

     (Required, string) Field to return. Supports wildcards (`*`). 
`format`

    

(可选，字符串)日期和地理空间字段的格式。其他字段数据类型不支持此参数。

"日期"和"date_nanos"字段接受日期格式。"geo_point"和"geo_shape"字段接受：

"geojson"(默认)

     [GeoJSON](http://www.geojson.org)
`wkt`

     [Well Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
`mvt(<spec>)`

    

二进制地图框矢量图块。API 将磁贴作为 base64 编码的字符串返回。""<spec>的格式为"//<zoom><x><y>"，带有两个可选的后缀："@<extent>"和/或"："<buffer>。例如，"2/0/1"或"2/0/1@4096：5"。

"MVT"参数

`<zoom>`

     (Required, integer) Zoom level for the tile. Accepts `0`-`29`. 
`<x>`

     (Required, integer) X coordinate for the tile. 
`<y>`

     (Required, integer) Y coordinate for the tile. 
`<extent>`

     (Optional, integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. Defaults to `4096`. 
`<buffer>`

     (Optional, integer) Size, in pixels, of a clipping buffer outside the tile. This allows renderers to avoid outline artifacts from geometries that extend past the extent of the tile. Defaults to `5`. 

`grid_agg`

    

(可选，字符串)用于为 '' 创建网格的聚合<field>。

"grid_agg"的有效值

"地理图"(默认)

     [`geotile_grid`](search-aggregations-bucket-geotilegrid-aggregation.html "Geotile grid aggregation") aggregation. 
`geohex`

     [`geohex_grid`](search-aggregations-bucket-geohexgrid-aggregation.html "Geohex grid aggregation") aggregation. 

`grid_precision`

    

(可选，整数)"grid_agg"中单元格的精度级别。接受"0"-"8"。默认为"8"。如果为"0"，则结果不包括"aggs"图层。

"地理"的网格精度

对于"地理图块"的"grid_agg"，您可以使用"aggs"图层中的单元格作为较低缩放级别的切片。"grid_precision"表示通过这些单元格提供的其他缩放级别。最终精度的计算公式如下：

'<zoom> + grid_precision'

例如，如果""<zoom>为"7"，grid_precision"为"8"，则"geotile_grid"聚合将使用精度"15"。最大最终精度为"29"。

"grid_precision"还确定网格的单元格数量，如下所示：

'(2^grid_precision) x (2^grid_precision)'

例如，值"8"将磁贴划分为 256 x 256 个单元格的网格。"aggs"图层仅包含具有匹配数据的像元的特征。

"地质六角"的网格精度

对于"geohex"的"grid_agg"，Elasticsearch使用<zoom>""和"grid_precision"来计算最终精度，如下所示：

'<zoom> + grid_precision'

该精度决定了由"geohex"聚合产生的六边形单元的 H3 分辨率。下表映射了每个精度的 H3 分辨率。

例如，如果"<zoom>"为"3"，grid_precision"为"3"，则精度为"6"。在精度为"6"时，六边形单元格的 H3 分辨率为"2"。如果"<zoom>"为"3"，grid_precision"为"4"，则精度为"7"。在精度为"7"时，六边形单元格的 H3 分辨率为"3"。

精度 |独特的瓷砖箱 |H3 分辨率 |独特的六角箱 |比率 ---|---|---|---|--- 1

|

4

|

0

|

122

|

30.5    2

|

16

|

0

|

122

|

7.625    3

|

64

|

1

|

842

|

13.15625    4

|

256

|

1

|

842

|

3.2890625    5

|

1024

|

2

|

5882

|

5.744140625    6

|

4096

|

2

|

5882

|

1.436035156    7

|

16384

|

3

|

41162

|

2.512329102    8

|

65536

|

3

|

41162

|

0.6280822754    9

|

262144

|

4

|

288122

|

1.099098206    10

|

1048576

|

4

|

288122

|

0.2747745514    11

|

4194304

|

5

|

2016842

|

0.4808526039    12

|

16777216

|

6

|

14117882

|

0.8414913416    13

|

67108864

|

6

|

14117882

|

0.2103728354    14

|

268435456

|

7

|

98825162

|

0.3681524172    15

|

1073741824

|

8

|

691776122

|

0.644266719    16

|

4294967296

|

8

|

691776122

|

0.1610666797    17

|

17179869184

|

9

|

4842432842

|

0.2818666889    18

|

68719476736

|

10

|

33897029882

|

0.4932667053    19

|

274877906944

|

11

|

237279209162

|

0.8632167343    20

|

1099511627776

|

11

|

237279209162

|

0.2158041836    21

|

4398046511104

|

12

|

1660954464122

|

0.3776573213    22

|

17592186044416

|

13

|

11626681248842

|

0.6609003122    23

|

70368744177664

|

13

|

11626681248842

|

0.165225078    24

|

281474976710656

|

14

|

81386768741882

|

0.2891438866    25

|

1125899906842620

|

15

|

569707381193162

|

0.5060018015    26

|

4503599627370500

|

15

|

569707381193162

|

0.1265004504    27

|

18014398509482000

|

15

|

569707381193162

|

0.03162511259    28

|

72057594037927900

|

15

|

569707381193162

|

0.007906278149    29

|

288230376151712000

|

15

|

569707381193162

|

0.001976569537 六边形单元格在矢量图块上不完全对齐。某些单元格可能与多个矢量图块相交。为了计算每个精度的 H3 分辨率，Elasticsearch 将每个分辨率的六边形图格的平均密度与每个缩放级别的图块箱的平均密度进行比较。Elasticsearch使用最接近相应"地理分布"密度的H3分辨率。

`grid_type`

    

(可选，字符串)确定"aggs"图层中要素的几何类型。在"aggs"图层中，每个要素表示格网中的一个像元。

"grid_type"的有效值

"网格"(默认)

     Each feature is a `Polygon` of the cell's geometry. For a `grid_agg` of `geotile`, the feature is the cell's bounding box. For a `grid_agg` of `geohex`, the feature is the hexagonal cell's boundaries. 
`point`

     Each feature is a `Point` that's the centroid of the cell. 
`centroid`

     Each feature is a `Point` that's the centroid of the data within the cell. For complex geometries, the actual centroid may be outside the cell. In these cases, the feature is set to the closest point to the centroid inside the cell. 

`query`

     (Optional, object) [Query DSL](query-dsl.html "Query DSL") used to filter documents for the search. 
`runtime_mappings`

    

(可选，对象的对象)在搜索请求中定义一个或多个运行时字段。这些字段优先于具有相同名称的映射字段。

"runtime_mappings"对象的属性

`<field-name>`

    

(必填，对象)运行时字段的配置。键是字段名称。

""的属性<field-name>

`type`

    

(必需，字符串)字段类型，可以是以下任何一种：

* "布尔值" * "复合" * "日期" * "双精度" * "geo_point" * "IP" * "关键字" * "长" * "查找"

`script`

    

(可选，字符串)查询时执行的无痛脚本。该脚本可以访问文档的整个上下文，包括原始"_source"和任何映射字段及其值。

此脚本必须包含"emit"以返回计算值。例如：

    
    
    "script": "emit(doc['@timestamp'].value.dayOfWeekEnum.toString())"

`size`

     (Optional, integer) Maximum number of features to return in the `hits` layer. Accepts `0`-`10000`. Defaults to `10000`. If `0`, results don't include the `hits` layer. 
`sort`

    

(可选，排序对象数组)对"命中"图层中的要素进行排序。

默认情况下，API 会为每个功能计算一个边界框。它根据此框的对角线长度(从最长到最短)对要素进行排序。

`track_total_hits`

    

(可选，整数或布尔值)与查询匹配的命中数准确计数。默认为"10000"。

如果为"true"，则以牺牲某些性能为代价返回确切的命中数。如果为"false"，则响应不包括与查询匹配的命中总数。

`with_labels`

    

(可选，布尔值)如果为 true，则命中图层和 aggs 图层将包含表示原始要素建议标注位置的附加点要素。

* "点"和"多点"要素将选择其中一个点。  * "面"和"多面"要素将生成一个点，即质心(如果位于面内)或从排序的三角形树中选择的面内的另一个点。  * "LineString"功能同样将提供一个从三角树中选择的大致中心点。  * 聚合结果将为每个聚合存储桶提供一个中心点。

原始要素中的所有属性也将复制到新标注要素。此外，可以使用标签"_mvt_label_position"来区分新功能。

###Response

返回的矢量切片包含以下数据：

`hits`

    

(对象)包含"geo_bounding_box"查询结果的图层。

"命中"的属性

`extent`

     (integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. 

`version`

     (integer) Major version number of the [Mapbox vector tile specification](https://github.com/mapbox/vector-tile-spec). 
`features`

    

(对象数组)一系列功能。包含<field>与"geo_bounding_box"查询匹配的每个"值"的功能。

"特征"对象的属性

`geometry`

    

(对象)要素的几何。

"几何"的属性

`type`

    

(字符串)要素的几何类型。有效值为：

* "未知" * "点" * "线串" * "多边形"

`coordinates`

     (array of integers or array of arrays) Tile coordinates for the feature. 

`properties`

    

(对象)功能的属性。

"属性"的属性

`_id`

     (string) Document `_id` for the feature's document. 
`_index`

     (string) Name of the index for the feature's document. 
`<field>`

     Field value. Only returned for fields in the `fields` parameter. 

`type`

    

(整数)要素几何类型的标识符。值为：

* "1" ("点") * "2" ("线串") * "3" ("多边形")

`aggs`

    

(对象)包含"grid_agg"聚合及其子聚合结果的图层。

"阿格斯"的属性

`extent`

     (integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. 
`version`

     (integer) Major version number of the [Mapbox vector tile specification](https://github.com/mapbox/vector-tile-spec). 
`features`

    

(对象数组)一系列功能。包含网格的每个像元的特征。

"特征"对象的属性

`geometry`

    

(对象)要素的几何。

"几何"的属性

`type`

    

(字符串)要素的几何类型。有效值为：

* "未知" * "点" * "线串" * "多边形"

`coordinates`

     (array of integers or array of arrays) Tile coordinates for the feature. 

`properties`

    

(对象)功能的属性。

"属性"的属性

`_count`

     (long) Count of the cell's documents. 
`_key`

     (string) Bucket key of the cell in the format `<zoom>/<x>/<y>`. 
`<sub-aggregation>.value`

     Sub-aggregation results for the cell. Only returned for sub-aggregations in the `aggs` parameter. 

`type`

    

(整数)要素几何类型的标识符。值为：

* "1" ("点") * "2" ("线串") * "3" ("多边形")

`meta`

    

(对象)包含请求元数据的图层。

"元"的属性

`extent`

     (integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. 
`version`

     (integer) Major version number of the [Mapbox vector tile specification](https://github.com/mapbox/vector-tile-spec). 
`features`

    

(对象数组)包含边界框的功能。

"特征"对象的属性

`geometry`

    

(对象)要素的几何。

"几何"的属性

`type`

    

(字符串)要素的几何类型。有效值为：

* "未知" * "点" * "线串" * "多边形"

`coordinates`

     (array of integers or array of arrays) Tile coordinates for the feature. 

`properties`

    

(对象)功能的属性。

"属性"的属性

`_shards.failed`

     (integer) Number of shards that failed to execute the search. See the search API's [`shards`](search-search.html#search-api-shards) response property. 
`_shards.skipped`

     (integer) Number of shards that skipped the search. See the search API's [`shards`](search-search.html#search-api-shards) response property. 
`_shards.successful`

     (integer) Number of shards that executed the search successfully. See the search API's [`shards`](search-search.html#search-api-shards) response property. 
`_shards.total`

     (integer) Total number of shards that required querying, including unallocated shards. See the search API's [`shards`](search-search.html#search-api-shards) response property. 
`aggregations._count.avg`

     (float) Average `_count` value for features in the `aggs` layer. 
`aggregations._count.count`

     (integer) Number of unique `_count` values for features in the `aggs` layer. 
`aggregations._count.max`

     (float) Largest `_count` value for features in the `aggs` layer. 
`aggregations._count.min`

     (float) Smallest `_count` value for features in the `aggs` layer. 
`aggregations._count.sum`

     (float) Sum of `_count` values for features in the `aggs` layer. 
`aggregations.<sub-aggregation>.avg`

     (float) Average value for the sub-aggregation's results. 
`aggregations.<agg_name>.count`

     (integer) Number of unique values from the sub-aggregation's results. 
`aggregations.<agg_name>.max`

     (float) Largest value from the sub-aggregation's results. 
`aggregations.<agg_name>.min`

     (float) Smallest value from the sub-aggregation's results. 
`aggregations.<agg_name>.sum`

     (float) Sum of values for the sub-aggregation's results. 
`hits.max_score`

     (float) Highest document `_score` for the search's hits. 
`hits.total.relation`

    

(字符串)指示"hits.total.value"是准确的还是下限的。可能的值为：

`eq`

     Accurate 
`gte`

     Lower bound 

`hits.total.value`

     (integer) Total number of hits for the search. 
`timed_out`

     (Boolean) If `true`, the search timed out before completion. Results may be partial or empty. 
`took`

     (integer) Milliseconds it took Elasticsearch to run the search. See the search API's [`took`](search-search.html#search-api-took) response property. 

`type`

    

(整数)要素几何类型的标识符。值为：

* "1" ("点") * "2" ("线串") * "3" ("多边形")

###Examples

以下请求创建"博物馆"索引并添加多个地理空间"位置"值。

    
    
    response = client.indices.create(
      index: 'museums',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'geo_point'
            },
            name: {
              type: 'keyword'
            },
            price: {
              type: 'long'
            },
            included: {
              type: 'boolean'
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
            _id: '1'
          }
        },
        {
          location: 'POINT (4.912350 52.374081)',
          name: 'NEMO Science Museum',
          price: 1750,
          included: true
        },
        {
          index: {
            _id: '2'
          }
        },
        {
          location: 'POINT (4.901618 52.369219)',
          name: 'Museum Het Rembrandthuis',
          price: 1500,
          included: false
        },
        {
          index: {
            _id: '3'
          }
        },
        {
          location: 'POINT (4.914722 52.371667)',
          name: 'Nederlands Scheepvaartmuseum',
          price: 1650,
          included: true
        },
        {
          index: {
            _id: '4'
          }
        },
        {
          location: 'POINT (4.914722 52.371667)',
          name: 'Amsterdam Centre for Architecture',
          price: 0,
          included: true
        }
      ]
    )
    puts response
    
    
    PUT museums
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_point"
          },
          "name": {
            "type": "keyword"
          },
          "price": {
            "type": "long"
          },
          "included": {
            "type": "boolean"
          }
        }
      }
    }
    
    POST museums/_bulk?refresh
    { "index": { "_id": "1" } }
    { "location": "POINT (4.912350 52.374081)", "name": "NEMO Science Museum",  "price": 1750, "included": true }
    { "index": { "_id": "2" } }
    { "location": "POINT (4.901618 52.369219)", "name": "Museum Het Rembrandthuis", "price": 1500, "included": false }
    { "index": { "_id": "3" } }
    { "location": "POINT (4.914722 52.371667)", "name": "Nederlands Scheepvaartmuseum", "price":1650, "included": true }
    { "index": { "_id": "4" } }
    { "location": "POINT (4.914722 52.371667)", "name": "Amsterdam Centre for Architecture", "price":0, "included": true }

以下请求在索引中搜索与"13/4207/2692"矢量切片相交的"位置"值。

    
    
    GET museums/_mvt/location/13/4207/2692
    {
      "grid_agg": "geotile",
      "grid_precision": 2,
      "fields": [
        "name",
        "price"
      ],
      "query": {
        "term": {
          "included": true
        }
      },
      "aggs": {
        "min_price": {
          "min": {
            "field": "price"
          }
        },
        "max_price": {
          "max": {
            "field": "price"
          }
        },
        "avg_price": {
          "avg": {
            "field": "price"
          }
        }
      }
    }

API 以二进制矢量磁贴的形式返回结果。解码为 JSON 时，磁贴包含以下数据：

    
    
    {
      "hits": {
        "extent": 4096,
        "version": 2,
        "features": [
          {
            "geometry": {
              "type": "Point",
              "coordinates": [
                3208,
                3864
              ]
            },
            "properties": {
              "_id": "1",
              "_index": "museums",
              "name": "NEMO Science Museum",
              "price": 1750
            },
            "type": 1
          },
          {
            "geometry": {
              "type": "Point",
              "coordinates": [
                3429,
                3496
              ]
            },
            "properties": {
              "_id": "3",
              "_index": "museums",
              "name": "Nederlands Scheepvaartmuseum",
              "price": 1650
            },
            "type": 1
          },
          {
            "geometry": {
              "type": "Point",
              "coordinates": [
                3429,
                3496
              ]
            },
            "properties": {
              "_id": "4",
              "_index": "museums",
              "name": "Amsterdam Centre for Architecture",
              "price": 0
            },
            "type": 1
          }
        ]
      },
      "aggs": {
        "extent": 4096,
        "version": 2,
        "features": [
          {
            "geometry": {
              "type": "Polygon",
              "coordinates": [
                [
                  [
                    3072,
                    3072
                  ],
                  [
                    4096,
                    3072
                  ],
                  [
                    4096,
                    4096
                  ],
                  [
                    3072,
                    4096
                  ],
                  [
                    3072,
                    3072
                  ]
                ]
              ]
            },
            "properties": {
              "_count": 3,
              "max_price.value": 1750.0,
              "min_price.value": 0.0,
              "avg_price.value": 1133.3333333333333
            },
            "type": 3
          }
        ]
      },
      "meta": {
        "extent": 4096,
        "version": 2,
        "features": [
          {
            "geometry": {
              "type": "Polygon",
              "coordinates": [
                [
                  [
                    0,
                    0
                  ],
                  [
                    4096,
                    0
                  ],
                  [
                    4096,
                    4096
                  ],
                  [
                    0,
                    4096
                  ],
                  [
                    0,
                    0
                  ]
                ]
              ]
            },
            "properties": {
              "_shards.failed": 0,
              "_shards.skipped": 0,
              "_shards.successful": 1,
              "_shards.total": 1,
              "aggregations._count.avg": 3.0,
              "aggregations._count.count": 1,
              "aggregations._count.max": 3.0,
              "aggregations._count.min": 3.0,
              "aggregations._count.sum": 3.0,
              "aggregations.avg_price.avg": 1133.3333333333333,
              "aggregations.avg_price.count": 1,
              "aggregations.avg_price.max": 1133.3333333333333,
              "aggregations.avg_price.min": 1133.3333333333333,
              "aggregations.avg_price.sum": 1133.3333333333333,
              "aggregations.max_price.avg": 1750.0,
              "aggregations.max_price.count": 1,
              "aggregations.max_price.max": 1750.0,
              "aggregations.max_price.min": 1750.0,
              "aggregations.max_price.sum": 1750.0,
              "aggregations.min_price.avg": 0.0,
              "aggregations.min_price.count": 1,
              "aggregations.min_price.max": 0.0,
              "aggregations.min_price.min": 0.0,
              "aggregations.min_price.sum": 0.0,
              "hits.max_score": 0.0,
              "hits.total.relation": "eq",
              "hits.total.value": 3,
              "timed_out": false,
              "took": 2
            },
            "type": 3
          }
        ]
      }
    }

[« Ranking evaluation API](search-rank-eval.md) [Search Application APIs
»](search-application-apis.md)
