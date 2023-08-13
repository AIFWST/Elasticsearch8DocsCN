

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Auto-interval date histogram aggregation](search-aggregations-bucket-
autodatehistogram-aggregation.md) [Children aggregation »](search-
aggregations-bucket-children-aggregation.md)

## 对文本聚合进行分类

将半结构化文本分组到存储桶中的多存储桶聚合。每个"文本"字段都使用自定义分析器重新分析。然后对生成的令牌进行分类，创建具有类似格式的文本值的存储桶。此聚合最适合计算机生成的文本(如系统日志)。只有前 100 个分析的标记用于对文本进行分类。

如果为JVM分配了大量内存，但从此聚合中接收到断路器异常，则可能正在尝试对格式不正确的文本进行分类。考虑添加"categorization_filters"或在采样器、多样化采样器或随机采样器下运行，以探索创建的类别。

用于分类的算法在版本中已完全更改 8.3.0.As 因此此聚合在混合版本群集中不起作用，其中某些节点位于版本 8.3.0 或更高版本，而其他节点位于早于 8.3.0 的版本。如果遇到与此更改相关的错误，请将群集中的所有节点升级到同一版本。

###Parameters

`categorization_analyzer`

    

(可选、对象或字符串)分类分析器指定在对文本进行分类之前如何分析和标记文本。该语法与用于在 Analyzeendpoint 中定义"分析器"的语法非常相似。此属性不能与"categorization_filters"同时使用。

"categorization_analyzer"字段可以指定为字符串或 asan 对象。如果它是一个字符串，它必须引用内置分析器或另一个插件添加的分析器。如果它是一个对象，则它具有以下属性：

"categorization_analyzer"的属性

`char_filter`

     (array of strings or objects) One or more [character filters](analysis-charfilters.html "Character filters reference"). In addition to the built-in character filters, other plugins can provide more character filters. This property is optional. If it is not specified, no character filters are applied prior to categorization. If you are customizing some other aspect of the analyzer and you need to achieve the equivalent of `categorization_filters` (which are not permitted when some other aspect of the analyzer is customized), add them here as [pattern replace character filters](analysis-pattern-replace-charfilter.html "Pattern replace character filter"). 
`tokenizer`

     (string or object) The name or definition of the [tokenizer](analysis-tokenizers.html "Tokenizer reference") to use after character filters are applied. This property is compulsory if `categorization_analyzer` is specified as an object. Machine learning provides a tokenizer called `ml_standard` that tokenizes in a way that has been determined to produce good categorization results on a variety of log file formats for logs in English. If you want to use that tokenizer but change the character or token filters, specify `"tokenizer": "ml_standard"` in your `categorization_analyzer`. Additionally, the `ml_classic` tokenizer is available, which tokenizes in the same way as the non-customizable tokenizer in old versions of the product (before 6.2). `ml_classic` was the default categorization tokenizer in versions 6.2 to 7.13, so if you need categorization identical to the default for jobs created in these versions, specify `"tokenizer": "ml_classic"` in your `categorization_analyzer`. 
`filter`

     (array of strings or objects) One or more [token filters](analysis-tokenfilters.html "Token filter reference"). In addition to the built-in token filters, other plugins can provide more token filters. This property is optional. If it is not specified, no token filters are applied prior to categorization. 

`categorization_filters`

     (Optional, array of strings) This property expects an array of regular expressions. The expressions are used to filter out matching sequences from the categorization field values. You can use this functionality to fine tune the categorization by excluding sequences from consideration when categories are defined. For example, you can exclude SQL statements that appear in your log files. This property cannot be used at the same time as `categorization_analyzer`. If you only want to define simple regular expression filters that are applied prior to tokenization, setting this property is the easiest method. If you also want to customize the tokenizer or post-tokenization filtering, use the `categorization_analyzer` property instead and include the filters as `pattern_replace` character filters. 
`field`

     (Required, string) The semi-structured text field to categorize. 
`max_matched_tokens`

     (Optional, integer) This parameter does nothing now, but is permitted for compatibility with the original pre-8.3.0 implementation. 
`max_unique_tokens`

     (Optional, integer) This parameter does nothing now, but is permitted for compatibility with the original pre-8.3.0 implementation. 
`min_doc_count`

     (Optional, integer) The minimum number of documents for a bucket to be returned to the results. 
`shard_min_doc_count`

     (Optional, integer) The minimum number of documents for a bucket to be returned from the shard before merging. 
`shard_size`

     (Optional, integer) The number of categorization buckets to return from each shard before merging all the results. 
`similarity_threshold`

     (Optional, integer, default: `70`) The minimum percentage of token weight that must match for text to be added to the category bucket. Must be between 1 and 100. The larger the value the narrower the categories. Larger values will increase memory usage and create narrower categories. 
`size`

     (Optional, integer, default: `10`) The number of buckets to return. 

### 响应正文

`key`

     (string) Consists of the tokens (extracted by the `categorization_analyzer`) that are common to all values of the input field included in the category. 
`doc_count`

     (integer) Number of documents matching the category. 
