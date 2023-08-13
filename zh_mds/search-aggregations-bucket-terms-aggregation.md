

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Significant text aggregation](search-aggregations-bucket-significanttext-
aggregation.md) [Time series aggregation »](search-aggregations-bucket-time-
series-aggregation.md)

## 术语聚合

基于多存储桶值源的聚合，其中存储桶是动态构建的 - 每个唯一值一个。

Example:

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            terms: {
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
          "terms": { "field": "genre" }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "genres": {
          "doc_count_error_upper_bound": 0,   __"sum_other_doc_count": 0, __"buckets": [ __{
              "key": "electronic",
              "doc_count": 6
            },
            {
              "key": "rock",
              "doc_count": 3
            },
            {
              "key": "jazz",
              "doc_count": 2
            }
          ]
        }
      }
    }

__

|

文档错误上限为每个术语计数，请参见下面的 ---|--- __

|

当有很多唯一术语时，Elasticsearch 只返回排名靠前的术语;这个数字是不属于响应的所有存储桶的文档计数之和 __

|

顶级存储桶的列表，"top"的含义由顺序定义 "字段"可以是关键字、数字、"ip"、"布尔值"或"二进制"。

默认情况下，不能对"文本"字段运行"术语"聚合。请改用"关键字"子字段。或者，您可以在"文本"字段上启用"字段数据"，为字段的分析术语创建存储桶。启用"字段数据"可以显著增加内存使用量。

###Size

默认情况下，"terms"聚合返回文档最多的前十个术语。使用"size"参数返回更多术语，最高可达搜索.max_buckets限制。

如果数据包含 100 或 1000 个唯一字词，则可以增加"字词"聚合的"大小"以返回所有字词。如果您有更多唯一术语并且需要所有术语，请改用复合聚合。

较大的"size"值使用更多的内存进行计算，并将整个聚合推向接近"max_buckets"限制。如果请求失败并显示有关"max_buckets"的消息，您将知道您变得太大了。

### 分片大小

为了获得更准确的结果，"术语"agg 从每个分片中获取的比顶部"大小"术语更多。它获取顶部的"shard_size"项，默认为"大小 * 1.5 + 10"。

这是为了处理一个术语在一个分片上有许多文档，但刚好低于所有其他分片的"大小"阈值的情况。如果每个分片仅返回"大小"术语，则聚合将返回该术语的部分文档计数。因此，"terms"返回更多术语，以试图捕获缺失的术语。这很有帮助，但仍然很有可能返回一个学期的部分文档计数。它只需要一个术语，每个分片文档计数更不同。

您可以增加"shard_size"以更好地解释这些不同的文档计数，并提高选择热门术语的准确性。增加"shard_size"比增加"大小"便宜得多。但是，它仍然会通过线路占用更多字节，并在协调节点上的内存中等待。

仅当使用"术语"聚合的默认排序"顺序"时，本指南才适用。如果要按文档计数降序以外的任何内容进行排序，请参阅顺序。

"shard_size"不能小于"大小"(因为它没有多大意义)。当它是时，Elasticsearch将覆盖它并将其重置为等于"size"。

### 文档计数错误

即使具有较大的"shard_size"值，"术语"聚合的"doc_count"值也可能是近似值。因此，"术语"聚合上的任何子聚合也可能是近似的。

"sum_other_doc_count"是未进入最高"大小"术语的文档数量。如果此值大于"0"，则可以确定"terms"agg 必须丢弃一些存储桶，因为它们不适合协调节点上的"大小"，或者它们不适合数据节点上的"shard_size"。

### 每个存储桶文档计数错误

如果将"show_term_doc_count_error"参数设置为"true"，则"terms"聚合将包含"doc_count_error_upper_bound"，这是每个分片返回的"doc_count"错误的上限。它是每个分片上不适合"shard_size"的最大存储桶大小的总和。

