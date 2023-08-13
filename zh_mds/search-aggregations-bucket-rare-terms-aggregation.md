

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Range aggregation](search-aggregations-bucket-range-aggregation.md)
[Reverse nested aggregation »](search-aggregations-bucket-reverse-nested-
aggregation.md)

## 简体词聚合

一种基于多桶值源的聚合，它查找"稀有"术语 - 位于分布的长尾且不常见的术语。从概念上讲，这就像按"_count"升序排序的"术语"聚合。如术语聚合文档中所述，实际上按计数升序对"术语"AGG进行排序具有无限错误。相反，您应该使用"rare_terms"聚合

###Syntax

"rare_terms"聚合单独如下所示：

    
    
    {
      "rare_terms": {
        "field": "the_field",
        "max_doc_count": 1
      }
    }

**表 50.'rare_terms' 参数**

参数名称

|

Description

|

Required

|

默认值 ---|---|---|--- 'field'

|

我们希望在其中找到稀有术语的字段

|

Required

|   "max_doc_count"

|

术语应出现在的最大文档中数。

|

Optional

|

"1""精度"

|

内部布谷鸟过滤器的精度。精度越小，近似值越好，但内存使用率越高。不能小于"0.00001"

|

Optional

|

"0.001""包括"

|

应包含在聚合中的术语

|

Optional

|   "排除"

|

应从聚合中排除的术语

|

Optional

|   "失踪"

|

文档没有要聚合的字段时应使用的值

|

Optional

|   例：

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            rare_terms: {
              field: 'genre'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "rare_terms": {
            "field": "genre"
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "genres": {
          "buckets": [
            {
              "key": "swing",
              "doc_count": 1
            }
          ]
        }
      }
    }

在此示例中，我们看到的唯一存储桶是"swing"存储桶，因为它是出现在一个文档中的唯一术语。如果我们将"max_doc_count"增加到"2"，我们将看到更多的存储桶：

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            rare_terms: {
              field: 'genre',
              max_doc_count: 2
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "rare_terms": {
            "field": "genre",
            "max_doc_count": 2
          }
        }
      }
    }

现在，这显示了"爵士乐"术语，其"doc_count"为2"：

    
    
    {
      ...
      "aggregations": {
        "genres": {
          "buckets": [
            {
              "key": "swing",
              "doc_count": 1
            },
            {
              "key": "jazz",
              "doc_count": 2
            }
          ]
        }
      }
    }

### 最大文档计数

"max_doc_count"参数用于控制术语可以具有的文档计数上限。"rare_terms"agg 没有像"术语"agg 那样的大小限制。这意味着将返回与"max_doc_count"条件匹配的术语。聚合以这种方式运行，以避免困扰"术语"聚合的按升序问题。

但是，这确实意味着如果选择不正确，可能会返回大量结果。为了限制此设置的危险，最大值"max_doc_count"为 100。

### 最大存储桶限制

稀有术语聚合比其他聚合更容易触发"search.max_buckets"软限制，因为它的工作方式。在聚合收集结果时，将基于每个分片评估"max_bucket"软限制。一个术语在分片上可能是"稀有的"，但是一旦所有分片结果合并在一起，就会变成"不稀有"。这意味着单个分片往往会收集比真正罕见的存储桶更多的存储桶，因为它们只有自己的本地视图。此列表最终被修剪为协调节点上正确的、较小的稀有术语列表......但是分片可能已经触发了"max_buckets"软限制并中止了请求。