`max_matching_length`

     (integer) Categories from short messages containing few tokens may also match categories containing many tokens derived from much longer messages. `max_matching_length` is an indication of the maximum length of messages that should be considered to belong to the category. When searching for messages that match the category, any messages longer than `max_matching_length` should be excluded. Use this field to prevent a search for members of a category of short messages from matching much longer ones. 
`regex`

     (string) A regular expression that will match all values of the input field included in the category. It is possible that the `regex` does not incorporate every term in `key`, if ordering varies between the values included in the category. However, in simple cases the `regex` will be the ordered terms concatenated into a regular expression that allows for arbitrary sections in between them. It is not recommended to use the `regex` as the primary mechanism for searching for the original documents that were categorized. Search using a regular expression is very slow. Instead the terms in the `key` field should be used to search for matching documents, as a terms search can use the inverted index and hence be much faster. However, there may be situations where it is useful to use the `regex` field to test whether a small set of messages that have not been indexed match the category, or to confirm that the terms in the `key` occur in the correct order in all the matched documents. 

### 基本使用

重新分析 _large_ 结果集将需要大量的时间和内存。此聚合应与异步搜索结合使用。此外，您可以考虑将聚合用作采样器或多样化采样器聚合的子级。这通常会提高速度和内存使用。

Example:

    
    
    POST log-messages/_search?filter_path=aggregations
    {
      "aggs": {
        "categories": {
          "categorize_text": {
            "field": "message"
          }
        }
      }
    }

Response:

    
    
    {
      "aggregations" : {
        "categories" : {
          "buckets" : [
            {
              "doc_count" : 3,
              "key" : "Node shutting down",
              "regex" : ".*?Node.+?shutting.+?down.*?",
              "max_matching_length" : 49
            },
            {
              "doc_count" : 1,
              "key" : "Node starting up",
              "regex" : ".*?Node.+?starting.+?up.*?",
              "max_matching_length" : 47
            },
            {
              "doc_count" : 1,
              "key" : "User foo_325 logging on",
              "regex" : ".*?User.+?foo_325.+?logging.+?on.*?",
              "max_matching_length" : 52
            },
            {
              "doc_count" : 1,
              "key" : "User foo_864 logged off",
              "regex" : ".*?User.+?foo_864.+?logged.+?off.*?",
              "max_matching_length" : 52
            }
          ]
        }
      }
    }

下面是一个使用"categorization_filters"的示例

    
    
    POST log-messages/_search?filter_path=aggregations
    {
      "aggs": {
        "categories": {
          "categorize_text": {
            "field": "message",
            "categorization_filters": ["\\w+\\_\\d{3}"] __}
        }
      }
    }

__

|

要应用于分析令牌的筛选器。它会过滤掉像"bar_123"这样的令牌。   ---|--- 请注意"foo_<number>"标记如何不是类别结果的一部分

    
    
    {
      "aggregations" : {
        "categories" : {
          "buckets" : [
            {
              "doc_count" : 3,
              "key" : "Node shutting down",
              "regex" : ".*?Node.+?shutting.+?down.*?",
              "max_matching_length" : 49
            },
            {
              "doc_count" : 1,
              "key" : "Node starting up",
              "regex" : ".*?Node.+?starting.+?up.*?",
              "max_matching_length" : 47
            },
            {
              "doc_count" : 1,
              "key" : "User logged off",
              "regex" : ".*?User.+?logged.+?off.*?",
              "max_matching_length" : 52
            },
            {
              "doc_count" : 1,
              "key" : "User logging on",
              "regex" : ".*?User.+?logging.+?on.*?",
              "max_matching_length" : 52
            }
          ]
        }
      }
    }

