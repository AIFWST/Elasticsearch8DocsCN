

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Shape queries](shape-queries.md)

[« Shape queries](shape-queries.md) [Joining queries »](joining-
queries.md)

## 形状查询

查询包含使用"shape"类型编制索引的字段的文档。

需要"形状"映射。

查询支持两种定义目标形状的方法，一种是提供整个形状定义，另一种是引用在另一个索引中预先编制索引的形状的名称或 id。下面通过示例定义了这两种格式。

### 内联形状定义

与"geo_shape"查询类似，"shape"查询使用GeoJSON或已知文本(WKT)来表示形状。

给定以下索引：

    
    
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
    
    response = client.index(
      index: 'example',
      id: 1,
      refresh: 'wait_for',
      body: {
        name: 'Lucky Landing',
        geometry: {
          type: 'point',
          coordinates: [
            1355.400544,
            5255.530286
          ]
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
    
    PUT /example/_doc/1?refresh=wait_for
    {
      "name": "Lucky Landing",
      "geometry": {
        "type": "point",
        "coordinates": [ 1355.400544, 5255.530286 ]
      }
    }

以下查询将使用Elasticsearch的'envelope'GeoJSON扩展找到该点：

    
    
    GET /example/_search
    {
      "query": {
        "shape": {
          "geometry": {
            "shape": {
              "type": "envelope",
              "coordinates": [ [ 1355.0, 5355.0 ], [ 1400.0, 5200.0 ] ]
            },
            "relation": "within"
          }
        }
      }
    }

### 预索引形状

查询还支持使用已在另一个索引中编制索引的形状。当您有一个预定义的形状列表，这些形状对您的应用程序很有用，并且您希望使用逻辑名称(例如_New Zealand_)引用它，而不必每次都提供它们的坐标时，这特别有用。在这种情况下，只需要提供：

* 'id' \- 包含预索引形状的文档的 ID。  * 'index' \- 预索引形状所在的索引的名称。默认为 _shapes_。  * 'path' \- 指定为包含预索引形状的路径的字段。默认为 _shape_。  * "路由" \- 形状文档的路由(如果需要)。

以下是将筛选器与预先编制索引的形状一起使用的示例：

    
    
    response = client.indices.create(
      index: 'shapes',
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
    
    response = client.index(
      index: 'shapes',
      id: 'footprint',
      body: {
        geometry: {
          type: 'envelope',
          coordinates: [
            [
              1355,
              5355
            ],
            [
              1400,
              5200
            ]
          ]
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'example',
      body: {
        query: {
          shape: {
            geometry: {
              indexed_shape: {
                index: 'shapes',
                id: 'footprint',
                path: 'geometry'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /shapes
    {
      "mappings": {
        "properties": {
          "geometry": {
            "type": "shape"
          }
        }
      }
    }
    
    PUT /shapes/_doc/footprint
    {
      "geometry": {
        "type": "envelope",
        "coordinates": [ [ 1355.0, 5355.0 ], [ 1400.0, 5200.0 ] ]
      }
    }
    
    GET /example/_search
    {
      "query": {
        "shape": {
          "geometry": {
            "indexed_shape": {
              "index": "shapes",
              "id": "footprint",
              "path": "geometry"
            }
          }
        }
      }
    }

### 空间关系

以下是可用的空间关系运算符的完整列表：

* 'INTERSECTS' \-(默认值)返回 'shape' 字段与查询几何相交的所有文档。  * 'DISJOINT' \- 返回其 'shape' 字段与查询几何没有任何共同点的所有文档。  * "WITHIN" \- 返回其"shape"字段在查询几何中的所有文档。  * 'CONTAINS' \- 返回其 'shape' 字段包含查询几何的所有文档。

#### 忽略未映射

当设置为"true"时，"ignore_unmapped"选项将忽略未映射的字段，并且不会匹配此查询的任何文档。这在查询可能具有不同映射的多个索引时非常有用。当设置为"false"(默认值)时，如果未映射字段，查询将引发异常。

[« Shape queries](shape-queries.md) [Joining queries »](joining-
queries.md)
