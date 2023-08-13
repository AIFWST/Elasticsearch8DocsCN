

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Sampler aggregation](search-aggregations-bucket-sampler-aggregation.md)
[Significant text aggregation »](search-aggregations-bucket-significanttext-
aggregation.md)

## 重要术语聚合

返回 aset 中有趣或不寻常的术语的聚合。

**示例用例：**

*当用户在文本中搜索"禽流感"时建议"H5N1" *从信用卡所有者报告损失的交易历史记录中识别出"共同妥协点"的商家 *建议与自动新闻分类器的股票代码$ATI相关的关键字 *发现欺诈医生，他正在诊断超过他们公平份额的鞭打伤害 *发现爆胎次数不成比例的轮胎制造商

在所有这些情况下，选择的术语不仅仅是一组中最受欢迎的术语。它们是在 _foreground_ 和 _background_ 集之间发生重大变化的术语。如果术语"H5N1"仅存在于1000万个文档索引中的5个文档中，但在构成用户搜索结果的100个文档中的4个文档中，这些文档很重要，并且可能与他们的搜索非常相关。5/10，000，000 与 4/100 的频率波动很大。

### 单集分析

在最简单的情况下，感兴趣的 _foreground_ 集是与查询匹配的搜索结果，用于统计比较的 _background_ 集是收集结果的一个或多个索引。