聚合可能具有许多"稀有"术语的字段时，可能需要增加"max_buckets"软限制。或者，您可能需要找到一种方法来过滤结果以返回更少的稀有值(较小的时间跨度，按类别过滤等)，或者重新评估您对"稀有"的定义(例如，如果某物出现 100，000 次，它真的是"稀有"吗？

### 文档计数是近似值

确定数据集中"稀有"术语的天真方法是将所有值放在地图中，在访问每个文档时递增计数，然后返回底部的"n"行。这甚至不会扩展到中等大小的数据集之外。从每个分片中仅保留"前n个"值(ala "terms"聚合)的分片方法失败了，因为问题的长尾性质意味着如果不简单地从所有分片中收集所有值，就不可能找到"前n个"底部值。

相反，稀有术语聚合使用不同的近似算法：

1. 值在第一次看到时放置在地图中。  2. 该术语的每次加法都会增加地图中的一个计数器 3.如果计数器>"max_doc_count"阈值，则该术语将从地图中删除并放置在 CuckooFilter 4 中。布谷鸟过滤器在每个术语上都参考。如果该值在筛选器内，则已知该值已高于阈值并已跳过。

执行后，值映射是"max_doc_count"阈值下的"稀有"项映射。然后，此地图和CuckooFilter与所有其他分片合并。如果存在大于阈值的术语(或出现在其他分片的 CuckooFilter 中)，则该术语将从出现列表中删除。值的最终映射作为"稀有"项返回给用户。

CuckooFilters有可能返回误报(他们可以说一个值存在于他们的集合中，而实际上它不存在)。由于 CuckooFilter 用于查看术语是否超过阈值，这意味着来自 CuckooFilter 的误报将错误地表示某个值很常见(从而将其从最终的存储桶列表中排除)。实际上，这意味着聚合表现出假阴性行为，因为过滤器的使用方式与人们通常如何看待近似集合成员草图"相反"。

CuckooFilters在论文中有更详细的描述：

Fan， Bin， et al. "Cuckoo filter： Actual Better， Than bloom."第十届ACM国际新兴网络实验与技术会议论文集.ACM， 2014.

###Precision

虽然内部布谷鸟过滤器本质上是近似的，但假阴性率可以通过"精度"参数来控制。这允许用户交换更多的运行时内存以获得更准确的结果。

默认精度为"0.001"，最小精度(例如，最准确和最大的内存开销)为"0.00001"。下面是一些图表，它们演示了聚合的准确性如何受到精度和不同项数的影响。

X 轴显示聚合看到的不同值的数量，Y 轴显示百分比误差。每个系列代表一个"稀有"条件(范围从一件稀有物品到 100，000 件稀有物品)。例如，橙色"10"行表示 1-20m 个不同值中的 10 个值是"稀有"('doc_count == 1')(其余值有"doc_count > 1")

第一个图表显示精度"0.01"：

精度 01

和精度"0.001"(默认值)：

！精度 001

最后是"精度 0.0001"：

！精度 0001

对于测试条件，默认精度"0.001"保持< 2.5% 的精度，并且随着不同值数量的增加，精度以受控的线性方式缓慢下降。

默认精度"0.001"的内存配置文件为"1.748⁻⁶ * n"字节，其中"n"是聚合看到的不同值的数量(也可以粗略地目测，例如，2000 万个唯一值大约是 30mb 的内存)。内存使用情况与非重复值的数量成线性关系无论选择哪种精度，精度仅影响内存配置文件的斜率，如下图所示：

![memory](images/rare_terms/memory.png)

相比之下，2000 万个存储桶的等效项聚合大约为"20m * 69b == ~1.38gb"(69 字节是对空存储桶成本的非常乐观的估计，远低于断路器所占的)。因此，尽管"rare_terms"AGG相对较重，但它仍然比等效项聚合小几个数量级。

### 筛选值

可以筛选将为其创建存储桶的值。这可以使用基于正则表达式字符串或精确值数组的"include"和"exclude"参数来完成。此外，"include"子句可以使用"分区"表达式进行筛选。

#### 使用正则表达式过滤值

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            rare_terms: {
              field: 'genre',
              include: 'swi*',
              exclude: 'electro*'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "rare_terms": {
            "field": "genre",
            "include": "swi*",
            "exclude": "electro*"
          }
        }
      }
    }

在上面的示例中，将为所有以"swi"开头的标签创建存储桶，但以"electro"开头的标签除外(因此标签"swing"将被聚合，而不是"electro_swing")。"include"正则表达式将确定"允许"聚合哪些值，而"排除"则确定不应聚合的值。当两者都被定义时，"排除"具有优先权，这意味着，首先评估"包含"，然后才评估"排除"。

语法与正则表达式查询相同。

#### 使用精确值筛选值

对于基于精确值的匹配，"include"和"exclude"参数可以简单地采用一个字符串数组，这些字符串表示在索引中找到的术语：

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            rare_terms: {
              field: 'genre',
              include: [
                'swing',
                'rock'
              ],
              exclude: [
                'jazz'
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "rare_terms": {
            "field": "genre",
            "include": [ "swing", "rock" ],
            "exclude": [ "jazz" ]
          }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            rare_terms: {
              field: 'genre',
              missing: 'N/A'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "rare_terms": {
            "field": "genre",
            "missing": "N/A" __}
        }
      }
    }

__

|

"标签"字段中没有值的文档将属于与值为"N/A"的文档相同的存储桶。   ---|--- ### 嵌套、稀有术语和评分子聚合编辑

RareTerm 聚合必须在"breadth_first"模式下运行，因为它需要在超出文档计数阈值时修剪术语。此要求意味着 RareTerm 聚合与需要"depth_first"的某些聚合组合不兼容。特别是，对"嵌套"内的子聚合进行评分会强制整个聚合树以"depth_first"模式运行。这将引发异常，因为 RareTerm 无法处理"depth_first"。

举个具体的例子，如果"rare_terms"聚合是"嵌套"聚合的子聚合，并且"rare_terms"的子聚合之一需要 documentscores(如"top_hits"聚合)，这将引发异常。

[« Range aggregation](search-aggregations-bucket-range-aggregation.md)
[Reverse nested aggregation »](search-aggregations-bucket-reverse-nested-
aggregation.md)
