

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Stats aggregation](search-aggregations-metrics-stats-aggregation.md) [Sum
aggregation »](search-aggregations-metrics-sum-aggregation.md)

## 字符串统计聚合

一种"多值"指标聚合，用于计算从聚合文档中提取的字符串值的统计信息。这些值可以从特定的"关键字"字段中检索。

字符串统计信息聚合返回以下结果：

* 'count' \- 计数的非空字段数。  * 'min_length' \- 最短期限的长度。  * "max_length" \- 最长期限的长度。  * 'avg_length' \- 计算所有项的平均长度。  * "熵" \- 香农熵)值计算聚合收集的所有项。香农熵量化了字段中包含的信息量。对于测量数据集的各种属性(例如多样性，相似性，随机性等)而言，这是一个非常有用的指标。

例如：

    
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          message_stats: {
            string_stats: {
              field: 'message.keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /my-index-000001/_search?size=0
    {
      "aggs": {
        "message_stats": { "string_stats": { "field": "message.keyword" } }
      }
    }

上面的聚合计算所有文档中"消息"字段的字符串统计信息。聚合类型为"string_stats"，"字段"参数定义将计算统计信息的文档字段。以上将返回以下内容：

    
    
    {
      ...
    
      "aggregations": {
        "message_stats": {
          "count": 5,
          "min_length": 24,
          "max_length": 30,
          "avg_length": 28.8,
          "entropy": 3.94617750050791
        }
      }
    }

聚合的名称(上面的"message_stats")也用作可以从返回的响应中检索聚合结果的键。

### 字符分布

香农熵值的计算基于聚合收集的所有术语中每个字符出现的概率。要查看所有字符的概率分布，我们可以添加"show_distribution"(默认："false")参数。

    
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          message_stats: {
            string_stats: {
              field: 'message.keyword',
              show_distribution: true
            }
          }
        }
      }
    )
    puts response
    
    
    POST /my-index-000001/_search?size=0
    {
      "aggs": {
        "message_stats": {
          "string_stats": {
            "field": "message.keyword",
            "show_distribution": true  __}
        }
      }
    }

__

|

将"show_distribution"参数设置为"true"，以便在结果中返回所有字符的概率分布。   ---|---                {      ...         "聚合"： { "message_stats"： { "计数"： 5， "min_length"： 24， "max_length"： 30， "avg_length"： 28.8， "熵"： 3.94617750050791， "分布"： { " "： 0.15277777777777778， "e"： 0.14583333333333334， "s"： 0.09722222222222222， "m"： 0.083333333333333333， "t"： 0.0763888888888889， "h"： 0.0625， "a"： 0.04166666666666666664， "i"： 0.041666666666666666664，           "r"： 0.0416666666666666664， "g"： 0.034722222222222224， "n"： 0.034722222222222224， "o"： 0.0.034722222222222222， "u"： 0.03472222222222222， "b"： 0.027777777777777777776， "w"： 0.027777777777777776， "c"： 0.0138888888888888888， "E"： 0.0069444444444444444， "l"： 0.0069444444444444444， "1"： 0.00694444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444           "4"： 0.0069444444444444444， "y"： 0.00694444444444444 } } } }

"分布"对象显示每个字符在所有术语中出现的概率。字符按降序概率排序。

###Script

如果需要获取比单个字段更复杂的内容的"string_stats"，请在运行时字段上运行聚合。

    
    
    POST /my-index-000001/_search
    {
      "size": 0,
      "runtime_mappings": {
        "message_and_context": {
          "type": "keyword",
          "script": """
            emit(doc['message.keyword'].value + ' ' + doc['context.keyword'].value)
          """
        }
      },
      "aggs": {
        "message_stats": {
          "string_stats": { "field": "message_and_context" }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          message_stats: {
            string_stats: {
              field: 'message.keyword',
              missing: '[empty message]'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /my-index-000001/_search?size=0
    {
      "aggs": {
        "message_stats": {
          "string_stats": {
            "field": "message.keyword",
            "missing": "[empty message]" __}
        }
      }
    }

__

|

"消息"字段中没有值的文档将被视为具有值"空消息]"的文档。   ---|--- [« 统计聚合 总和聚合 »