

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Significant terms aggregation](search-aggregations-bucket-significantterms-
aggregation.md) [Terms aggregation »](search-aggregations-bucket-terms-
aggregation.md)

## 重要文本聚合

返回集合中有趣或不寻常的自由文本术语的聚合。它类似于重要术语聚合但不同之处在于：

* 它专为用于类型"文本"字段而设计 * 它不需要字段数据或文档值 * 它即时重新分析文本内容，这意味着它还可以过滤嘈杂文本的重复部分，否则这些部分往往会扭曲统计数据。

重新分析 _large_ 结果集将需要大量的时间和内存。建议将significant_text聚合用作采样器或多样化采样器聚合的子项，以将分析限制为_小_选择的顶级匹配文档，例如 200。这通常会提高速度、内存使用和结果质量。

**示例用例：**

* 当用户搜索"禽流感"时建议使用"H5N1"，以帮助扩大查询范围 * 建议与股票代码$ATI相关的关键字，以便在自动新闻分类器中使用

在这些情况下，选择的单词不仅仅是结果中最受欢迎的术语。最流行的词往往非常无聊(_and，的，的，我们，我，they_......)。重要单词是在 _foreground_ and_background_ 集之间测量的流行度发生重大变化的单词。如果术语"H5N1"仅存在于1000万份文件索引中的5份文件中，但在构成用户搜索结果的100份文件中的4份文件中却被发现，那么该文献很重要，并且可能与他们的搜索非常相关。5/10，000，000 与 4/100 是频率的大幅波动。

### 基本使用

在典型用例中，感兴趣的 _foreground_ 集是查询的顶级匹配搜索结果的选择，用于统计比较的 _background_ 集是从中收集结果的一个或多个索引。

