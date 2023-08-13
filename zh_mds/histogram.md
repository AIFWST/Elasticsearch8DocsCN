

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Geoshape field type](geo-shape.md) [IP field type »](ip.md)

## 直方图字段类型

用于存储表示直方图的预聚合数值数据的字段。此数据是使用两个成对数组定义的：

* "双精度"数字的"值"数组，表示直方图的存储桶。这些值必须按升序提供。  * 一个相应的"整数"数组，表示每个存储桶中有多少个值。这些数字必须为正数或零。

由于"values"数组中的元素对应于"count"数组相同位置的元素，因此这两个数组必须具有相同的长度。

* "直方图"字段只能为每个文档存储一对"值"和"计数"数组。不支持嵌套数组。  * "直方图"字段不支持排序。

###Uses

"直方图"字段主要用于聚合。为了便于聚合访问，"直方图"字段数据存储为二进制文档值，而不是索引。以字节为单位的 Itssize 最多为 '13 * numValues'，其中 'numValues' 是所提供数组的长度。

由于数据未编制索引，因此只能将"直方图"字段用于以下聚合和查询：

* 最小聚合 * 最大聚合 * 总和聚合 * value_count聚合 * 平均聚合 * 百分位数聚合 * 百分位数排名聚合 * 箱线图聚合 * 直方图聚合 * 范围聚合 * 存在查询

### 构建直方图

使用直方图作为聚合的一部分时，结果的准确性将取决于直方图的构造方式。请务必考虑将用于构建它的百分位数聚合模式。一些可能性包括：

* 对于 T 摘要模式，"值"数组表示平均质心位置，"计数"数组表示归属于每个质心的值数。如果算法已经开始近似百分位数，则这种不准确性将在直方图中延续。  * 对于高动态范围 (HDR) 直方图模式，"值"数组表示每个存储桶间隔的固定上限，"计数"数组表示归因于每个间隔的值数。此实现保持固定的最坏情况百分比误差(指定为有效位数)，因此生成直方图时使用的值将是聚合时可以达到的最大精度。

直方图字段与"算法无关"，不存储特定于 T-Digest 或 HDRHistogram 的数据。虽然这意味着该字段在技术上可以使用任一算法进行聚合，但在实践中，用户应该选择一种算法并以这种方式索引数据(例如，质心用于 T-Digest 或区间用于 HDRHistogram)以确保最佳准确性。

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"直方图"字段在其默认配置中支持合成的"_source"。合成"_source"不能与"ignore_malformed"或"copy_to"一起使用。

为了节省空间，零计数存储桶不会存储在直方图文档值中。因此，在启用合成源的索引中为直方图字段编制索引时，为包含零计数存储桶的直方图编制索引将导致在回取直方图时丢失存储桶。

###Examples

以下创建索引 APIrequest 使用两个字段映射创建新索引：

* "my_histogram"，用于存储百分位数据的"直方图"字段 * "my_text"，用于存储直方图标题的"关键字"字段

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_histogram: {
              type: 'histogram'
            },
            my_text: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings" : {
        "properties" : {
          "my_histogram" : {
            "type" : "histogram"
          },
          "my_text" : {
            "type" : "keyword"
          }
        }
      }
    }

以下索引 API 请求存储两个直方图的预聚合："histogram_1"和"histogram_2"。

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        my_text: 'histogram_1',
        my_histogram: {
          values: [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5
          ],
          counts: [
            3,
            7,
            23,
            12,
            6
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        my_text: 'histogram_2',
        my_histogram: {
          values: [
            0.1,
            0.25,
            0.35,
            0.4,
            0.45,
            0.5
          ],
          counts: [
            8,
            17,
            8,
            7,
            6,
            2
          ]
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "my_text" : "histogram_1",
      "my_histogram" : {
          "values" : [0.1, 0.2, 0.3, 0.4, 0.5], __"counts" : [3, 7, 23, 12, 6] __}
    }
    
    PUT my-index-000001/_doc/2
    {
      "my_text" : "histogram_2",
      "my_histogram" : {
          "values" : [0.1, 0.25, 0.35, 0.4, 0.45, 0.5], __"counts" : [8, 17, 8, 7, 6, 2] __}
    }

__

|

每个存储桶的值。数组中的值被视为双精度值，必须按递增顺序给出。对于 T-Digest 近似值")直方图，此值表示平均值。对于 HDR 直方图，这表示迭代到的值。   ---|---    __

|

每个存储桶的计数。数组中的值被视为整数，并且必须为正数或零。负值将被拒绝。abucket 和计数之间的关系由数组中的位置给出。   « 地形字段类型 IP 字段类型 »