

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Foreach processor](foreach-processor.md) [GeoIP processor »](geoip-
processor.md)

## 地理网格处理器

将网格图块或单元格的地理网格定义转换为描述其形状的常规边界框或多边形。如果需要将切片形状作为空间可索引字段进行交互，这将非常有用。例如，可以将"geotile"字段值""4/8/3""索引为字符串字段，但这不会对其启用任何空间操作。相反，将其转换为值"POLYGON ((0.0 40.979898069620134， 22.5 40.979898069620134， 22.555.77657301866769， 0.0 55.77657301866769， 0.0 40.979898069620134))"，可以索引为"geo_shape"字段。

**表 21.geo_grid处理器选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要解释为地理磁贴的字段。字段格式由"tile_type"确定。   "tile_type"

|

yes

|

-

|

了解三种磁贴格式："geohash"、"geotile"和"geohex"。   "target_field"

|

no

|

`field`

|

要将多边形形状分配到的字段(默认情况下为"字段")将就地更新。   "parent_field"

|

no

|

-

|

如果指定且父磁贴存在，请将该磁贴地址保存到此字段。   "children_field"

|

no

|

-

|

如果指定且存在子磁贴，请将这些磁贴地址作为字符串数组保存到此字段。   "non_children_field"

|

no

|

-

|

如果存在指定且相交的非子磁贴，请将其地址保存到此字段作为字符串数组。   "precision_field"

|

no

|

-

|

如果指定，请将切片精度(缩放)作为整数保存到此字段。   "ignore_missing"

|

no

|

-

|

如果"true"和"field"不存在，处理器将静默退出而不修改文档。   "target_format"

|

no

|

"GeoJSON"

|

将生成的多边形保存为哪种格式。"WKT"或"GeoJSON"。   "说明"

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