Example:

    
    
    response = client.search(
      body: {
        query: {
          terms: {
            force: [
              'British Transport Police'
            ]
          }
        },
        aggregations: {
          significant_crime_types: {
            significant_terms: {
              field: 'crime_type'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "terms": { "force": [ "British Transport Police" ] }
      },
      "aggregations": {
        "significant_crime_types": {
          "significant_terms": { "field": "crime_type" }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "significant_crime_types": {
          "doc_count": 47347,
          "bg_count": 5064554,
          "buckets": [
            {
              "key": "Bicycle theft",
              "doc_count": 3640,
              "score": 0.371235374214817,
              "bg_count": 66799
            }
                  ...
          ]
        }
      }
    }

当查询所有警察部队的所有犯罪指数时，这些结果表明，英国交通警察部队在处理不成比例的大量自行车盗窃案时脱颖而出。通常，自行车盗窃仅占犯罪的1%(66799/5064554)，但对于在铁路和车站处理犯罪的英国交通警察来说，7%的犯罪(3640/47347)是自行车盗窃。这是显著增加七倍的频率，因此这种异常被强调为顶级犯罪类型。

使用查询来发现异常的问题在于，它只为我们提供了一个用于比较的子集。要发现所有其他警察部队的异常情况，我们必须对每个不同的部队重复查询。

这可能是在索引中查找异常模式的繁琐方法。

### 多集分析

跨多个类别执行分析的更简单方法是使用父级聚合对准备进行分析的数据进行分段。

使用父聚合进行分段的示例：

    
    
    response = client.search(
      body: {
        aggregations: {
          forces: {
            terms: {
              field: 'force'
            },
            aggregations: {
              significant_crime_types: {
                significant_terms: {
                  field: 'crime_type'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggregations": {
        "forces": {
          "terms": { "field": "force" },
          "aggregations": {
            "significant_crime_types": {
              "significant_terms": { "field": "crime_type" }
            }
          }
        }
      }
    }

Response:

    
    
    {
     ...
     "aggregations": {
        "forces": {
            "doc_count_error_upper_bound": 1375,
            "sum_other_doc_count": 7879845,
            "buckets": [
                {
                    "key": "Metropolitan Police Service",
                    "doc_count": 894038,
                    "significant_crime_types": {
                        "doc_count": 894038,
                        "bg_count": 5064554,
                        "buckets": [
                            {
                                "key": "Robbery",
                                "doc_count": 27617,
                                "score": 0.0599,
                                "bg_count": 53182
                            }
                            ...
                        ]
                    }
                },
                {
                    "key": "British Transport Police",
                    "doc_count": 47347,
                    "significant_crime_types": {
                        "doc_count": 47347,
                        "bg_count": 5064554,
                        "buckets": [
                            {
                                "key": "Bicycle theft",
                                "doc_count": 3640,
                                "score": 0.371,
                                "bg_count": 66799
                            }
                            ...
                        ]
                    }
                }
            ]
        }
      }
    }

现在，我们可以使用单个请求对每个警察部队进行异常检测。

我们可以使用其他形式的顶级聚合来细分我们的数据，例如按地理区域细分以识别特定犯罪类型的异常热点：

    
    
    response = client.search(
      body: {
        aggregations: {
          hotspots: {
            geohash_grid: {
              field: 'location',
              precision: 5
            },
            aggregations: {
              significant_crime_types: {
                significant_terms: {
                  field: 'crime_type'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "hotspots": {
          "geohash_grid": {
            "field": "location",
            "precision": 5
          },
          "aggs": {
            "significant_crime_types": {
              "significant_terms": { "field": "crime_type" }
            }
          }
        }
      }
    }

此示例使用"geohash_grid"聚合来创建表示地理区域的结果存储桶，在每个存储桶中，我们可以识别这些紧密集中区域中犯罪类型的异常级别，例如

*机场表现出异常数量的武器没收 *大学显示自行车盗窃案有所增加

在更高的geohash_grid缩放级别和更大的覆盖区域，我们将开始看到整个警察部队可能正在处理异常数量的特定犯罪类型。

显然，基于时间的顶级细分将有助于识别每个时间点的当前趋势，其中简单的"术语"聚合通常会显示跨所有时隙的非常流行的"常量"。

**分数是如何计算的？

为分数返回的数字主要用于对不同的建议进行合理的排名，而不是最终用户容易理解的内容。分数来自 _foreground_ 和 _background_sets 中的文档频率。简而言之，如果一个术语在子集和背景中出现的频率存在明显差异，则认为该术语具有重要意义。可以配置术语的排名方式，请参阅"参数"部分。

### 在自由文本字段上使用

significant_terms聚合可以有效地用于标记化的自由文本字段，以建议：

* 用于优化最终用户搜索的关键字 * 用于渗滤器查询的关键字

选择一个自由文本字段作为重要术语分析的主题可能会很昂贵！它将尝试将每个唯一的单词加载到 RAM 中。建议仅在较小的索引上使用它。

**使用 _"像这样但不是这样"_ 模式**

您可以通过首先搜索结构化字段来发现错误分类的内容，例如"类别：成人电影"，并在自由文本"movie_description"字段中使用significant_terms。采用建议的单词(我会把它们留给你想象)，然后搜索所有未标记为类别：成人电影但包含这些关键字的电影。您现在有一个分类不良的电影的排名列表，您应该重新分类或至少从"家庭友好"类别中删除。

每个术语的显著性分数还可以提供有用的"提升"设置来对匹配项进行排序。将"terms"查询的"minimum_should_match"设置与关键字一起使用将有助于控制结果集中精度/召回率的平衡，即高设置将包含少量相关结果，其中包含关键字，而设置为"1"将生成更详尽的结果集，其中包含所有包含_any_keyword的文档。

**在上下文中显示significant_terms** 在上下文中查看时，自由文本significant_terms更容易理解。从自由文本字段中获取"significant_terms"建议的结果，并在带有"突出显示"子句的同一字段的"术语"查询中使用它们，以向用户显示文档的示例片段。当术语不带词干、突出显示、以正确的大小写、正确的顺序和一些上下文呈现时，它们的意义/含义就更容易显现出来。

### 自定义背景集

通常，前台文档集与索引中所有文档的背景集"不同"。但是，有时使用较窄的背景集作为比较的基础可能会很有用。例如，在包含世界各地内容的索引中查询与"马德里"有关的文件可能会发现"西班牙文"是一个重要的术语。这可能是真的，但如果你想要一些更集中的术语，你可以在术语_spain_上使用"background_filter"来建立一组更窄的文档作为上下文。以此为背景，"西班牙语"现在将被视为司空见惯，因此不如与马德里更紧密相关的"首都"等词重要。请注意，使用后台过滤器会减慢速度 - 每个术语的背景频率现在必须从过滤发布列表中即时派生，而不是读取索引预先计算的术语计数。

###Limitations

#### 重要术语必须是索引值

与术语聚合不同，目前无法使用脚本生成的术语进行计数。由于聚合thesignificant_terms必须同时考虑 _foreground_ 和 _background_frequencies 的方式，因此在整个索引上使用脚本来获取背景频率进行比较的成本过高。此外，出于类似原因，不支持将文档值作为术语数据源。

#### 不分析浮点字段

目前不支持将浮点字段作为分析的主题ofsignificant_terms。虽然整数或长字段可用于表示银行帐号或类别编号等概念，这些概念可能很有趣，但浮点字段通常用于表示某物的数量。因此，单个浮点项对于这种形式的频率分析没有用处。

#### 用作父聚合

如果存在等效的"match_all"查询或没有查询条件提供索引的子集，则不应将significant_terms聚合用作最顶层的聚合 - 在这种情况下，_foreground_ 集与 _background_ 集完全相同，因此文档内没有要观察的频率差异，并从中提出明智的建议。

另一个考虑因素是，significant_terms聚合在分片级别生成许多候选结果，只有在合并所有分片的所有统计信息后，这些结果才会在 reducingnode 上进行修剪。因此，在 RAM 方面，在后来丢弃许多候选术语的聚合下嵌入大型子聚合可能效率低下且成本高昂significant_terms。在这些情况下，建议执行两次搜索 - 第一次提供不合理的significant_terms列表，然后将此术语候选列表添加到第二个查询中，以返回并获取所需的子聚合。

#### 近似计数

包含结果中提供的项的文档数的计数基于对每个分片返回的样本求和，因此可能是：

* 如果某些分片未在其顶部样本中提供给定术语的数字，则为低 * 考虑背景频率时为高，因为它可能会计算在已删除文档中发现的出现次数

与大多数设计决策一样，这是权衡的基础，我们选择以一些(通常是小的)不准确性为代价来提供快速性能。但是，下一节中介绍的"大小"和"分片大小"设置提供了帮助控制精度级别的工具。

###Parameters

#### JLHscore

JLH 分数可以通过添加参数用作显著性分数

    
    
    	 "jlh": {
    	 }

分数来自 _foreground_ and_background_ 集中的文档频率。流行度的绝对变化(前景百分比-背景百分比)将有利于常用术语，而_相对_变化流行度(前景百分比/背景百分比)将有利于稀有术语。Rarevs 常见本质上是精度与召回率的平衡，因此绝对和相对变化相乘，以提供精度和召回率之间的最佳平衡点。

#### 互助信息

Manning 等人第 13.5.1 章中描述的互信息可以通过添加参数作为显著性得分

    
    
    	 "mutual_information": {
    	      "include_negatives": true
    	 }

互信息不区分描述子集或子集外文档的术语。因此，有效项可以包含子集中出现频率高于子集外的项。要过滤掉子集中出现频率低于子集外文档中出现的术语，可以将"include_negatives"设置为"false"。

默认情况下，假设存储桶中的文档也包含在后台。相反，如果您定义了表示要比较的另一组文档的自定义背景筛选器，请将

    
    
    "background_is_superset": false

#### 赤方

Manning 等人第 13.5.2 章中描述的"信息检索"中所述的卡方可以通过添加参数作为显著性分数

    
    
    	 "chi_square": {
    	 }

卡方的行为类似于互信息，可以使用相同的参数"include_negatives"和"background_is_superset"进行配置。

#### 谷歌标准化距离

谷歌归一化距离如"谷歌相似性距离"中所述，Cilibrasi 和 Vitanyi，2007 年可以通过添加参数作为显著性分数

    
    
    	 "gnd": {
    	 }

"gnd"也接受"background_is_superset"参数。

#### p-valuescore

p 值是在假设原假设正确的情况下，获得检验结果至少与实际观察到的结果一样极端的概率。计算 p 值时，假设前景集和背景集是独立的伯努利试验，原假设概率相同。

##### 示例用法

本示例计算术语"user_agent.version"的 p 值得分，给定"以失败结束"与"未以失败结束"的前景集。

"background_is_superset"：false"表示背景集不包含前景集的计数，因为它们被过滤掉。

"normalize_above"：1000' 有助于在不同尺度上返回一致的显著性结果。"1000"表示大于"1000"的术语计数按"1000/term_count"的系数缩小。

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            filter: [
              {
                term: {
                  "event.outcome": 'failure'
                }
              },
              {
                range: {
                  "@timestamp": {
                    gte: '2021-02-01',
                    lt: '2021-02-04'
                  }
                }
              },
              {
                term: {
                  "service.name": {
                    value: 'frontend-node'
                  }
                }
              }
            ]
          }
        },
        aggregations: {
          failure_p_value: {
            significant_terms: {
              field: 'user_agent.version',
              background_filter: {
                bool: {
                  must_not: [
                    {
                      term: {
                        "event.outcome": 'failure'
                      }
                    }
                  ],
                  filter: [
                    {
                      range: {
                        "@timestamp": {
                          gte: '2021-02-01',
                          lt: '2021-02-04'
                        }
                      }
                    },
                    {
                      term: {
                        "service.name": {
                          value: 'frontend-node'
                        }
                      }
                    }
                  ]
                }
              },
              p_value: {
                background_is_superset: false,
                normalize_above: 1000
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "bool": {
          "filter": [
            {
              "term": {
                "event.outcome": "failure"
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": "2021-02-01",
                  "lt": "2021-02-04"
                }
              }
            },
            {
              "term": {
                "service.name": {
                  "value": "frontend-node"
                }
              }
            }
          ]
        }
      },
      "aggs": {
        "failure_p_value": {
          "significant_terms": {
            "field": "user_agent.version",
            "background_filter": {
              "bool": {
                "must_not": [
                  {
                    "term": {
                      "event.outcome": "failure"
                    }
                  }
                ],
                "filter": [
                  {
                    "range": {
                      "@timestamp": {
                        "gte": "2021-02-01",
                        "lt": "2021-02-04"
                      }
                    }
                  },
                  {
                    "term": {
                      "service.name": {
                        "value": "frontend-node"
                      }
                    }
                  }
                ]
              }
            },
            "p_value": {"background_is_superset": false, "normalize_above": 1000}
          }
        }
      }
    }

####Percentage

简单计算前景样本中的文档数(含项除以背景中带项的文档数)。默认情况下，这将产生大于零且小于 1 的分数。

这种启发式的好处是，评分逻辑很容易向熟悉"人均"统计数据的人解释。但是，对于具有高基数的字段，这种启发式方法倾向于选择最稀有的术语，例如仅出现一次的拼写错误，因为它们的得分为 1/1 = 100%。

如果纯粹根据赢得比赛的百分比来颁发奖项，那么经验丰富的拳击手将很难赢得冠军——根据这些规则，只有一场战斗的新人是不可能被击败的。通常需要多个观测值来强化视图，因此在这些情况下，建议将"min_doc_count"和"shard_min_doc_count"设置为更高的值，例如 10，以过滤掉否则优先的低频项。

    
    
    	 "percentage": {
    	 }

#### 哪一个最好？

粗略地说，"mutual_information"更喜欢高频率的术语，即使它们在后台也经常出现。例如，在对自然语言文本的分析中，这可能会导致选择停用词。"mutual_information"不太可能选择拼写错误等非常罕见的术语。"GND"首选具有高度重现的术语，并避免选择非索引字。它可能更适合同义词检测。然而，"gnd"倾向于选择非常罕见的术语，例如，拼写错误的结果。"chi_square"和"jlh"介于两者之间。

很难说哪一种不同的启发式是最佳选择，因为它取决于重要术语的用途(例如参见Yang和Pedersen，"文本分类中特征选择的比较研究"，1997年关于使用重要术语进行文本分类的特征选择的研究)。

如果上述度量都不适合您的用例，则另一个选项是实现自定义显著性度量：

####Scripted

自定义分数可以通过脚本实现：

    
    
    	    "script_heuristic": {
                  "script": {
    	        "lang": "painless",
    	        "source": "params._subset_freq/(params._superset_freq - params._subset_freq + 1)"
    	      }
                }

脚本可以是内联的(如上面的示例)、索引或存储在磁盘上。有关选项的详细信息，请参阅脚本文档。

脚本中的可用参数为

`_subset_freq`

|

术语出现在子集中的文档数。   ---|--- "_superset_freq"

|

术语出现在超集中的文档数。   "_subset_size"

|

子集中的文档数。   "_superset_size"

|

超集中的文档数。   #### Size & ShardSizeedit

可以设置"size"参数来定义应从整个术语列表中返回多少术语存储桶。默认情况下，协调搜索过程的节点将请求每个分片提供自己的顶级术语存储桶，一旦所有分片响应，它将结果减少到最终列表，然后将返回给客户端。如果唯一字词的数量大于"大小"，则返回的列表可能略有偏差且不准确(可能是字词计数略有偏差，甚至可能是本应位于最大大小存储桶中的字词未返回)。

为了确保更好的准确性，使用最终"大小"的倍数作为每个分片请求的项数("2 *(大小* 1.5 + 10)")。要手动控制此设置，可以使用"shard_size"参数来控制每个分片生成的候选项的数量。

一旦合并了所有结果，低频项就会成为最有趣的项，因此当"shard_size"参数设置为明显高于"大小"设置的值时，significant_terms聚合可以产生更高质量的结果。这可确保在最终选择之前，减少节点对大量有希望的候选术语进行合并审查。显然，大型候选术语列表会导致网络外流量和 RAM 使用，因此这是需要平衡的质量/成本权衡。如果"shard_size"设置为 -1(默认值)，则将根据分片数量和"size"参数自动估计"shard_size"。

"shard_size"不能小于"大小"(因为它没有多大意义)。当它是时，Elasticsearch将覆盖它并将其重置为等于"size"。

#### 最小文档数

可以使用"min_doc_count"选项仅返回匹配超过配置命中数的字词：

    
    
    response = client.search(
      body: {
        aggregations: {
          tags: {
            significant_terms: {
              field: 'tag',
              min_doc_count: 10
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "tags": {
          "significant_terms": {
            "field": "tag",
            "min_doc_count": 10
          }
        }
      }
    }

上述聚合只会返回在 10 次或更多点击中找到的标签。默认值为"3"。

得分高的术语将在分片级别收集，并在第二步中与从其他分片收集的术语合并。但是，分片没有有关可用全局术语频率的信息。是否将术语添加到候选列表的决定仅取决于使用本地分片频率在分片上计算的分数，而不是单词的全局频率。"min_doc_count"标准仅在合并所有分片的本地术语统计信息后应用。在某种程度上，将术语添加为候选人的决定是在没有非常_确定_该术语是否实际达到所需的"min_doc_count"的情况下做出的。如果候选人列表中填充了低频率但得分高的术语，这可能会导致最终结果中缺少许多(全局)高频率术语。为了避免这种情况，可以增加"shard_size"参数以允许分片上有更多的候选项。但是，这会增加内存消耗和网络流量。

####'shard_min_doc_count'

参数"shard_min_doc_count"规定了分片是否应该将该术语添加到候选列表中与"min_doc_count"相关的_确定性_。仅当术语在集合中的本地分片频率高于"shard_min_doc_count"时，才会考虑术语。如果您的字典包含许多低频率术语，并且您对这些术语不感兴趣(例如拼写错误)，那么您可以设置 'shard_min_doc_count' 参数以在分片级别过滤掉候选术语，即使在合并本地计数后，这些候选术语也不会达到所需的"min_doc_count"。默认情况下，"shard_min_doc_count"设置为"0"，除非您明确设置，否则无效。

通常不建议将"min_doc_count"设置为"1"，因为它往往会返回拼写错误或其他奇怪的好奇心。找到一个术语的多个实例有助于强化这一点，虽然仍然很少见，但该术语不是一次性事故的结果。默认值 3 用于提供最小证据权重。将"shard_min_doc_count"设置得太高将导致在分片级别过滤掉重要的候选术语。此值应设置为远低于"min_doc_count/#shards"。

#### 自定义背景上下文

背景术语频率的默认统计信息来源是整个索引，可以通过使用"background_filter"来缩小范围，以关注较窄上下文中的重要术语：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            city: 'madrid'
          }
        },
        aggregations: {
          tags: {
            significant_terms: {
              field: 'tag',
              background_filter: {
                term: {
                  text: 'spain'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match": {
          "city": "madrid"
        }
      },
      "aggs": {
        "tags": {
          "significant_terms": {
            "field": "tag",
            "background_filter": {
              "term": { "text": "spain" }
            }
          }
        }
      }
    }

上述过滤器将有助于关注马德里市特有的术语，而不是揭示像"西班牙语"这样的术语，这些术语在完整索引的全球背景下是不寻常的，但在包含"西班牙"一词的文件子集中却司空见惯。

使用后台过滤器会减慢查询速度，因为必须过滤每个术语的帖子以确定频率

#### 筛选值

可以(尽管很少需要)筛选将为其创建存储桶的值。这可以使用基于正则表达式字符串或精确术语数组的"include"和"exclude"参数来完成。此功能反映了术语聚合文档中描述的功能。

### 收集模式

为了避免内存问题，"significant_terms"聚合始终在"breadth_first"模式下计算子聚合。可以在术语聚合文档中找到不同集合模式的说明。

### 执行提示

可以通过不同的机制执行术语聚合：

* 直接使用字段值以聚合每个存储桶的数据("map") * 通过使用字段的全局序号并为每个全局序号分配一个存储桶 ("global_ordinals")

Elasticsearch尝试使用合理的默认值，因此通常不需要配置。

"global_ordinals"是"关键字"字段的默认选项，它使用全局序号动态分配存储桶，因此内存使用情况与属于聚合范围的文档的值数量成线性关系。

仅当很少有文档与查询匹配时，才应考虑"map"。否则，基于序数的执行模式会明显更快。默认情况下，"map"仅在脚本上运行聚合时使用，因为它们没有序号。

    
    
    response = client.search(
      body: {
        aggregations: {
          tags: {
            significant_terms: {
              field: 'tags',
              execution_hint: 'map'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "tags": {
          "significant_terms": {
            "field": "tags",
            "execution_hint": "map" __}
        }
      }
    }

__

|

可能的值为"map"、"global_ordinals"---|--- 请注意，如果此执行提示不适用，Elasticsearch 将忽略它。

[« Sampler aggregation](search-aggregations-bucket-sampler-aggregation.md)
[Significant text aggregation »](search-aggregations-bucket-significanttext-
aggregation.md)