更具体地说，假设有一个桶在 onehard 上非常大，而在所有其他分片的"shard_size"之外。在这种情况下，"terms" agg 将返回存储桶，因为它很大，但它会丢失来自分片上许多文档的数据，其中术语低于"shard_size"阈值。"doc_count_error_upper_bound"是丢失文档的最大数量。

    
    
    response = client.search(
      body: {
        aggregations: {
          products: {
            terms: {
              field: 'product',
              size: 5,
              show_term_doc_count_error: true
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "products": {
    	      "terms": {
    	        "field": "product",
    	        "size": 5,
    	        "show_term_doc_count_error": true
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "products": {
          "terms": {
            "field": "product",
            "size": 5,
            "show_term_doc_count_error": true
          }
        }
      }
    }

仅当按文档计数降序排序术语时，才能以这种方式计算这些错误。当聚合按术语值本身(升序或降序)排序时，文档计数中没有错误，因为如果分片没有返回出现在另一个分片的结果中的特定术语，则其索引中不得包含该术语。当聚合按子聚合或按升序文档计数排序时，无法确定文档计数中的错误，并被赋予值 -1 以指示这一点。

###Order

默认情况下，"条款"聚合按文档"_count"降序排列术语。这会产生一个有界的文档计数错误，Elasticsearch 可以报告该错误。

您可以使用"order"参数指定不同的排序顺序，但我们不建议这样做。创建只会返回错误结果的术语排序非常容易，并且当您这样做时并不明显。仅谨慎更改此设置。

特别是避免使用"订单"： { "_count"： "asc" }'。如果需要查找稀有术语，请改用"rare_terms"聚合。由于"术语"聚合从分片获取术语的方式，按文档计数升序排序通常会产生不准确的结果。

#### 按术语值排序

在这种情况下，存储桶按实际术语值排序，例如关键字的词典顺序或数字的数字顺序。这种排序在升序和降序方向上都是安全的，并产生准确的结果。

按术语的字母顺序以升序方式对存储桶进行排序的示例：

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            terms: {
              field: 'genre',
              order: {
                _key: 'asc'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "genres": {
    	      "terms": {
    	        "field": "genre",
    	        "order": {
    	          "_key": "asc"
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "terms": {
            "field": "genre",
            "order": { "_key": "asc" }
          }
        }
      }
    }

#### 按子聚合排序

按子聚合排序通常会产生不正确的排序，因为"术语"聚合从分片获取结果的方式。

在两种情况下，子聚合排序是安全的并返回正确的结果：按降序按最大值排序，或按最小升序排序。这些方法之所以有效，是因为它们与子聚合的行为一致。也就是说，如果您正在寻找最大最大值或最小值，则必须将全局答案(来自组合分片)包含在其中一个本地分片答案中。相反，不会准确计算最小最大值和最大最小值。

另请注意，在这些情况下，排序是正确的，但文档计数和非排序子聚合可能仍然存在错误(并且 Elasticsearch 不会计算这些错误的界限)。

按单值指标子聚合(由聚合名称标识)对存储桶进行排序：

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            terms: {
              field: 'genre',
              order: {
                max_play_count: 'desc'
              }
            },
            aggregations: {
              max_play_count: {
                max: {
                  field: 'play_count'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "genres": {
    	      "terms": {
    	        "field": "genre",
    	        "order": {
    	          "max_play_count": "desc"
    	        }
    	      },
    	      "aggs": {
    	        "max_play_count": {
    	          "max": {
    	            "field": "play_count"
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "terms": {
            "field": "genre",
            "order": { "max_play_count": "desc" }
          },
          "aggs": {
            "max_play_count": { "max": { "field": "play_count" } }
          }
        }
      }
    }

按多值指标子聚合(由聚合名称标识)对存储桶进行排序：

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            terms: {
              field: 'genre',
              order: {
                "playback_stats.max": 'desc'
              }
            },
            aggregations: {
              playback_stats: {
                stats: {
                  field: 'play_count'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "genres": {
    	      "terms": {
    	        "field": "genre",
    	        "order": {
    	          "playback_stats.max": "desc"
    	        }
    	      },
    	      "aggs": {
    	        "playback_stats": {
    	          "stats": {
    	            "field": "play_count"
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "terms": {
            "field": "genre",
            "order": { "playback_stats.max": "desc" }
          },
          "aggs": {
            "playback_stats": { "stats": { "field": "play_count" } }
          }
        }
      }
    }

### 管道 agggs 不能用于排序

管道聚合在所有其他聚合完成后的缩减阶段运行。因此，它们不能用于订购。

还可以根据层次结构中的"更深"聚合对存储桶进行排序。只要聚合路径为单存储桶类型，就支持此功能，其中路径中的最后一个聚合可以是单存储桶聚合，也可以是指标聚合。如果是单存储桶类型，则顺序将由存储桶中的文档数量(即"doc_count")定义，如果是指标类型，则应用与上述相同的规则(其中路径必须指示在多值指标聚合的情况下要排序的指标名称，如果是单值指标聚合，排序将应用于该值)。

路径必须按以下形式定义：

    
    
    AGG_SEPARATOR       =  '>' ;
    METRIC_SEPARATOR    =  '.' ;
    AGG_NAME            =  <the name of the aggregation> ;
    METRIC              =  <the name of the metric (in case of multi-value metrics aggregation)> ;
    PATH                =  <AGG_NAME> [ <AGG_SEPARATOR>, <AGG_NAME> ]* [ <METRIC_SEPARATOR>, <METRIC> ] ;
    
    
    response = client.search(
      body: {
        aggregations: {
          countries: {
            terms: {
              field: 'artist.country',
              order: {
                "rock>playback_stats.avg": 'desc'
              }
            },
            aggregations: {
              rock: {
                filter: {
                  term: {
                    genre: 'rock'
                  }
                },
                aggregations: {
                  playback_stats: {
                    stats: {
                      field: 'play_count'
                    }
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "countries": {
    	      "terms": {
    	        "field": "artist.country",
    	        "order": {
    	          "rock>playback_stats.avg": "desc"
    	        }
    	      },
    	      "aggs": {
    	        "rock": {
    	          "filter": {
    	            "term": {
    	              "genre": "rock"
    	            }
    	          },
    	          "aggs": {
    	            "playback_stats": {
    	              "stats": {
    	                "field": "play_count"
    	              }
    	            }
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "countries": {
          "terms": {
            "field": "artist.country",
            "order": { "rock>playback_stats.avg": "desc" }
          },
          "aggs": {
            "rock": {
              "filter": { "term": { "genre": "rock" } },
              "aggs": {
                "playback_stats": { "stats": { "field": "play_count" } }
              }
            }
          }
        }
      }
    }

以上将根据摇滚歌曲的平均播放次数对艺术家的国家/地区进行排序。

通过提供一系列排序条件，可以使用多个条件对存储桶进行排序，如下所示：

    
    
    response = client.search(
      body: {
        aggregations: {
          countries: {
            terms: {
              field: 'artist.country',
              order: [
                {
                  "rock>playback_stats.avg": 'desc'
                },
                {
                  _count: 'desc'
                }
              ]
            },
            aggregations: {
              rock: {
                filter: {
                  term: {
                    genre: 'rock'
                  }
                },
                aggregations: {
                  playback_stats: {
                    stats: {
                      field: 'play_count'
                    }
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "countries": {
    	      "terms": {
    	        "field": "artist.country",
    	        "order": [
    	          {
    	            "rock>playback_stats.avg": "desc"
    	          },
    	          {
    	            "_count": "desc"
    	          }
    	        ]
    	      },
    	      "aggs": {
    	        "rock": {
    	          "filter": {
    	            "term": {
    	              "genre": "rock"
    	            }
    	          },
    	          "aggs": {
    	            "playback_stats": {
    	              "stats": {
    	                "field": "play_count"
    	              }
    	            }
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "countries": {
          "terms": {
            "field": "artist.country",
            "order": [ { "rock>playback_stats.avg": "desc" }, { "_count": "desc" } ]
          },
          "aggs": {
            "rock": {
              "filter": { "term": { "genre": "rock" } },
              "aggs": {
                "playback_stats": { "stats": { "field": "play_count" } }
              }
            }
          }
        }
      }
    }

以上将根据摇滚歌曲的平均播放次数对艺术家的国家桶进行排序，然后按其"doc_count"降序排列。

如果两个存储桶的所有顺序标准共享相同的值，则存储桶的术语值将用作按字母升序排列的决胜局，以防止存储桶的非确定性排序。

#### 按计数升序排序

按文档升序"_count"对术语进行排序会产生一个无限错误，Elasticsearch 无法准确报告该错误。因此，我们强烈建议不要使用"订单"： { "_count"： "asc" }'，如以下示例所示：

    
    
    response = client.search(
      body: {
        aggregations: {
          genres: {
            terms: {
              field: 'genre',
              order: {
                _count: 'asc'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "genres": {
    	      "terms": {
    	        "field": "genre",
    	        "order": {
    	          "_count": "asc"
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "genres": {
          "terms": {
            "field": "genre",
            "order": { "_count": "asc" }
          }
        }
      }
    }

### 最小文档计数

可以使用"min_doc_count"选项仅返回匹配超过配置命中数的字词：

    
    
    response = client.search(
      body: {
        aggregations: {
          tags: {
            terms: {
              field: 'tags',
              min_doc_count: 10
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "tags": {
    	      "terms": {
    	        "field": "tags",
    	        "min_doc_count": 10
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "tags": {
          "terms": {
            "field": "tags",
            "min_doc_count": 10
          }
        }
      }
    }

上述聚合只会返回在 10 次或更多点击中找到的标签。默认值为"1"。

术语在分片级别收集和排序，并在第二步中与从其他分片收集的术语合并。但是，分片没有有关全局文档计数的可用信息。是否将 aterm 添加到候选列表的决定仅取决于使用本地分片频率在分片上计算的顺序。"min_doc_count"标准仅在合并所有分片的本地术语统计信息后应用。在某种程度上，将术语添加为候选人的决定是在没有非常_certain_about术语是否真的达到所需的"min_doc_count"的情况下做出的。这可能会导致许多(全局)高频率术语在最终结果中缺失 iflow 频繁术语填充候选列表。为了避免这种情况，可以增加"shard_size"参数以允许分片上有更多的候选项。但是，这会增加内存消耗和网络流量。

####'shard_min_doc_count'

参数"shard_min_doc_count"规定了分片是否应该将该术语添加到候选列表中与"min_doc_count"相关的_确定性_。仅当术语在集合中的本地分片频率高于"shard_min_doc_count"时，才会考虑术语。如果您的字典包含许多低频率术语，并且您对这些术语不感兴趣(例如拼写错误)，那么您可以设置 'shard_min_doc_count' 参数以在分片级别过滤掉候选术语，即使在合并本地计数后，这些候选术语也不会达到所需的"min_doc_count"。默认情况下，"shard_min_doc_count"设置为"0"，除非您明确设置，否则无效。

设置"min_doc_count"="0"也会返回与任何匹配项不匹配的字词的存储桶。但是，某些返回的文档计数为零的术语可能只属于已删除的文档或其他类型的文档，因此无法保证"match_all"查询会找到这些术语的正文档计数。

当不按"doc_count"降序排序时，高值"min_doc_count"可能会返回许多小于"大小"的存储桶，因为从分片中收集的数据不足。丢失的存储桶可以通过增加"shard_size"来恢复。将"shard_min_doc_count"设置得太高将导致在分片级别过滤掉术语。此值应设置为远低于"min_doc_count/#shards"。

###Script

如果文档中的数据与要聚合的数据不完全匹配，请使用运行时字段。例如，如果"选集"需要属于特殊类别，那么您可以运行以下命令：

    
    
    response = client.search(
      body: {
        size: 0,
        runtime_mappings: {
          normalized_genre: {
            type: 'keyword',
            script: "\n        String genre = doc['genre'].value;\n        if (doc['product'].value.startsWith('Anthology')) {\n          emit(genre + ' anthology');\n        } else {\n          emit(genre);\n        }\n      "
          }
        },
        aggregations: {
          genres: {
            terms: {
              field: 'normalized_genre'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "runtime_mappings": {
        "normalized_genre": {
          "type": "keyword",
          "script": """
            String genre = doc['genre'].value;
            if (doc['product'].value.startsWith('Anthology')) {
              emit(genre + ' anthology');
            } else {
              emit(genre);
            }
          """
        }
      },
      "aggs": {
        "genres": {
          "terms": {
            "field": "normalized_genre"
          }
        }
      }
    }

这将看起来像：

    
    
    {
      "aggregations": {
        "genres": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "electronic",
              "doc_count": 4
            },
            {
              "key": "rock",
              "doc_count": 3
            },
            {
              "key": "electronic anthology",
              "doc_count": 2
            },
            {
              "key": "jazz",
              "doc_count": 2
            }
          ]
        }
      },
      ...
    }

这有点慢，因为运行时字段必须访问两个字段而不是一个字段，并且因为有一些优化适用于非运行时"关键字"字段，我们必须放弃运行时"关键字"字段。如果您需要速度，可以索引"normalized_genre"字段。

### 筛选值

可以筛选将为其创建存储桶的值。这可以使用基于正则表达式字符串或精确值数组的"include"和"exclude"参数来完成。此外，"include"子句可以使用"分区"表达式进行筛选。

#### 使用正则表达式过滤值

    
    
    response = client.search(
      body: {
        aggregations: {
          tags: {
            terms: {
              field: 'tags',
              include: '.*sport.*',
              exclude: 'water_.*'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "tags": {
    	      "terms": {
    	        "field": "tags",
    	        "include": ".*sport.*",
    	        "exclude": "water_.*"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "tags": {
          "terms": {
            "field": "tags",
            "include": ".*sport.*",
            "exclude": "water_.*"
          }
        }
      }
    }

在上面的示例中，将为包含"sport"一词的所有标签创建存储桶，但以"water_"开头的标签除外(因此不会聚合标签"water_sports")。"include"正则表达式将确定"允许"聚合哪些值，而"排除"则确定不应聚合的值。当两者都被定义时，"排除"具有优先权，这意味着，首先评估"包含"，然后才评估"排除"。

语法与正则表达式查询相同。

#### 使用精确值筛选值

对于基于精确值的匹配，"include"和"exclude"参数可以简单地采用一个字符串数组，这些字符串表示在索引中找到的术语：

    
    
    response = client.search(
      body: {
        aggregations: {
          "JapaneseCars": {
            terms: {
              field: 'make',
              include: [
                'mazda',
                'honda'
              ]
            }
          },
          "ActiveCarManufacturers": {
            terms: {
              field: 'make',
              exclude: [
                'rover',
                'jensen'
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "JapaneseCars": {
    	      "terms": {
    	        "field": "make",
    	        "include": [
    	          "mazda",
    	          "honda"
    	        ]
    	      }
    	    },
    	    "ActiveCarManufacturers": {
    	      "terms": {
    	        "field": "make",
    	        "exclude": [
    	          "rover",
    	          "jensen"
    	        ]
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "JapaneseCars": {
          "terms": {
            "field": "make",
            "include": [ "mazda", "honda" ]
          }
        },
        "ActiveCarManufacturers": {
          "terms": {
            "field": "make",
            "exclude": [ "rover", "jensen" ]
          }
        }
      }
    }

#### 使用分区过滤值

有时，在单个请求/响应对中需要处理的唯一术语太多，因此将分析分解为多个请求可能很有用。这可以通过在查询时将字段的值分组到多个分区中并在每个请求中仅处理一个分区来实现。考虑此请求，该请求正在寻找最近未记录任何访问权限的帐户：

    
    
    $params = [
        'body' => [
            'size' => 0,
            'aggs' => [
                'expired_sessions' => [
                    'terms' => [
                        'field' => 'account_id',
                        'include' => [
                            'partition' => 0,
                            'num_partitions' => 20,
                        ],
                        'size' => 10000,
                        'order' => [
                            'last_access' => 'asc',
                        ],
                    ],
                    'aggs' => [
                        'last_access' => [
                            'max' => [
                                'field' => 'access_date',
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "size": 0,
            "aggs": {
                "expired_sessions": {
                    "terms": {
                        "field": "account_id",
                        "include": {"partition": 0, "num_partitions": 20},
                        "size": 10000,
                        "order": {"last_access": "asc"},
                    },
                    "aggs": {"last_access": {"max": {"field": "access_date"}}},
                }
            },
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          expired_sessions: {
            terms: {
              field: 'account_id',
              include: {
                partition: 0,
                num_partitions: 20
              },
              size: 10_000,
              order: {
                last_access: 'asc'
              }
            },
            aggregations: {
              last_access: {
                max: {
                  field: 'access_date'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "size": 0,
    	  "aggs": {
    	    "expired_sessions": {
    	      "terms": {
    	        "field": "account_id",
    	        "include": {
    	          "partition": 0,
    	          "num_partitions": 20
    	        },
    	        "size": 10000,
    	        "order": {
    	          "last_access": "asc"
    	        }
    	      },
    	      "aggs": {
    	        "last_access": {
    	          "max": {
    	            "field": "access_date"
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        size: 0,
        aggs: {
          expired_sessions: {
            terms: {
              field: 'account_id',
              include: {
                partition: 0,
                num_partitions: 20
              },
              size: 10000,
              order: {
                last_access: 'asc'
              }
            },
            aggs: {
              last_access: {
                max: {
                  field: 'access_date'
                }
              }
            }
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
       "size": 0,
       "aggs": {
          "expired_sessions": {
             "terms": {
                "field": "account_id",
                "include": {
                   "partition": 0,
                   "num_partitions": 20
                },
                "size": 10000,
                "order": {
                   "last_access": "asc"
                }
             },
             "aggs": {
                "last_access": {
                   "max": {
                      "field": "access_date"
                   }
                }
             }
          }
       }
    }

此请求正在查找客户帐户子集的最后记录访问日期，因为我们可能希望使一些长时间未见的客户帐户过期。"num_partitions"设置已请求将唯一account_ids均匀地组织到二十个分区(0 到 19)中。此请求中的"分区"设置筛选为仅在属于分区 0 consideraccount_ids。后续请求应要求分区 1 然后 2 等，以完成过期帐户分析。

请注意，返回结果数的"大小"设置需要与"num_partitions"相对应。对于此特定帐户过期示例，平衡"大小"和"num_partitions"值的过程如下：

1. 使用"基数"聚合估计唯一account_id值的总数 2.为"num_partitions"选择一个值，将数字从 1) 向上分解为更易于管理的块 3。为我们希望从每个分区 4 获得的响应数量选择一个"大小"值。运行测试请求

如果我们有一个断路器错误，我们试图在一个请求中做太多事情并且必须增加"num_partitions"。如果请求成功，但日期排序测试响应中的最后一个帐户 ID 仍然是我们可能想要过期的帐户，那么我们可能缺少感兴趣的帐户，并且将数字设置得太低。我们必须要么

* 增加"size"参数以返回每个分区的更多结果(可能会占用大量内存)或 * 增加"num_partitions"以考虑每个请求的帐户更少(可能会增加整体处理时间，因为我们需要发出更多请求)

最终，这是在管理处理单个请求所需的 Elasticsearchresources 和客户端应用程序完成任务必须发出的请求量之间的平衡行为。

分区不能与"排除"参数一起使用。

### 多字段术语聚合

"术语"聚合不支持从同一文档中的多个字段收集术语。原因是"terms"agg 本身不收集字符串术语值，而是使用全局序号来生成字段中所有唯一值的列表。全局序数可带来重要的性能提升，这在多个领域是不可能的。

您可以使用三种方法跨多个字段执行"术语"聚合：

脚本

     Use a script to retrieve terms from multiple fields. This disables the global ordinals optimization and will be slower than collecting terms from a single field, but it gives you the flexibility to implement this option at search time. 
[`copy_to` field](copy-to.html "copy_to")

     If you know ahead of time that you want to collect the terms from two or more fields, then use `copy_to` in your mapping to create a new dedicated field at index time which contains the values from both fields. You can aggregate on this single field, which will benefit from the global ordinals optimization. 
[`multi_terms` aggregation](search-aggregations-bucket-multi-terms-
aggregation.html "Multi Terms aggregation")

     Use multi_terms aggregation to combine terms from multiple fields into a compound key. This also disables the global ordinals and will be slower than collecting terms from a single field. It is faster but less flexible than using a script. 

### 收集模式

延迟子聚合的计算

对于具有许多唯一术语和少量所需结果的字段，在修剪顶级父级 aggs 之前延迟子聚合的计算可能更有效。通常，聚合树的所有分支都在一次深度优先传递中展开，然后才进行任何修剪。在某些情况下，这可能会非常浪费，并且可能会遇到内存限制。一个示例问题场景是在电影数据库中查询 10 位最受欢迎的演员及其 5 位最常见的联合主演：

    
    
    response = client.search(
      body: {
        aggregations: {
          actors: {
            terms: {
              field: 'actors',
              size: 10
            },
            aggregations: {
              costars: {
                terms: {
                  field: 'actors',
                  size: 5
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "actors": {
    	      "terms": {
    	        "field": "actors",
    	        "size": 10
    	      },
    	      "aggs": {
    	        "costars": {
    	          "terms": {
    	            "field": "actors",
    	            "size": 5
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "actors": {
          "terms": {
            "field": "actors",
            "size": 10
          },
          "aggs": {
            "costars": {
              "terms": {
                "field": "actors",
                "size": 5
              }
            }
          }
        }
      }
    }

尽管参与者的数量可能相对较小，并且我们只需要 50 个结果桶，但在计算过程中会出现桶的组合爆炸 - 单个参与者可以生成 n² 个桶，其中 n 是因子的数量。理智的选择是首先确定 10 位最受欢迎的演员，然后才检查这 10 位演员的顶级联合主演。这种替代策略就是我们所说的"breadth_first"收集模式，而不是"depth_first"模式。

"breadth_first"是基数大于请求大小或基数未知的字段(例如数字字段或脚本)的默认模式。可以覆盖默认的启发式方法，并直接在请求中提供收集模式：

    
    
    response = client.search(
      body: {
        aggregations: {
          actors: {
            terms: {
              field: 'actors',
              size: 10,
              collect_mode: 'breadth_first'
            },
            aggregations: {
              costars: {
                terms: {
                  field: 'actors',
                  size: 5
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "actors": {
    	      "terms": {
    	        "field": "actors",
    	        "size": 10,
    	        "collect_mode": "breadth_first"
    	      },
    	      "aggs": {
    	        "costars": {
    	          "terms": {
    	            "field": "actors",
    	            "size": 5
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "actors": {
          "terms": {
            "field": "actors",
            "size": 10,
            "collect_mode": "breadth_first" __},
          "aggs": {
            "costars": {
              "terms": {
                "field": "actors",
                "size": 5
              }
            }
          }
        }
      }
    }

__

|

可能的值是"breadth_first"和"depth_first"---|--- 使用"breadth_first"模式时，落入最上层存储桶的文档集将被缓存以供后续重放，因此执行此操作的内存开销与匹配文档的数量成线性关系。请注意，当使用"breadth_first"设置时，"order"参数仍可用于引用来自子聚合的数据 - 父聚合了解在任何其他子聚合之前需要首先调用此子聚合。

嵌套聚合(如"top_hits")需要使用"breadth_first"集合模式的聚合下访问 scoreinfo 需要在第二次传递时重播查询，但仅适用于属于顶级存储桶的文档。

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
            terms: {
              field: 'tags',
              execution_hint: 'map'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "tags": {
    	      "terms": {
    	        "field": "tags",
    	        "execution_hint": "map"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "tags": {
          "terms": {
            "field": "tags",
            "execution_hint": "map" __}
        }
      }
    }

__

|

可能的值是"map"、"global_ordinals"---|--- 请注意，如果此执行提示不适用，Elasticsearch 将忽略该执行提示，并且这些提示没有向后兼容性保证。

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      body: {
        aggregations: {
          tags: {
            terms: {
              field: 'tags',
              missing: 'N/A'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "tags": {
    	      "terms": {
    	        "field": "tags",
    	        "missing": "N/A"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "aggs": {
        "tags": {
          "terms": {
            "field": "tags",
            "missing": "N/A" __}
        }
      }
    }

__

|

"标签"字段中没有值的文档将属于与值为"N/A"的文档相同的存储桶。   ---|--- ### 混合字段类型编辑

聚合多个索引时，聚合字段的类型在所有索引中可能不同。某些类型彼此兼容("整数"和"长整型"或"浮点数"和"双精度数")，但是当类型是十进制数和非十进制数的混合时，术语聚合会将非十进制数提升为十进制数。这可能会导致存储桶值的精度损失。

####Troubleshooting

#### 尝试格式化字节失败

在多个索引上运行术语聚合(或其他聚合，但实际上通常是术语)时，您可能会收到以"尝试格式化字节失败...".这通常是由于两个索引对要聚合的字段没有相同的映射类型引起的。

**使用显式'value_type'** 尽管最好更正映射，但如果字段在其中一个索引中未映射，则可以解决此问题。设置"value_type"参数可以通过强制未映射字段为正确的类型来解决此问题。

    
    
    response = client.search(
      body: {
        aggregations: {
          ip_addresses: {
            terms: {
              field: 'destination_ip',
              missing: '0.0.0.0',
              value_type: 'ip'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "ip_addresses": {
          "terms": {
            "field": "destination_ip",
            "missing": "0.0.0.0",
            "value_type": "ip"
          }
        }
      }
    }

[« Significant text aggregation](search-aggregations-bucket-significanttext-
aggregation.md) [Time series aggregation »](search-aggregations-bucket-time-
series-aggregation.md)