下面是使用"categorization_filters"的示例。默认分析器使用"ml_standard"分词器，类似于空格分词器，但过滤掉可能被解释为十六进制数的标记。默认分析器还使用"first_line_with_letters"字符筛选器，因此仅考虑多行消息的第一行有意义的行。但是，令牌可能是已知的高度可变令牌(格式化的用户名，电子邮件等)。在这种情况下，最好提供自定义"categorization_filters"以过滤掉这些令牌以获得更好的类别。这些筛选器还可以减少内存使用量，因为类别的内存中保存的令牌较少。(如果有足够的不同用户名，电子邮件等示例，那么将形成类别，自然地将它们丢弃为变量，但对于仅存在一个示例的小型输入数据，则不会发生这种情况。

    
    
    POST log-messages/_search?filter_path=aggregations
    {
      "aggs": {
        "categories": {
          "categorize_text": {
            "field": "message",
            "categorization_filters": ["\\w+\\_\\d{3}"], __"similarity_threshold": 11 __}
        }
      }
    }

__

|

要应用于分析令牌的筛选器。它会过滤掉像"bar_123"这样的令牌。   ---|---    __

|

在将消息添加到现有类别而不是创建新类别之前，需要匹配 11% 的令牌权重。   生成的类别现在非常广泛，合并了日志组。(11%的A'similarity_threshold'通常太低。超过 50% 的设置通常更好。

    
    
    {
      "aggregations" : {
        "categories" : {
          "buckets" : [
            {
              "doc_count" : 4,
              "key" : "Node",
              "regex" : ".*?Node.*?",
              "max_matching_length" : 49
            },
            {
              "doc_count" : 2,
              "key" : "User",
              "regex" : ".*?User.*?",
              "max_matching_length" : 52
            }
          ]
        }
      }
    }

此聚合可以同时具有子聚合，并且其本身是子聚合。这允许收集顶级每日类别和顶级示例文档，如下所示。

    
    
    POST log-messages/_search?filter_path=aggregations
    {
      "aggs": {
        "daily": {
          "date_histogram": {
            "field": "time",
            "fixed_interval": "1d"
          },
          "aggs": {
            "categories": {
              "categorize_text": {
                "field": "message",
                "categorization_filters": ["\\w+\\_\\d{3}"]
              },
              "aggs": {
                "hit": {
                  "top_hits": {
                    "size": 1,
                    "sort": ["time"],
                    "_source": "message"
                  }
                }
              }
            }
          }
        }
      }
    }
    
    
    {
      "aggregations" : {
        "daily" : {
          "buckets" : [
            {
              "key_as_string" : "2016-02-07T00:00:00.000Z",
              "key" : 1454803200000,
              "doc_count" : 3,
              "categories" : {
                "buckets" : [
                  {
                    "doc_count" : 2,
                    "key" : "Node shutting down",
                    "regex" : ".*?Node.+?shutting.+?down.*?",
                    "max_matching_length" : 49,
                    "hit" : {
                      "hits" : {
                        "total" : {
                          "value" : 2,
                          "relation" : "eq"
                        },
                        "max_score" : null,
                        "hits" : [
                          {
                            "_index" : "log-messages",
                            "_id" : "1",
                            "_score" : null,
                            "_source" : {
                              "message" : "2016-02-07T00:00:00+0000 Node 3 shutting down"
                            },
                            "sort" : [
                              1454803260000
                            ]
                          }
                        ]
                      }
                    }
                  },
                  {
                    "doc_count" : 1,
                    "key" : "Node starting up",
                    "regex" : ".*?Node.+?starting.+?up.*?",
                    "max_matching_length" : 47,
                    "hit" : {
                      "hits" : {
                        "total" : {
                          "value" : 1,
                          "relation" : "eq"
                        },
                        "max_score" : null,
                        "hits" : [
                          {
                            "_index" : "log-messages",
                            "_id" : "2",
                            "_score" : null,
                            "_source" : {
                              "message" : "2016-02-07T00:00:00+0000 Node 5 starting up"
                            },
                            "sort" : [
                              1454803320000
                            ]
                          }
                        ]
                      }
                    }
                  }
                ]
              }
            },
            {
              "key_as_string" : "2016-02-08T00:00:00.000Z",
              "key" : 1454889600000,
              "doc_count" : 3,
              "categories" : {
                "buckets" : [
                  {
                    "doc_count" : 1,
                    "key" : "Node shutting down",
                    "regex" : ".*?Node.+?shutting.+?down.*?",
                    "max_matching_length" : 49,
                    "hit" : {
                      "hits" : {
                        "total" : {
                          "value" : 1,
                          "relation" : "eq"
                        },
                        "max_score" : null,
                        "hits" : [
                          {
                            "_index" : "log-messages",
                            "_id" : "4",
                            "_score" : null,
                            "_source" : {
                              "message" : "2016-02-08T00:00:00+0000 Node 5 shutting down"
                            },
                            "sort" : [
                              1454889660000
                            ]
                          }
                        ]
                      }
                    }
                  },
                  {
                    "doc_count" : 1,
                    "key" : "User logged off",
                    "regex" : ".*?User.+?logged.+?off.*?",
                    "max_matching_length" : 52,
                    "hit" : {
                      "hits" : {
                        "total" : {
                          "value" : 1,
                          "relation" : "eq"
                        },
                        "max_score" : null,
                        "hits" : [
                          {
                            "_index" : "log-messages",
                            "_id" : "6",
                            "_score" : null,
                            "_source" : {
                              "message" : "2016-02-08T00:00:00+0000 User foo_864 logged off"
                            },
                            "sort" : [
                              1454889840000
                            ]
                          }
                        ]
                      }
                    }
                  },
                  {
                    "doc_count" : 1,
                    "key" : "User logging on",
                    "regex" : ".*?User.+?logging.+?on.*?",
                    "max_matching_length" : 52,
                    "hit" : {
                      "hits" : {
                        "total" : {
                          "value" : 1,
                          "relation" : "eq"
                        },
                        "max_score" : null,
                        "hits" : [
                          {
                            "_index" : "log-messages",
                            "_id" : "5",
                            "_score" : null,
                            "_source" : {
                              "message" : "2016-02-08T00:00:00+0000 User foo_325 logging on"
                            },
                            "sort" : [
                              1454889720000
                            ]
                          }
                        ]
                      }
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    }

[« Auto-interval date histogram aggregation](search-aggregations-bucket-
autodatehistogram-aggregation.md) [Children aggregation »](search-
aggregations-bucket-children-aggregation.md)