处理器的标识符。对于调试和指标很有用。   为了演示此采集处理器的用法，请考虑一个名为"geocell"的索引，该索引具有类型为"geo_shape"的字段"geocell"的映射。要使用"geotile"和"geohex"字段填充该索引，请定义两个摄取处理器：

    
    
    response = client.indices.create(
      index: 'geocells',
      body: {
        mappings: {
          properties: {
            geocell: {
              type: 'geo_shape'
            }
          }
        }
      }
    )
    puts response
    
    response = client.ingest.put_pipeline(
      id: 'geotile2shape',
      body: {
        description: 'translate rectangular z/x/y geotile to bounding box',
        processors: [
          {
            geo_grid: {
              field: 'geocell',
              tile_type: 'geotile'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.ingest.put_pipeline(
      id: 'geohex2shape',
      body: {
        description: 'translate H3 cell to polygon',
        processors: [
          {
            geo_grid: {
              field: 'geocell',
              tile_type: 'geohex',
              target_format: 'wkt'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT geocells
    {
      "mappings": {
        "properties": {
          "geocell": {
            "type": "geo_shape"
          }
        }
      }
    }
    
    PUT _ingest/pipeline/geotile2shape
    {
      "description": "translate rectangular z/x/y geotile to bounding box",
      "processors": [
        {
          "geo_grid": {
            "field": "geocell",
            "tile_type": "geotile"
          }
        }
      ]
    }
    
    PUT _ingest/pipeline/geohex2shape
    {
      "description": "translate H3 cell to polygon",
      "processors": [
        {
          "geo_grid": {
            "field": "geocell",
            "tile_type": "geohex",
            "target_format": "wkt"
          }
        }
      ]
    }

这两个管道可用于将文档索引到"geocell"索引中。"geocell"字段将是格式为"z/x/y"的矩形磁贴或 H3 单元格地址的字符串版本，具体取决于我们在索引文档时使用的采集处理器。生成的几何图形将以 GeoJSON 或已知文本格式表示为"geo_shape"字段并编制索引。

### 示例：GeoJSON 中带有封套的矩形地理磁贴

在此示例中，具有以"z/x/y"格式定义的值的"geocell"字段被索引为 GeoJSON 信封，因为上面的摄取处理器是使用默认"target_format"定义的。

    
    
    response = client.index(
      index: 'geocells',
      id: 1,
      pipeline: 'geotile2shape',
      body: {
        geocell: '4/8/5'
      }
    )
    puts response
    
    response = client.get(
      index: 'geocells',
      id: 1
    )
    puts response
    
    
    PUT geocells/_doc/1?pipeline=geotile2shape
    {
      "geocell": "4/8/5"
    }
    
    GET geocells/_doc/1

响应显示了摄取处理器如何将"geocell"字段替换为可索引的"geo_shape"：

    
    
    {
     "_index": "geocells",
      "_id": "1",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
        "geocell": {
          "type": "Envelope",
          "coordinates": [
            [ 0.0, 55.77657301866769 ],
            [ 22.5, 40.979898069620134 ]
          ]
        }
      }
    }

!Kibana 地图，显示 4/8/5 处的地理图块及其四个子单元

### 示例：WKT格式的六边形地理六角形和多边形

在此示例中，具有 H3 字符串地址的"geocell"字段被索引为 aWKT 多边形，因为此摄取处理器显式定义了"target_format"。

    
    
    response = client.index(
      index: 'geocells',
      id: 1,
      pipeline: 'geohex2shape',
      body: {
        geocell: '811fbffffffffff'
      }
    )
    puts response
    
    response = client.get(
      index: 'geocells',
      id: 1
    )
    puts response
    
    
    PUT geocells/_doc/1?pipeline=geohex2shape
    {
      "geocell": "811fbffffffffff"
    }
    
    GET geocells/_doc/1

响应显示了摄取处理器如何将"geocell"字段替换为可索引的"geo_shape"：

    
    
    {
     "_index": "geocells",
      "_id": "1",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
        "geocell": "POLYGON ((1.1885095294564962 49.470279179513454, 2.0265689212828875 45.18424864858389, 7.509948452934623 43.786609335802495, 12.6773177459836 46.40695743262768, 12.345747342333198 50.55427505169064, 6.259687012061477 51.964770150370896, 3.6300085578113794 50.610463307239115, 1.1885095294564962 49.470279179513454))"
      }
    }

!显示 H3 单元格的 Kibana 地图

### 示例：扩充磁贴详细信息

如geo_grid处理器选项中所述，可以设置许多其他字段，这将丰富可用信息。例如，对于 H3 磁贴，有 7 个子磁贴，但只有第一个被父磁贴完全包含。其余六个磁贴仅部分重叠父磁贴，并且还有六个非子磁贴与父磁贴重叠。这可以通过将父字段和子字段添加到摄取处理器来调查：

    
    
    response = client.ingest.put_pipeline(
      id: 'geohex2shape',
      body: {
        description: 'translate H3 cell to polygon with enriched fields',
        processors: [
          {
            geo_grid: {
              description: "Ingest H3 cells like '811fbffffffffff' and create polygons",
              field: 'geocell',
              tile_type: 'geohex',
              target_format: 'wkt',
              target_field: 'shape',
              parent_field: 'parent',
              children_field: 'children',
              non_children_field: 'nonChildren',
              precision_field: 'precision'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/geohex2shape
    {
      "description": "translate H3 cell to polygon with enriched fields",
      "processors": [
        {
          "geo_grid": {
            "description": "Ingest H3 cells like '811fbffffffffff' and create polygons",
            "field": "geocell",
            "tile_type": "geohex",
            "target_format": "wkt",
            "target_field": "shape",
            "parent_field": "parent",
            "children_field": "children",
            "non_children_field": "nonChildren",
            "precision_field": "precision"
          }
        }
      ]
    }

为文档编制索引以查看不同的结果：

    
    
    response = client.index(
      index: 'geocells',
      id: 1,
      pipeline: 'geohex2shape',
      body: {
        geocell: '811fbffffffffff'
      }
    )
    puts response
    
    response = client.get(
      index: 'geocells',
      id: 1
    )
    puts response
    
    
    PUT geocells/_doc/1?pipeline=geohex2shape
    {
      "geocell": "811fbffffffffff"
    }
    
    GET geocells/_doc/1

此索引请求的响应：

    
    
    {
      "_index": "geocells",
      "_id": "1",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
        "parent": "801ffffffffffff",
        "geocell": "811fbffffffffff",
        "precision": 1,
        "shape": "POLYGON ((1.1885095294564962 49.470279179513454, 2.0265689212828875 45.18424864858389, 7.509948452934623 43.786609335802495, 12.6773177459836 46.40695743262768, 12.345747342333198 50.55427505169064, 6.259687012061477 51.964770150370896, 3.6300085578113794 50.610463307239115, 1.1885095294564962 49.470279179513454))",
        "children": [
          "821f87fffffffff",
          "821f8ffffffffff",
          "821f97fffffffff",
          "821f9ffffffffff",
          "821fa7fffffffff",
          "821faffffffffff",
          "821fb7fffffffff"
        ],
        "nonChildren": [
          "821ea7fffffffff",
          "82186ffffffffff",
          "82396ffffffffff",
          "821f17fffffffff",
          "821e37fffffffff",
          "82194ffffffffff"
        ]
      }
    }

然后，这些附加信息将能够创建例如H3细胞，其子细胞及其相交的非子细胞的可视化。

!具有三个 H3 图层的 Kibana 贴图：单元格

[« Foreach processor](foreach-processor.md) [GeoIP processor »](geoip-
processor.md)
