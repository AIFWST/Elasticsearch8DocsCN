

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_routing` field](mapping-routing-field.md) [`_tier` field »](mapping-
tier-field.md)

## '_source'字段

"_source"字段包含在索引时传递的原始 JSON 文档正文。"_source"字段本身没有索引(因此是值得注意的)，但它被存储起来，以便在executing_fetch_请求(如 get 或搜索)时可以返回它。

如果磁盘使用情况对您很重要，请查看 synthetic'_source'它以仅支持映射子集和较慢的获取或(不推荐)禁用"_source"字段为代价来减少磁盘使用量，但禁用了许多功能。

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

虽然非常方便，但源字段占用了磁盘上的大量空间。Elasticsearch 不是在发送源文档时将源文档完全存储在磁盘上，而是可以在检索时即时重建源内容。通过在"_source"中设置"模式：合成"来启用此功能：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          }
        }
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": {
          "mode": "synthetic"
        }
      }
    }

虽然这种动态重建通常比逐字保存源文档并在查询时加载它们要慢，但它节省了大量存储空间。

#### 合成"_source"限制

有几个限制需要注意：

* 当您检索合成的"_source"内容时，与原始 JSON 相比，它会进行细微的修改。  * "params._source"在脚本中不可用。请改用"文档"API 或"字段"API。  * 使用合成"_source"的索引目前不支持没有脚本的运行时字段和访问"_source"的运行时字段。改用脚本化运行时字段，该字段使用文档值或"字段"API 访问字段。  * 合成"_source"可以与仅包含以下字段类型的索引一起使用：

    * [`aggregate_metric_double`](aggregate-metric-double.html#aggregate-metric-double-synthetic-source "Synthetic _source")
    * [`boolean`](boolean.html#boolean-synthetic-source "Synthetic _source")
    * [`byte`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`date`](date.html#date-synthetic-source "Synthetic _source")
    * [`date_nanos`](date_nanos.html#date-nanos-synthetic-source "Synthetic _source")
    * [`dense_vector`](dense-vector.html#dense-vector-synthetic-source "Synthetic _source")
    * [`double`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`flattened`](flattened.html#flattened-synthetic-source "Synthetic _source")
    * [`float`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`geo_point`](geo-point.html#geo-point-synthetic-source "Synthetic source")
    * [`half_float`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`histogram`](histogram.html#histogram-synthetic-source "Synthetic _source")
    * [`integer`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`ip`](ip.html#ip-synthetic-source "Synthetic _source")
    * [`keyword`](keyword.html#keyword-synthetic-source "Synthetic _source")
    * [`long`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`scaled_float`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`short`](number.html#numeric-synthetic-source "Synthetic _source")
    * [`text`](text.html#text-synthetic-source "Synthetic _source")
    * [`version`](version.html#version-synthetic-source "Synthetic _source")
    * [`wildcard`](keyword.html#wildcard-synthetic-source "Synthetic _source")

#### 合成"_source"修改

启用合成"_source"后，与原始 JSON 相比，检索到的文档会进行一些修改。

##### 数组移动到叶字段

合成的"_source"数组被移动到叶子上。例如：

    
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        foo: [
          {
            bar: 1
          },
          {
            bar: 2
          }
        ]
      }
    )
    puts response
    
    
    PUT idx/_doc/1
    {
      "foo": [
        {
          "bar": 1
        },
        {
          "bar": 2
        }
      ]
    }

将成为：

    
    
    {
      "foo": {
        "bar": [1, 2]
      }
    }

这可能会导致某些数组消失：

    
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        foo: [
          {
            bar: 1
          },
          {
            baz: 2
          }
        ]
      }
    )
    puts response
    
    
    PUT idx/_doc/1
    {
      "foo": [
        {
          "bar": 1
        },
        {
          "baz": 2
        }
      ]
    }

将成为：

    
    
    {
      "foo": {
        "bar": 1,
        "baz": 2
      }
    }

##### 按映射命名的字段

合成源名称字段，因为它们在映射中命名。与动态映射一起使用时，默认情况下，名称中带有点 ('.') 的字段被解释为多个对象，而字段名称中的点保留在禁用了"子对象"的对象中。例如：

    
    
    PUT idx/_doc/1
    {
      "foo.bar.baz": 1
    }

将成为：

    
    
    {
      "foo": {
        "bar": {
          "baz": 1
        }
      }
    }

##### 按字母顺序排序

合成的"_source"字段按字母顺序排序。JSONRFC 将对象定义为"零个或多个名称/值对的无序集合"，因此应用程序不应该关心，但没有合成的"_source"，原始排序将被保留，并且某些应用程序可能会与规范相反，对该排序执行某些操作。

### 禁用"_source"字段

虽然非常方便，但源字段确实会在索引中产生存储开销。因此，可以按如下方式禁用它：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          _source: {
            enabled: false
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "_source": {
          "enabled": false
        }
      }
    }

### 禁用"_source"字段之前请三思

用户经常在不考虑后果的情况下禁用"_source"字段，然后活着后悔。如果"_source"字段不可用，则不支持许多功能：

* "更新"、"update_by_query"和"重新索引"API。  *在飞行中突出显示。  * 能够从一个 Elasticsearch 索引重新索引到另一个索引，以更改映射或分析，或将索引升级到新的主要版本。  * 通过查看索引时使用的原始文档来调试查询或聚合的功能。  * 将来可能会自动修复索引损坏。

如果磁盘空间是一个问题，请提高压缩级别，而不是禁用"_source"。

### 包括/排除"_source"中的字段

专家专用功能是能够在文档编制索引之后但在存储"_source"字段之前修剪"_source"字段的内容。

从"_source"中删除字段与禁用"_source"具有类似的缺点，尤其是您无法将文档从oneElasticsearch索引重新索引到另一个索引的事实。请考虑改用源筛选。

"include"/"excludes"参数(也接受通配符)可以按如下方式使用：

    
    
    response = client.indices.create(
      index: 'logs',
      body: {
        mappings: {
          _source: {
            includes: [
              '*.count',
              'meta.*'
            ],
            excludes: [
              'meta.description',
              'meta.other.*'
            ]
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'logs',
      id: 1,
      body: {
        requests: {
          count: 10,
          foo: 'bar'
        },
        meta: {
          name: 'Some metric',
          description: 'Some metric description',
          other: {
            foo: 'one',
            baz: 'two'
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'logs',
      body: {
        query: {
          match: {
            "meta.other.foo": 'one'
          }
        }
      }
    )
    puts response
    
    
    PUT logs
    {
      "mappings": {
        "_source": {
          "includes": [
            "*.count",
            "meta.*"
          ],
          "excludes": [
            "meta.description",
            "meta.other.*"
          ]
        }
      }
    }
    
    PUT logs/_doc/1
    {
      "requests": {
        "count": 10,
        "foo": "bar" __},
      "meta": {
        "name": "Some metric",
        "description": "Some metric description", __"other": {
          "foo": "one", __"baz": "two" __}
      }
    }
    
    GET logs/_search
    {
      "query": {
        "match": {
          "meta.other.foo": "one" __}
      }
    }

__

|

这些字段将从存储的"_source"字段中删除。   ---|---    __

|

我们仍然可以搜索此字段，即使它不在存储的"_source"中。   « "_routing"字段 "_tier"字段 »