Example:

    
    
    response = client.search(
      index: 'news',
      body: {
        query: {
          match: {
            content: 'Bird flu'
          }
        },
        aggregations: {
          my_sample: {
            sampler: {
              shard_size: 100
            },
            aggregations: {
              keywords: {
                significant_text: {
                  field: 'content'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET news/_search
    {
      "query": {
        "match": { "content": "Bird flu" }
      },
      "aggregations": {
        "my_sample": {
          "sampler": {
            "shard_size": 100
          },
          "aggregations": {
            "keywords": {
              "significant_text": { "field": "content" }
            }
          }
        }
      }
    }

Response:

    
    
    {
      "took": 9,
      "timed_out": false,
      "_shards": ...,
      "hits": ...,
        "aggregations" : {
            "my_sample": {
                "doc_count": 100,
                "keywords" : {
                    "doc_count": 100,
                    "buckets" : [
                        {
                            "key": "h5n1",
                            "doc_count": 4,
                            "score": 4.71235374214817,
                            "bg_count": 5
                        }
                        ...
                    ]
                }
            }
        }
    }

结果表明，"h5n1"是与禽流感密切相关的几个术语之一。它在整个索引中只出现5次(见"bg_count")，但其中4次幸运地出现在我们的100个"禽流感"结果样本中。这表明一个重要的词，用户可以将其添加到他们的搜索中。

### 使用"filter_duplicate_text"处理嘈杂数据

自由文本字段通常包含原始内容和机械文本副本(剪切和粘贴传记、电子邮件回复链、转推、样板页眉/页脚、页面导航菜单、侧边栏新闻链接、版权声明、标准免责声明、地址)的混合。

在实际数据中，如果不过滤掉这些重复的文本部分，它们往往会在"significant_text"结果中占据重要位置。在索引时过滤近似重复的文本是一项艰巨的任务，但我们可以使用"filter_duplicate_text"设置在查询时即时清理数据。

首先，让我们看一个未经过滤的真实世界示例，该示例使用涵盖各种新闻的百万篇新闻文章的信号媒体数据集。以下是搜索提及"弹性搜索"的文章的原始文本结果：

    
    
    {
      ...
      "aggregations": {
        "sample": {
          "doc_count": 35,
          "keywords": {
            "doc_count": 35,
            "buckets": [
              {
                "key": "elasticsearch",
                "doc_count": 35,
                "score": 28570.428571428572,
                "bg_count": 35
              },
              ...
              {
                "key": "currensee",
                "doc_count": 8,
                "score": 6530.383673469388,
                "bg_count": 8
              },
              ...
              {
                "key": "pozmantier",
                "doc_count": 4,
                "score": 3265.191836734694,
                "bg_count": 4
              },
              ...
    
    }

未清理的文档抛出了一些看起来很奇怪的术语，从表面上看，这些术语与我们的搜索词"elasticsearch"(例如"pozmantier")的外观在统计上相关。我们可以向下钻取这些文档的示例，以了解为什么使用此查询连接 pozmantier：

    
    
    response = client.search(
      index: 'news',
      body: {
        query: {
          simple_query_string: {
            query: '+elasticsearch  +pozmantier'
          }
        },
        _source: [
          'title',
          'source'
        ],
        highlight: {
          fields: {
            content: {}
          }
        }
      }
    )
    puts response
    
    
    GET news/_search
    {
      "query": {
        "simple_query_string": {
          "query": "+elasticsearch  +pozmantier"
        }
      },
      "_source": [
        "title",
        "source"
      ],
      "highlight": {
        "fields": {
          "content": {}
        }
      }
    }

结果显示了一系列关于许多技术项目评审团的非常相似的新闻文章：

    
    
    {
      ...
      "hits": {
        "hits": [
          {
            ...
            "_source": {
              "source": "Presentation Master",
              "title": "T.E.N. Announces Nominees for the 2015 ISE® North America Awards"
            },
            "highlight": {
              "content": [
                "City of San Diego Mike <em>Pozmantier</em>, Program Manager, Cyber Security Division, Department of",
                " Janus, Janus <em>ElasticSearch</em> Security Visualization Engine "
              ]
            }
          },
          {
            ...
            "_source": {
              "source": "RCL Advisors",
              "title": "T.E.N. Announces Nominees for the 2015 ISE(R) North America Awards"
            },
            "highlight": {
              "content": [
                "Mike <em>Pozmantier</em>, Program Manager, Cyber Security Division, Department of Homeland Security S&T",
                "Janus, Janus <em>ElasticSearch</em> Security Visualization Engine"
              ]
            }
          },
          ...

Mike Pozmantier是小组的众多评委之一，elasticsearch被用于许多被评判的项目之一。

通常情况下，这篇冗长的新闻稿是由各种新闻网站剪切和粘贴的，因此它们包含的任何罕见名称、数字或拼写错误都与我们的匹配查询在统计上相关。

幸运的是，类似的文档往往排名相似，因此作为检查顶级匹配文档流的一部分，significant_text聚合可以应用过滤器来删除已经看到的任何 6 个或更多令牌的序列。现在让我们尝试同样的查询，但打开了"filter_duplicate_text"设置：

    
    
    response = client.search(
      index: 'news',
      body: {
        query: {
          match: {
            content: 'elasticsearch'
          }
        },
        aggregations: {
          sample: {
            sampler: {
              shard_size: 100
            },
            aggregations: {
              keywords: {
                significant_text: {
                  field: 'content',
                  filter_duplicate_text: true
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET news/_search
    {
      "query": {
        "match": {
          "content": "elasticsearch"
        }
      },
      "aggs": {
        "sample": {
          "sampler": {
            "shard_size": 100
          },
          "aggs": {
            "keywords": {
              "significant_text": {
                "field": "content",
                "filter_duplicate_text": true
              }
            }
          }
        }
      }
    }

对于熟悉弹性堆栈的人来说，分析重复数据删除文本的结果显然质量更高：

    
    
    {
      ...
      "aggregations": {
        "sample": {
          "doc_count": 35,
          "keywords": {
            "doc_count": 35,
            "buckets": [
              {
                "key": "elasticsearch",
                "doc_count": 22,
                "score": 11288.001166180758,
                "bg_count": 35
              },
              {
                "key": "logstash",
                "doc_count": 3,
                "score": 1836.648979591837,
                "bg_count": 4
              },
              {
                "key": "kibana",
                "doc_count": 3,
                "score": 1469.3020408163263,
                "bg_count": 5
              }
            ]
          }
        }
      }
    }

Pozmantier先生和其他与elasticsearch的一次性关联不再出现在聚合结果中，这是复制粘贴操作或其他形式的机械重复的结果。

如果您的重复或近似重复的内容可以通过单值索引字段(可能是文章的"标题"文本或"original_press_release_url"字段的哈希值)识别，那么使用父级多元化采样器聚合从基于该单个键的样本集中消除这些文档会更有效。您可以预先输入到significant_text聚合中的重复内容越少，性能就越好。

**如何计算显著性分数？

为分数返回的数字主要用于对不同的建议进行合理的排名，而不是最终用户容易理解的内容。分数来自 _foreground_ 和 _background_sets 中的文档频率。简而言之，如果一个术语在子集和背景中出现的频率存在明显差异，则认为该术语具有重要意义。可以配置术语的排名方式，请参阅"参数"部分。

**使用 _"像这样但不是这样"_ 模式**

您可以通过首先搜索结构化字段来发现错误分类的内容，例如"类别：成人电影"并在文本"movie_description"字段中使用significant_text。采用建议的单词(我会把它们留给你想象)，然后搜索所有未标记为类别：成人电影但包含这些关键字的电影。您现在有一个分类不良的电影的排名列表，您应该重新分类或至少从"家庭友好"类别中删除。

每个术语的显著性分数还可以提供有用的"提升"设置来对匹配项进行排序。将"terms"查询的"minimum_should_match"设置与关键字一起使用将有助于控制结果集中精度/召回率的平衡，即高设置将包含少量相关结果，其中包含关键字，而设置为"1"将生成更详尽的结果集，其中包含所有包含_any_keyword的文档。

###Limitations

#### 不支持子聚合

significant_text聚合有意不支持添加子聚合，因为：

*这将带来很高的内存成本*这不是一个通常有用的功能，对于那些需要它的人来说，有一个解决方法

候选术语的数量通常非常高，在返回最终结果之前，这些术语会被大量修剪。支持子聚合会产生额外的流失，并且效率低下。客户端始终可以从"significant_text"请求中获取大量修剪的结果集，并使用带有"include"子句和子句的"terms"聚合进行后续后续查询，以更有效的方式对所选关键字执行进一步分析。

#### 不支持嵌套对象

significant_text聚合目前也不能与嵌套对象中的文本字段一起使用，因为它适用于文档 JSON 源。这使得此功能在匹配存储的 JSON 中的嵌套文档时效率低下，给定匹配的 Lucene docID。

#### 近似计数

包含结果中提供的项的文档数的计数基于对每个分片返回的样本求和，因此可能是：

* 如果某些分片未在其顶部样本中提供给定术语的数字，则为低 * 考虑背景频率时为高，因为它可能会计算在已删除文档中发现的出现次数

与大多数设计决策一样，这是权衡的基础，我们选择以一些(通常是小的)不准确性为代价来提供快速性能。但是，下一节中介绍的"大小"和"分片大小"设置提供了帮助控制精度级别的工具。

###Parameters

#### 意义启发式

此聚合支持与重要术语聚合相同的评分启发式(JLH、mutual_information、gnd、chi_square 等)

#### 大小和分片大小

可以设置"size"参数来定义应从整个术语列表中返回多少术语存储桶。默认情况下，协调搜索过程的节点将请求每个分片提供自己的顶级术语存储桶，一旦所有分片响应，它将结果减少到最终列表，然后将返回给客户端。如果唯一字词的数量大于"大小"，则返回的列表可能略有偏差且不准确(可能是字词计数略有偏差，甚至可能是本应位于最大大小存储桶中的字词未返回)。

为了确保更好的准确性，使用最终"大小"的倍数作为每个分片请求的项数("2 *(大小* 1.5 + 10)")。要手动控制此设置，可以使用"shard_size"参数来控制每个分片生成的候选项的数量。

一旦合并了所有结果，低频项就会成为最有趣的项，因此当"shard_size"参数设置为明显高于"大小"设置的值时，significant_terms聚合可以产生更高质量的结果。这可确保在最终选择之前，减少节点对大量有希望的候选术语进行合并审查。显然，大型候选术语列表会导致网络外流量和 RAM 使用，因此这是需要平衡的质量/成本权衡。如果"shard_size"设置为 -1(默认值)，则将根据分片数量和"size"参数自动估计"shard_size"。

"shard_size"不能小于"大小"(因为它没有多大意义)。如果是，elasticsearch将覆盖它并将其重置为等于"size"。

#### 最小文档数

可以使用"min_doc_count"选项仅返回匹配超过配置的命中数的字词。默认值为 3。

得分高的术语将在分片级别收集，并在第二步中与从其他分片收集的术语合并。但是，分片没有有关可用全局术语频率的信息。是否将术语添加到候选列表的决定仅取决于使用本地分片频率在分片上计算的分数，而不是单词的全局频率。"min_doc_count"标准仅在合并所有分片的本地术语统计信息后应用。在某种程度上，将术语添加为候选人的决定是在没有非常_确定_该术语是否实际达到所需的"min_doc_count"的情况下做出的。如果候选人列表中填充了低频率但得分高的术语，这可能会导致最终结果中缺少许多(全局)高频率术语。为了避免这种情况，可以增加"shard_size"参数以允许分片上有更多的候选项。但是，这会增加内存消耗和网络流量。

#####'shard_min_doc_count'

参数"shard_min_doc_count"规定了分片是否应该将该术语添加到候选列表中与"min_doc_count"相关的_确定性_。仅当术语在集合中的本地分片频率高于"shard_min_doc_count"时，才会考虑术语。如果您的字典包含许多低频率术语，并且您对这些术语不感兴趣(例如拼写错误)，那么您可以设置 'shard_min_doc_count' 参数以在分片级别过滤掉候选术语，即使在合并本地计数后，这些候选术语也不会达到所需的"min_doc_count"。默认情况下，"shard_min_doc_count"设置为"0"，除非您明确设置，否则无效。

通常不建议将"min_doc_count"设置为"1"，因为它往往会返回拼写错误或其他奇怪的好奇心。找到一个术语的多个实例有助于强化这一点，虽然仍然很少见，但该术语不是一次性事故的结果。默认值 3 用于提供最小证据权重。将"shard_min_doc_count"设置得太高将导致在分片级别过滤掉重要的候选术语。此值应设置为远低于"min_doc_count/#shards"。

#### 自定义背景上下文

背景术语频率的默认统计信息来源是整个索引，可以通过使用"background_filter"来缩小范围，以关注较窄上下文中的重要术语：

    
    
    response = client.search(
      index: 'news',
      body: {
        query: {
          match: {
            content: 'madrid'
          }
        },
        aggregations: {
          tags: {
            significant_text: {
              field: 'content',
              background_filter: {
                term: {
                  content: 'spain'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET news/_search
    {
      "query": {
        "match": {
          "content": "madrid"
        }
      },
      "aggs": {
        "tags": {
          "significant_text": {
            "field": "content",
            "background_filter": {
              "term": { "content": "spain" }
            }
          }
        }
      }
    }

上述过滤器将有助于关注马德里市特有的术语，而不是揭示像"西班牙语"这样的术语，这些术语在完整索引的全球背景下是不寻常的，但在包含"西班牙"一词的文件子集中却司空见惯。

使用后台过滤器会减慢查询速度，因为必须过滤每个术语的帖子以确定频率

#### 处理源映射和索引映射

通常，索引字段名称和要检索的原始 JSON 字段共享相同的名称。但是，对于使用"copy_to"等功能的更复杂的字段映射，源 JSON 字段和正在聚合的索引字段可能会有所不同。在这些情况下，可以使用"source_fields"参数列出 JSON _source字段，从中分析文本：

    
    
    response = client.search(
      index: 'news',
      body: {
        query: {
          match: {
            custom_all: 'elasticsearch'
          }
        },
        aggregations: {
          tags: {
            significant_text: {
              field: 'custom_all',
              source_fields: [
                'content',
                'title'
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET news/_search
    {
      "query": {
        "match": {
          "custom_all": "elasticsearch"
        }
      },
      "aggs": {
        "tags": {
          "significant_text": {
            "field": "custom_all",
            "source_fields": [ "content", "title" ]
          }
        }
      }
    }

#### 筛选值

可以(尽管很少需要)筛选将为其创建存储桶的值。这可以使用基于正则表达式字符串或精确术语数组的"include"和"exclude"参数来完成。此功能反映了术语聚合文档中描述的功能。

[« Significant terms aggregation](search-aggregations-bucket-significantterms-
aggregation.md) [Terms aggregation »](search-aggregations-bucket-terms-
aggregation.md)
