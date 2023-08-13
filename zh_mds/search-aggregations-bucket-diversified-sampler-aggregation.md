

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Date range aggregation](search-aggregations-bucket-daterange-
aggregation.md) [Filter aggregation »](search-aggregations-bucket-filter-
aggregation.md)

## 多样化的采样器聚合

与"采样器"聚合一样，这是一个过滤聚合，用于将任何子聚合的处理限制为得分最高的文档样本。"diversified_sampler"聚合增加了限制共享公共值(如"作者")的匹配项数的功能。

任何优秀的市场研究人员都会告诉你，在处理数据样本时，重要的是样本代表健康的各种意见，而不是被任何单一的声音所扭曲。聚合也是如此，使用这些多样化设置进行采样可以提供一种方法来消除内容中的偏见(人口过多的地理位置、时间线中的大峰值或过度活跃的论坛垃圾邮件发送者)。

**示例用例：**

* 将分析的重点集中在高相关性匹配上，而不是低质量匹配的潜在长尾 * 通过确保公平表示来自不同来源的内容来消除分析中的偏见 * 降低聚合的运行成本，这些聚合可以仅使用样本(例如"significant_terms")产生有用的结果

"字段"设置用于提供用于重复数据消除的值，"max_docs_per_value"设置控制在共享公共值的任何一个分片上收集的最大文档数。"max_docs_per_value"的默认设置为 1。

如果"字段"为单个文档生成多个值，则聚合将引发错误(由于效率问题，不支持使用多值字段进行重复数据消除)。

Example:

我们可能想看看哪些标签与 StackOverflow 论坛帖子上的"#elasticsearch"密切相关，但忽略了一些多产用户的影响，他们倾向于将 #Kibana 拼写错误为 #Cabana。

    
    
    response = client.search(
      index: 'stackoverflow',
      size: 0,
      body: {
        query: {
          query_string: {
            query: 'tags:elasticsearch'
          }
        },
        aggregations: {
          my_unbiased_sample: {
            diversified_sampler: {
              shard_size: 200,
              field: 'author'
            },
            aggregations: {
              keywords: {
                significant_terms: {
                  field: 'tags',
                  exclude: [
                    'elasticsearch'
                  ]
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /stackoverflow/_search?size=0
    {
      "query": {
        "query_string": {
          "query": "tags:elasticsearch"
        }
      },
      "aggs": {
        "my_unbiased_sample": {
          "diversified_sampler": {
            "shard_size": 200,
            "field": "author"
          },
          "aggs": {
            "keywords": {
              "significant_terms": {
                "field": "tags",
                "exclude": [ "elasticsearch" ]
              }
            }
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "my_unbiased_sample": {
          "doc_count": 151,           __"keywords": { __"doc_count": 151,
            "bg_count": 650,
            "buckets": [
              {
                "key": "kibana",
                "doc_count": 150,
                "score": 2.213,
                "bg_count": 200
              }
            ]
          }
        }
      }
    }

__

|

共抽样了151份文件。   ---|---    __

|

significant_terms聚合的结果不会因任何单一作者的怪癖而扭曲，因为我们要求样本中的任何一位作者最多发表一篇文章。   ### 脚本示例编辑

在这种情况下，我们可能希望字段值的组合多样化。我们可以使用运行时字段生成标签字段中多个值的哈希值，以确保我们没有由相同的重复标签组合组成的样本。

    
    
    response = client.search(
      index: 'stackoverflow',
      size: 0,
      body: {
        query: {
          query_string: {
            query: 'tags:kibana'
          }
        },
        runtime_mappings: {
          "tags.hash": {
            type: 'long',
            script: "emit(doc['tags'].hashCode())"
          }
        },
        aggregations: {
          my_unbiased_sample: {
            diversified_sampler: {
              shard_size: 200,
              max_docs_per_value: 3,
              field: 'tags.hash'
            },
            aggregations: {
              keywords: {
                significant_terms: {
                  field: 'tags',
                  exclude: [
                    'kibana'
                  ]
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /stackoverflow/_search?size=0
    {
      "query": {
        "query_string": {
          "query": "tags:kibana"
        }
      },
      "runtime_mappings": {
        "tags.hash": {
          "type": "long",
          "script": "emit(doc['tags'].hashCode())"
        }
      },
      "aggs": {
        "my_unbiased_sample": {
          "diversified_sampler": {
            "shard_size": 200,
            "max_docs_per_value": 3,
            "field": "tags.hash"
          },
          "aggs": {
            "keywords": {
              "significant_terms": {
                "field": "tags",
                "exclude": [ "kibana" ]
              }
            }
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "my_unbiased_sample": {
          "doc_count": 6,
          "keywords": {
            "doc_count": 6,
            "bg_count": 650,
            "buckets": [
              {
                "key": "logstash",
                "doc_count": 3,
                "score": 2.213,
                "bg_count": 50
              },
              {
                "key": "elasticsearch",
                "doc_count": 3,
                "score": 1.34,
                "bg_count": 200
              }
            ]
          }
        }
      }
    }

###shard_size

"shard_size"参数限制在每个分片上处理的样本中收集的得分最高的文档数。默认值为 100。

###max_docs_per_value

"max_docs_per_value"是一个可选参数，它限制每个重复数据消除值选择允许的文档数。默认设置为"1"。

###execution_hint

可选的"execution_hint"设置会影响用于重复数据消除的值的管理。执行重复数据消除时，每个选项最多可以在内存中保留"shard_size"值，但可以按如下方式控制保存的值类型：

* 直接保存字段值("map") * 保存由 Lucene 索引确定的字段序数 ('global_ordinals') * 保存字段值的哈希值 - 可能会发生哈希冲突 ('bytes_hash')

默认设置是，如果此信息可从 Luceneindex 获得，则使用"global_ordinals"，如果没有，则恢复为"map"。在某些情况下，"bytes_hash"设置可能会更快，但由于可能存在哈希冲突，因此会在重复数据消除逻辑中引入误报的可能性。请注意，如果执行提示的选择不适用，Elasticsearch 将忽略它，并且这些提示没有向后兼容性保证。

###Limitations

#### 不能嵌套在"breadth_first"聚合下

作为基于质量的筛选器，diversified_sampler聚合需要访问为每个文档生成的相关性分数。因此，它不能嵌套在"条款"聚合下，该聚合将"collect_mode"从默认的"depth_first"模式切换到"breadth_first"，因为这会丢弃分数。在这种情况下，将引发错误。

#### 有限的去重复逻辑。

重复数据消除逻辑仅适用于分片级别，因此不会跨分片应用。

#### 地理/日期字段没有专门的语法

目前，定义多样化值的语法是通过选择"字段"或"脚本"来定义的 - 没有添加语法糖来表达地理或日期单位，例如"7d"(7 天)。此支持可能会在以后的版本中添加，用户当前必须使用脚本创建这些类型的值。

[« Date range aggregation](search-aggregations-bucket-daterange-
aggregation.md) [Filter aggregation »](search-aggregations-bucket-filter-
aggregation.md)
