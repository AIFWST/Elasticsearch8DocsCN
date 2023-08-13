

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Search shards API](search-shards.md) [Multi search API »](search-multi-
search.md)

##Suggesters

使用建议器根据提供的文本建议外观相似的术语。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            message: 'tring out Elasticsearch'
          }
        },
        suggest: {
          "my-suggestion": {
            text: 'tring out Elasticsearch',
            term: {
              field: 'message'
            }
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_search
    {
      "query" : {
        "match": {
          "message": "tring out Elasticsearch"
        }
      },
      "suggest" : {
        "my-suggestion" : {
          "text" : "tring out Elasticsearch",
          "term" : {
            "field" : "message"
          }
        }
      }
    }

###Request

建议功能使用建议器根据提供的文本建议外观相似的术语。建议请求部分与"_search"请求中的查询部分一起定义。如果省略查询部分，则仅返回建议。

###Examples

每个请求可以指定多个建议。每个建议都用任意名称标识。在下面的示例中，请求了两个建议。"my-suggest-1"和"my-suggest-2"建议都使用"术语"建议器，但具有不同的"文本"。

    
    
    response = client.search(
      body: {
        suggest: {
          "my-suggest-1": {
            text: 'tring out Elasticsearch',
            term: {
              field: 'message'
            }
          },
          "my-suggest-2": {
            text: 'kmichy',
            term: {
              field: 'user.id'
            }
          }
        }
      }
    )
    puts response
    
    
    POST _search
    {
      "suggest": {
        "my-suggest-1" : {
          "text" : "tring out Elasticsearch",
          "term" : {
            "field" : "message"
          }
        },
        "my-suggest-2" : {
          "text" : "kmichy",
          "term" : {
            "field" : "user.id"
          }
        }
      }
    }

下面的建议响应示例包括"my-suggest-1"和"my-suggest-2"的建议响应。每个建议部分都包含条目。每个条目实际上是来自建议文本的标记，并包含建议条目文本、建议文本中的原始开始偏移量和长度，如果找到任意数量的选项。

    
    
    {
      "_shards": ...
      "hits": ...
      "took": 2,
      "timed_out": false,
      "suggest": {
        "my-suggest-1": [ {
          "text": "tring",
          "offset": 0,
          "length": 5,
          "options": [ {"text": "trying", "score": 0.8, "freq": 1 } ]
        }, {
          "text": "out",
          "offset": 6,
          "length": 3,
          "options": []
        }, {
          "text": "elasticsearch",
          "offset": 10,
          "length": 13,
          "options": []
        } ],
        "my-suggest-2": ...
      }
    }

每个选项数组都包含一个选项对象，该对象包括建议的文本，其文档频率以及与建议条目文本相比的分数。分数的含义取决于所使用的建议器。术语建议者的分数基于编辑距离。

##### 全局建议文本

为了避免建议文本的重复，可以定义全局文本。在下面的示例中，建议文本是全局定义的，适用于"my-suggest-1"和"my-suggest-2"建议。

    
    
    $params = [
        'body' => [
            'suggest' => [
                'text' => 'tring out Elasticsearch',
                'my-suggest-1' => [
                    'term' => [
                        'field' => 'message',
                    ],
                ],
                'my-suggest-2' => [
                    'term' => [
                        'field' => 'user',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "suggest": {
                "text": "tring out Elasticsearch",
                "my-suggest-1": {"term": {"field": "message"}},
                "my-suggest-2": {"term": {"field": "user"}},
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        suggest: {
          text: 'tring out Elasticsearch',
          "my-suggest-1": {
            term: {
              field: 'message'
            }
          },
          "my-suggest-2": {
            term: {
              field: 'user'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "suggest": {
    	    "text": "tring out Elasticsearch",
    	    "my-suggest-1": {
    	      "term": {
    	        "field": "message"
    	      }
    	    },
    	    "my-suggest-2": {
    	      "term": {
    	        "field": "user"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        suggest: {
          text: 'tring out Elasticsearch',
          'my-suggest-1': {
            term: {
              field: 'message'
            }
          },
          'my-suggest-2': {
            term: {
              field: 'user'
            }
          }
        }
      }
    })
    console.log(response)
    
    
    POST _search
    {
      "suggest": {
        "text" : "tring out Elasticsearch",
        "my-suggest-1" : {
          "term" : {
            "field" : "message"
          }
        },
        "my-suggest-2" : {
           "term" : {
            "field" : "user"
           }
        }
      }
    }

在上面的示例中，建议文本也可以指定为特定于建议的选项。在建议级别指定的建议文本将覆盖全局级别的建议文本。

### 术语建议器

"术语"建议器根据编辑距离建议术语。在建议术语之前，将分析提供的建议文本。建议的术语是每个分析的建议文本令牌提供的。"术语"建议器不会考虑作为请求一部分的查询。

#### 常见建议选项：

`text`

|

建议文本。建议文本是必需选项，需要全局设置或按建议设置。   ---|---"字段"

|

要从中获取候选建议的字段。这是必需的选项，需要全局设置或按建议设置。   "分析器"

|

用于分析建议文本的分析器。默认为建议字段的搜索分析器。   "大小"

|

每个建议文本标记返回的最大更正数。   "排序"

|

定义应如何按建议文本术语对建议进行排序。两个可能的值：

* "分数"：首先按分数排序，然后记录频率，然后是术语本身。  * "频率"：首先按文档频率排序，然后按相似性得分，然后按术语本身排序。

"suggest_mode"

|

建议模式控制包含哪些建议或控制应建议的文本术语。可以指定三个可能的值：

* "缺失"：仅针对不在索引中的建议文本术语提供建议(默认)。  * "热门"：仅建议出现在比原始建议文本术语更多的文档中的建议。  * "始终"：根据建议文本中的字词建议任何匹配的建议。

#### 其他术语建议选项：编辑

`max_edits`

|

候选建议可以具有的最大编辑距离，以便被视为建议。只能是介于 1 和 2 之间的值。任何其他值都会导致引发错误的请求错误。默认值为 2。   ---|--- "prefix_length"

|

必须匹配的最小前缀字符数，以便成为建议的候选字符。默认值为 1。增加此数字可提高拼写检查性能。通常拼写错误不会出现在术语的开头。   "min_word_length"

|

建议文本术语必须具有的最小长度才能包含在内。默认为"4"。   "shard_size"

|

设置要从每个人检索的最大建议数。在缩减阶段，仅根据"大小"选项返回前 N 个建议。默认为"大小"选项。将其设置为高于"size"的值可能很有用，以便以牺牲性能为代价获得更准确的拼写更正文档频率。由于术语在分片之间划分，因此拼写更正的分片级别文档频率可能不精确。增加此值将使这些文档频率更加精确。   "max_inspections"

|

用于与"shard_size"相乘以在分片级别检查更多候选拼写更正的因子。可以以性能为代价提高准确性。默认值为 5。   "min_doc_freq"

|

建议应出现在的文档数的最小阈值。这可以指定为绝对数或文档数的相对百分比。这可以通过仅建议高频术语来提高质量。默认为 0f 且未启用。如果指定了大于 1 的值，则该数字不能是小数。分片级文档频率用于此选项。   "max_term_freq"

|

建议文本标记可以存在以包含的文档数的最大阈值。可以是相对百分比数(例如，0.4)或绝对数来表示文档频率。如果指定的值大于 1，则不能指定小数。默认值为 0.01f。这可用于排除高频术语(通常拼写正确)的拼写检查。这也提高了拼写检查性能。分片级文档频率用于此选项。   "string_distance"

|

使用哪种字符串距离实现来比较建议术语的相似程度。可以指定五个可能的值：

* "internal"：基于damerau_levenshtein的默认值，但经过高度优化，用于比较索引内术语的字符串距离。  * 'damerau_levenshtein'：基于Damerau-Levenshtein算法的字符串距离算法。  * 'levenshtein'：基于Levenshtein编辑距离算法的字符串距离算法。  * 'jaro_winkler'：基于Jaro-Winkler算法的字符串距离算法。  * 'ngram'：基于字符 n-gram 的字符串距离算法。

### 短语建议器编辑

"term"建议器提供了一个非常方便的API，可以在一定的字符串距离内按令牌访问单词替代品。API 允许单独访问流中的每个令牌，而建议选择留给 API 使用者。然而，为了向最终用户展示，通常需要预先选择的建议。"短语"建议器在"术语"建议器之上添加额外的逻辑，以选择整个更正的短语，而不是基于"ngram语言"模型加权的单个标记。在实践中，这个建议器将能够根据共现和频率更好地决定选择哪些代币。

#### APIExample

通常，"短语"建议器需要预先进行特殊映射才能工作。此页面上的"短语"建议器示例需要以下映射才能工作。"反向"分析器仅在最后一个示例中使用。

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        settings: {
          index: {
            number_of_shards: 1,
            analysis: {
              analyzer: {
                trigram: {
                  type: 'custom',
                  tokenizer: 'standard',
                  filter: [
                    'lowercase',
                    'shingle'
                  ]
                },
                reverse: {
                  type: 'custom',
                  tokenizer: 'standard',
                  filter: [
                    'lowercase',
                    'reverse'
                  ]
                }
              },
              filter: {
                shingle: {
                  type: 'shingle',
                  min_shingle_size: 2,
                  max_shingle_size: 3
                }
              }
            }
          }
        },
        mappings: {
          properties: {
            title: {
              type: 'text',
              fields: {
                trigram: {
                  type: 'text',
                  analyzer: 'trigram'
                },
                reverse: {
                  type: 'text',
                  analyzer: 'reverse'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      refresh: true,
      body: {
        title: 'noble warriors'
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      refresh: true,
      body: {
        title: 'nobel prize'
      }
    )
    puts response
    
    
    PUT test
    {
      "settings": {
        "index": {
          "number_of_shards": 1,
          "analysis": {
            "analyzer": {
              "trigram": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase","shingle"]
              },
              "reverse": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase","reverse"]
              }
            },
            "filter": {
              "shingle": {
                "type": "shingle",
                "min_shingle_size": 2,
                "max_shingle_size": 3
              }
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "fields": {
              "trigram": {
                "type": "text",
                "analyzer": "trigram"
              },
              "reverse": {
                "type": "text",
                "analyzer": "reverse"
              }
            }
          }
        }
      }
    }
    POST test/_doc?refresh=true
    {"title": "noble warriors"}
    POST test/_doc?refresh=true
    {"title": "nobel prize"}

设置分析器和映射后，您可以在使用"术语"建议器的同一位置使用"短语"建议器：

    
    
    POST test/_search
    {
      "suggest": {
        "text": "noble prize",
        "simple_phrase": {
          "phrase": {
            "field": "title.trigram",
            "size": 1,
            "gram_size": 3,
            "direct_generator": [ {
              "field": "title.trigram",
              "suggest_mode": "always"
            } ],
            "highlight": {
              "pre_tag": "<em>",
              "post_tag": "</em>"
            }
          }
        }
      }
    }

响应包含按最可能的拼写更正首先评分的建议。在这种情况下，我们收到了预期的更正"诺贝尔奖"。

    
    
    {
      "_shards": ...
      "hits": ...
      "timed_out": false,
      "took": 3,
      "suggest": {
        "simple_phrase" : [
          {
            "text" : "noble prize",
            "offset" : 0,
            "length" : 11,
            "options" : [ {
              "text" : "nobel prize",
              "highlighted": "<em>nobel</em> prize",
              "score" : 0.48614594
            }]
          }
        ]
      }
    }

#### 基本短语建议 API 参数

`field`

|

用于对语言模型进行 n-gram 查找的字段的名称，建议器将使用此字段来获取统计信息以进行评分更正。此字段是必填字段。   ---|--- "gram_size"

|

设置"字段"中 n 元语法(带状疱疹)的最大大小。如果该字段不包含 n-gram(带状疱疹)，则应省略或将其设置为"1"。请注意，Elasticsearch 会尝试根据指定的"字段"检测克大小。如果字段使用"瓦片"过滤器，则"gram_size"设置为"max_shingle_size"(如果未明确设置)。   "real_word_error_likelihood"

|

即使词典中存在术语，术语拼写错误的可能性。默认值为"0.95"，表示 5% 的真实单词拼写错误。   "信心"

|

置信水平定义了应用于输入短语分数的因子，该因子用作其他建议候选项的阈值。只有分数高于阈值的候选人才会包含在结果中。例如，置信度为"1.0"只会返回得分高于输入短语的建议。如果设置为"0.0"，则返回前 N 个候选项。默认值为"1.0"。   "max_errors"

|

为了形成更正而被视为拼写错误的术语的最大百分比。此方法接受范围"[0..1)"中的浮点值作为实际查询词的分数或数字">=1"作为查询词的绝对数。默认值设置为"1.0"，这意味着仅返回最多一个拼写错误的术语的更正。请注意，设置得太高可能会对性能产生负面影响。建议使用较低的值(如"1"或"2")，否则建议调用所花费的时间可能会超过查询执行所花费的时间。   "分隔符"

|

用于分隔双字母字段中的术语的分隔符。如果未设置空格字符用作分隔符。   "大小"

|

为每个查询词生成的候选项数。像"3"或"5"这样的小数字通常会产生良好的结果。提高此值可以调出具有更高编辑距离的术语。默认值为"5"。   "分析器"

|

设置分析器以分析以建议文本。默认为通过"字段"传递的建议字段的搜索分析器。   "shard_size"

|

设置要从每个分片检索的建议术语的最大数量。在缩减阶段，仅根据"大小"选项返回前 N 个建议。默认为"5"。   "文本"

|

设置要为其提供建议的文本/查询。   "亮点"

|

设置建议突出显示。如果未提供，则不返回"突出显示"字段。如果提供，则必须包含"pre_tag"和"post_tag"，它们包裹在更改的令牌周围。如果更改了一行中的多个标记，则包装更改的令牌的整个短语，而不是每个标记。   "整理"

|

根据指定的"查询"检查每个建议，以修剪索引中不存在匹配文档的建议。建议的排序查询仅在从中生成建议的本地分片上运行。必须指定"查询"，并且可以对其进行模板化。请参阅_搜索模板_。当前建议自动作为"{{suggestion}}"变量提供，应在查询中使用。您仍然可以指定自己的模板"参数" - "建议"值将添加到您指定的变量中。此外，您可以指定"修剪"来控制是否返回所有短语建议;当设置为"true"时，建议将有一个附加选项"collate_match"，如果找到短语的匹配文档，则该选项将为"true"，否则为"false"。"修剪"的默认值为"假"。               开机自检测试/_search { "建议"： { "文本" ： "诺贝尔奖"， "simple_phrase" ： { "短语" ： { "字段" ： "title.trigram"， "size" ： 1， "direct_generator" ： [ { "field" ： "title.trigram"， "suggest_mode" ： "always"， "min_word_length" ： 1 } ]， "collate"： { "query"： { __"source" ： { "match"： { "{{field_name}}" ： "{{suggestion}}" __} } }， "params"： {"field_name" ： "title"}， __"prune"： true __} } } }

__

|

对于每个建议，将运行一次此查询。   ---|---    __

|

"{{建议}}"变量将被每个建议的文本替换。   __

|

在"参数"中指定了一个额外的"field_name"变量，并由"match"查询使用。   __

|

所有建议都将返回一个额外的"collate_match"选项，指示生成的短语是否与任何文档匹配。   #### 平滑模型编辑

"短语"建议器支持多个平滑模型，以平衡不常见克(索引中不存在克(带状疱疹))和频繁克(在索引中至少出现一次)之间的权重。可以通过将"平滑"参数设置为以下选项之一来选择平滑模型。每个平滑模型都支持可配置的特定属性。

`stupid_backoff`

|

一个简单的退避模型，如果较高的阶数为"0"，则回退到低阶 n-gram 模型，并通过恒定因子对低阶 n-gram 模型进行折扣。默认"折扣"为"0.4"。愚蠢的退避是默认模型。   ---|---"拉普拉斯"

|

一种使用加性平滑的平滑模型，其中将常量(通常为"1.0"或更小)添加到所有计数中以平衡权重。默认的"alpha"为"0.5"。   "linear_interpolation"

|

一种平滑模型，它根据用户提供的权重 (lambda) 获取单元组、双元组和三元组的加权平均值。线性插值没有任何默认值。必须提供所有参数("trigram_lambda"、"bigram_lambda"、"unigram_lambda")。               开机自检测试/_search { "建议"： { "文本" ： "奥贝尔奖"， "simple_phrase" ： { "短语" ： { "字段" ： "title.trigram"， "大小" ： 1， "平滑" ： { "laplace" ： { "alpha" ： 0.7 } } } } } }

#### 候选生成器

"短语"建议器使用候选生成器生成给定文本中每个术语的可能术语列表。单个候选生成器类似于为文本中的每个单独术语调用的"术语"建议器。随后，生成器的输出与其他术语的候选者一起评分，以供建议候选人使用。

目前仅支持一种类型的候选生成器，即"direct_generator"。短语建议 API 接受键"direct_generator"下的生成器列表;列表中的每个生成器在原始文本中称为 perterm。

#### 直接生成器

直接生成器支持以下参数：

`field`

|

要从中获取候选建议的字段。这是必需的选项，需要全局设置或按建议设置。   ---|---"大小"

|

每个建议文本标记返回的最大更正数。   "suggest_mode"

|

建议模式控制在每个分片上生成的建议中包含哪些建议。除"always"以外的所有值都可以视为优化，以生成更少的建议在每个分片上进行测试，并且在组合每个分片上生成的建议时不会重新检查。因此，"缺失"将生成对不包含它们的分片上的术语的建议，即使其他分片确实包含它们。这些应该使用"信心"过滤掉。可以指定三个可能的值：

* "缺失"：仅为不在分片中的术语生成建议。这是默认值。  * "流行"：仅建议分片上文档中出现的术语多于原始术语。  * "始终"：根据建议文本中的字词建议任何匹配的建议。

"max_edits"

|

候选建议可以具有的最大编辑距离，以便被视为建议。只能是介于 1 和 2 之间的值。任何其他值都会导致引发错误的请求错误。默认值为 2。   "prefix_length"

|

必须匹配的最小前缀字符数，以便成为候选建议。默认值为 1。增加此数字可提高拼写检查性能。通常拼写错误不会出现在术语的开头。   "min_word_length"

|

建议文本术语必须具有的最小长度才能包含在内。默认值为 4。   "max_inspections"

|

用于与"shard_size"相乘以在分片级别检查更多候选拼写更正的因子。可以以性能为代价提高准确性。默认值为 5。   "min_doc_freq"

|

建议应出现在的文档数的最小阈值。这可以指定为绝对数或文档数的相对百分比。这可以通过仅建议高频术语来提高质量。默认为 0f 且未启用。如果指定了大于 1 的值，则该数字不能是小数。分片级文档频率用于此选项。   "max_term_freq"

|

建议文本标记可以存在以包含的文档数的最大阈值。可以是相对百分比数(例如，0.4)或绝对数来表示文档频率。如果指定的值大于 1，则不能指定小数。默认值为 0.01f。这可用于排除高频术语(通常拼写正确)的拼写检查。这也提高了拼写检查性能。分片级文档频率用于此选项。   "pre_filter"

|

应用于传递给此候选生成器的每个令牌的筛选器(分析器)。此筛选器在生成候选项之前应用于原始令牌。   "post_filter"

|

一个筛选器(分析器)，在将每个生成的令牌传递给实际短语记分器之前应用于这些令牌。   以下示例显示了具有两个生成器的"短语"建议调用：第一个使用包含普通索引术语的字段，第二个使用使用通过"反向"筛选器索引的术语的字段(标记按相反顺序索引)。这用于克服直接发电机的限制，即需要常量前缀来提供高性能建议。"pre_filter"和"post_filter"选项接受普通分析器名称。

    
    
    POST test/_search
    {
      "suggest": {
        "text" : "obel prize",
        "simple_phrase" : {
          "phrase" : {
            "field" : "title.trigram",
            "size" : 1,
            "direct_generator" : [ {
              "field" : "title.trigram",
              "suggest_mode" : "always"
            }, {
              "field" : "title.reverse",
              "suggest_mode" : "always",
              "pre_filter" : "reverse",
              "post_filter" : "reverse"
            } ]
          }
        }
      }
    }

"pre_filter"和"post_filter"也可用于在生成候选项后注入同义词。例如，对于查询"captain usq"，我们可能会为术语"usq"生成候选"usa"，这是"美国"的同义词。这使我们能够向用户呈现"美国队长"，如果这个短语得分足够高。

### 完成建议器

"完成"建议器提供自动完成/按类型搜索功能。这是一项导航功能，可在用户键入时引导用户找到相关结果，从而提高搜索精度。它不是用于拼写更正或像"术语"或"短语"建议器那样的功能性。

理想情况下，自动完成功能应与用户键入的速度一样快，以提供与用户已键入内容相关的即时反馈。因此，"完成"建议器针对速度进行了优化。建议器使用支持快速查找的数据结构，但构建成本高昂且存储在内存中。

####Mapping

要使用"完成"建议器，请将要从中生成建议的字段映射为类型"完成"。这将为字段值编制索引，以便快速完成。

    
    
    response = client.indices.create(
      index: 'music',
      body: {
        mappings: {
          properties: {
            suggest: {
              type: 'completion'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT music
    {
      "mappings": {
        "properties": {
          "suggest": {
            "type": "completion"
          }
        }
      }
    }

### "完成"字段的参数

"完成"字段接受以下参数：

"分析器"

|

要使用的索引分析器默认为"简单"。   ---|--- "search_analyzer"

|

要使用的搜索分析器默认为"分析器"值。   "preserve_separators"

|

保留分隔符，默认为"true"。如果禁用，您可以找到以"Foo Fighters"开头的领域，如果您建议使用"foof"。   "preserve_position_increments"

|

启用位置增量，默认为"true"。如果禁用并使用停用词分析器，您可以获得一个以"披头士"开头的字段，如果您建议使用"b"。**注意**：您也可以通过索引两个输入"披头士"和"披头士"来实现这一点，如果您能够丰富您的数据，则无需更改简单的分析器。   "max_input_length"

|

限制单个输入的长度，默认为"50"UTF-16 码位。此限制仅在索引时使用，以减少每个输入字符串的字符总数，以防止大量输入使底层数据结构膨胀。大多数用例不会受到默认值的影响，因为前缀补全很少超过前缀长度超过少数字符。   ####Indexingedit

您可以像任何其他字段一样为建议编制索引。建议使用"输入"和可选的"权重"属性。"输入"是与建议查询匹配的预期文本，"权重"确定如何对建议进行评分。为建议编制索引如下：

    
    
    PUT music/_doc/1?refresh
    {
      "suggest" : {
        "input": [ "Nevermind", "Nirvana" ],
        "weight" : 34
      }
    }

支持以下参数：

`input`

|

要存储的输入，这可以是字符串数组或只是一个字符串。此字段是必填字段。

此值不能包含以下 UTF-16 控制字符：

* "\u0000"(空)* "\u001f"(信息分隔符 1)* "\u001e"(信息分隔符 2)

---|---"重量"

|

正整数或包含正整数的字符串，用于定义权重并允许您对建议进行排名。此字段是可选的。   您可以为文档的多个建议编制索引，如下所示：

    
    
    response = client.index(
      index: 'music',
      id: 1,
      refresh: true,
      body: {
        suggest: [
          {
            input: 'Nevermind',
            weight: 10
          },
          {
            input: 'Nirvana',
            weight: 3
          }
        ]
      }
    )
    puts response
    
    
    PUT music/_doc/1?refresh
    {
      "suggest": [
        {
          "input": "Nevermind",
          "weight": 10
        },
        {
          "input": "Nirvana",
          "weight": 3
        }
      ]
    }

您可以使用以下速记形式。请注意，您不能在速记形式中指定带有建议的权重。

    
    
    response = client.index(
      index: 'music',
      id: 1,
      refresh: true,
      body: {
        suggest: [
          'Nevermind',
          'Nirvana'
        ]
      }
    )
    puts response
    
    
    PUT music/_doc/1?refresh
    {
      "suggest" : [ "Nevermind", "Nirvana" ]
    }

####Querying

建议像往常一样工作，只是您必须将建议类型指定为"完成"。建议是近乎实时的，这意味着可以通过刷新使新建议可见，并且文档一旦删除将永远不会显示。此请求：

    
    
    response = client.search(
      index: 'music',
      pretty: true,
      body: {
        suggest: {
          "song-suggest": {
            prefix: 'nir',
            completion: {
              field: 'suggest'
            }
          }
        }
      }
    )
    puts response
    
    
    POST music/_search?pretty
    {
      "suggest": {
        "song-suggest": {
          "prefix": "nir",        __"completion": { __"field": "suggest" __}
        }
      }
    }

__

|

用于搜索建议的前缀 ---|--- __

|

建议类型 __

|

要在其中搜索建议的字段的名称返回此响应：

    
    
    {
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits": ...
      "took": 2,
      "timed_out": false,
      "suggest": {
        "song-suggest" : [ {
          "text" : "nir",
          "offset" : 0,
          "length" : 3,
          "options" : [ {
            "text" : "Nirvana",
            "_index": "music",
            "_id": "1",
            "_score": 1.0,
            "_source": {
              "suggest": ["Nevermind", "Nirvana"]
            }
          } ]
        } ]
      }
    }

必须启用"_source"元数据字段(这是默认行为)，才能返回带有建议的"_source"。

建议的配置权重返回为"_score"。"文本"字段使用索引建议的"输入"。默认情况下，建议返回完整文档"_source"。由于磁盘提取和网络传输开销，"_source"的大小可能会影响性能。为了节省一些网络开销，请使用源代码过滤从"_source"中过滤掉不必要的字段，以最小化"_source"大小。请注意，_suggest终结点不支持源筛选，但在"_search"终结点上使用建议可以：

    
    
    response = client.search(
      index: 'music',
      body: {
        _source: 'suggest',
        suggest: {
          "song-suggest": {
            prefix: 'nir',
            completion: {
              field: 'suggest',
              size: 5
            }
          }
        }
      }
    )
    puts response
    
    
    POST music/_search
    {
      "_source": "suggest",     __"suggest": {
        "song-suggest": {
          "prefix": "nir",
          "completion": {
            "field": "suggest", __"size": 5 __}
        }
      }
    }

__

|

过滤源以仅返回"建议"字段 ---|--- __

|

要在 __ 中搜索建议的字段的名称

|

要返回的建议数 应如下所示：

    
    
    {
      "took": 6,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 0,
          "relation": "eq"
        },
        "max_score": null,
        "hits": []
      },
      "suggest": {
        "song-suggest": [ {
            "text": "nir",
            "offset": 0,
            "length": 3,
            "options": [ {
                "text": "Nirvana",
                "_index": "music",
                "_id": "1",
                "_score": 1.0,
                "_source": {
                  "suggest": [ "Nevermind", "Nirvana" ]
                }
              } ]
          } ]
      }
    }

基本完成建议器查询支持以下参数：

`field`

|

要对其运行查询的字段的名称(必填)。   ---|---"大小"

|

要返回的建议数(默认为"5")。   "skip_duplicates"

|

是否应过滤掉重复的建议(默认为"false")。   完成建议器会考虑索引中的所有文档。请参阅上下文建议器，了解如何改为查询文档子集的说明。

如果完成查询跨越多个分片，则建议分两个阶段执行，其中最后一个阶段从分片中获取相关文档，这意味着对单个分片执行完成请求的性能更高，因为当建议跨越多个分片时，文档获取开销。为了获得最佳完成性能，建议将完成编制索引到单个分片索引中。如果由于分片大小而导致堆使用率较高，仍建议将索引分解为多个分片，而不是优化完成性能。

#### 跳过重复建议

查询可以返回来自不同文档的重复建议。可以通过将"skip_duplicates"设置为 true 来修改此行为。设置后，此选项会从结果中筛选出具有重复建议的文档。

    
    
    response = client.search(
      index: 'music',
      pretty: true,
      body: {
        suggest: {
          "song-suggest": {
            prefix: 'nor',
            completion: {
              field: 'suggest',
              skip_duplicates: true
            }
          }
        }
      }
    )
    puts response
    
    
    POST music/_search?pretty
    {
      "suggest": {
        "song-suggest": {
          "prefix": "nor",
          "completion": {
            "field": "suggest",
            "skip_duplicates": true
          }
        }
      }
    }

设置为 true 时，此选项可能会减慢搜索速度，因为需要访问更多建议才能找到前 N 个建议。

#### 模糊查询

完成建议器还支持模糊查询 - 这意味着您可以在搜索中出现拼写错误，但仍会返回结果。

    
    
    response = client.search(
      index: 'music',
      pretty: true,
      body: {
        suggest: {
          "song-suggest": {
            prefix: 'nor',
            completion: {
              field: 'suggest',
              fuzzy: {
                fuzziness: 2
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST music/_search?pretty
    {
      "suggest": {
        "song-suggest": {
          "prefix": "nor",
          "completion": {
            "field": "suggest",
            "fuzzy": {
              "fuzziness": 2
            }
          }
        }
      }
    }

与查询"前缀"共享最长前缀的建议的评分将更高。

模糊查询可以采用特定的模糊参数。支持以下参数：

`fuzziness`

|

模糊因子默认为"AUTO"。有关允许的设置，请参阅模糊度。   ---|---"换位"

|

如果设置为"true"，则换位计为一次更改而不是两次，默认为"true""min_length"

|

返回模糊建议之前的最小输入长度，默认值为"3""prefix_length"

|

输入的最小长度，未检查模糊替代方案，默认为"1""unicode_aware"

|

如果为"true"，则所有测量值(如模糊编辑距离、换位和长度)都以 Unicode 码位而不是字节为单位进行测量。这比原始字节稍慢，因此默认情况下设置为"false"。   如果你想坚持使用默认值，但仍然使用fuzzy，你可以使用'fuzzy： {}'或'fuzzy： true'。

#### 正则表达式查询

完成建议器还支持正则表达式查询，这意味着您可以将前缀表示为正则表达式

    
    
    response = client.search(
      index: 'music',
      pretty: true,
      body: {
        suggest: {
          "song-suggest": {
            regex: 'n[ever|i]r',
            completion: {
              field: 'suggest'
            }
          }
        }
      }
    )
    puts response
    
    
    POST music/_search?pretty
    {
      "suggest": {
        "song-suggest": {
          "regex": "n[ever|i]r",
          "completion": {
            "field": "suggest"
          }
        }
      }
    }

正则表达式查询可以采用特定的正则表达式参数。支持以下参数：

`flags`

|

可能的标志是"全部"(默认)、"任意字符串"、"补码"、"空"、"交集"、"间隔"或"无"。请参阅正则表达式语法的含义---|--- 'max_determinized_states'

|

正则表达式很危险，因为很容易意外地创建看起来无害的表达式，该表达式需要指数数量的内部确定的自动机状态(以及相应的 RAM 和 CPU)才能执行 Lucene。Lucene 使用"max_determinized_states"设置(默认为 10000)阻止这些设置。您可以提高此限制以允许执行更复杂的正则表达式。   ### 上下文建议器编辑

完成建议器会考虑索引中的所有文档，但通常需要提供按某些标准过滤和/或提升的建议。例如，您想建议由某些艺术家过滤的歌曲标题，或者您想根据他们的流派提升歌曲标题。

要实现建议过滤和/或提升，您可以在配置完成字段时添加上下文映射。您可以为完成字段定义多个上下文映射。每个上下文映射都有唯一的名称和类型。有两种类型："类别"和"地理"。上下文映射在字段映射中的"上下文"参数下配置。

在索引和查询启用上下文的完成字段时，必须提供上下文。

允许的最大完成字段上下文映射数为 10。

下面定义了类型，每个类型都有一个完成字段的两个上下文映射：

    
    
    response = client.indices.create(
      index: 'place',
      body: {
        mappings: {
          properties: {
            suggest: {
              type: 'completion',
              contexts: [
                {
                  name: 'place_type',
                  type: 'category'
                },
                {
                  name: 'location',
                  type: 'geo',
                  precision: 4
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.create(
      index: 'place_path_category',
      body: {
        mappings: {
          properties: {
            suggest: {
              type: 'completion',
              contexts: [
                {
                  name: 'place_type',
                  type: 'category',
                  path: 'cat'
                },
                {
                  name: 'location',
                  type: 'geo',
                  precision: 4,
                  path: 'loc'
                }
              ]
            },
            loc: {
              type: 'geo_point'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT place
    {
      "mappings": {
        "properties": {
          "suggest": {
            "type": "completion",
            "contexts": [
              {                                 __"name": "place_type",
                "type": "category"
              },
              { __"name": "location",
                "type": "geo",
                "precision": 4
              }
            ]
          }
        }
      }
    }
    PUT place_path_category
    {
      "mappings": {
        "properties": {
          "suggest": {
            "type": "completion",
            "contexts": [
              { __"name": "place_type",
                "type": "category",
                "path": "cat"
              },
              { __"name": "location",
                "type": "geo",
                "precision": 4,
                "path": "loc"
              }
            ]
          },
          "loc": {
            "type": "geo_point"
          }
        }
      }
    }

__

|

定义名为 _place_type_ 的"类别"上下文，其中类别必须随建议一起发送。   ---|---    __

|

定义一个名为 _location_ 的"地理"上下文，其中类别必须随建议一起发送。   __

|

定义名为_place_type_的"类别"上下文，其中从"cat"字段中读取类别。   __

|

定义一个名为 _location_ 的"地理"上下文，其中从"loc"字段中读取类别。   添加上下文映射会增加完成字段的索引大小。完成索引完全驻留在堆中，您可以使用索引统计信息监视完成字段索引大小。

##### 类别上下文

"类别"上下文允许您在索引时将一个或多个类别与建议相关联。在查询时，可以按建议的关联类别进行筛选和提升。

映射的设置类似于上面的"place_type"字段。如果定义了"path"，则从文档中的该路径读取类别，否则必须在建议字段中发送它们，如下所示：

    
    
    PUT place/_doc/1
    {
      "suggest": {
        "input": [ "timmy's", "starbucks", "dunkin donuts" ],
        "contexts": {
          "place_type": [ "cafe", "food" ]                    __}
      }
    }

__

|

这些建议将与 _cafe_ 和 _food_ 类别相关联。   ---|--- 如果映射具有"路径"，则以下索引请求足以添加类别：

    
    
    PUT place_path_category/_doc/1
    {
      "suggest": ["timmy's", "starbucks", "dunkin donuts"],
      "cat": ["cafe", "food"] __}

__

|

这些建议将与 _cafe_ 和 _food_ 类别相关联。   ---|--- 如果上下文映射引用了另一个字段，并且类别已显式编制索引，则建议将使用这两组类别编制索引。

###### 类别查询

可以按一个或多个类别筛选建议。以下按多个类别筛选建议：

    
    
    response = client.search(
      index: 'place',
      pretty: true,
      body: {
        suggest: {
          place_suggestion: {
            prefix: 'tim',
            completion: {
              field: 'suggest',
              size: 10,
              contexts: {
                place_type: [
                  'cafe',
                  'restaurants'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST place/_search?pretty
    {
      "suggest": {
        "place_suggestion": {
          "prefix": "tim",
          "completion": {
            "field": "suggest",
            "size": 10,
            "contexts": {
              "place_type": [ "cafe", "restaurants" ]
            }
          }
        }
      }
    }

如果在查询上设置了多个类别或类别上下文，则它们将作为析取出现。这意味着，如果建议至少包含一个提供的上下文值，则建议匹配。

某些类别的建议可以比其他类别的推荐更高。以下内容按类别筛选建议，并额外提升与某些类别关联的建议：

    
    
    response = client.search(
      index: 'place',
      pretty: true,
      body: {
        suggest: {
          place_suggestion: {
            prefix: 'tim',
            completion: {
              field: 'suggest',
              size: 10,
              contexts: {
                place_type: [
                  {
                    context: 'cafe'
                  },
                  {
                    context: 'restaurants',
                    boost: 2
                  }
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST place/_search?pretty
    {
      "suggest": {
        "place_suggestion": {
          "prefix": "tim",
          "completion": {
            "field": "suggest",
            "size": 10,
            "contexts": {
              "place_type": [                             __{ "context": "cafe" },
                { "context": "restaurants", "boost": 2 }
              ]
            }
          }
        }
      }
    }

__

|

上下文查询筛选与类别 _cafe_ 关联的建议and_restaurants_，并通过因子"2"---|提升与 _restaurants_ 关联的建议--- 除了接受类别值外，上下文查询还可以由多个类别上下文子句组成。"类别"上下文子句支持以下参数：

`context`

|

要筛选/提升的类别的值。这是强制性的。   ---|---"提升"

|

建议分数应提高的因子，分数是通过将提升乘以建议权重来计算的，默认为"1""前缀"

|

是否应将类别值视为前缀。例如，如果设置为"true"，则可以通过指定类别前缀 _type_ 来筛选_type1_、_type2_等类别。默认为"false" 如果建议条目与多个上下文匹配，则最终分数将计算为任何匹配上下文产生的最大分数。

##### 地理位置上下文

"geo"上下文允许您在索引时将一个或多个地理点或地理哈希与建议相关联。在查询时，如果建议在指定地理位置的一定距离内，则可以对其进行筛选和提升。

在内部，地理点被编码为具有指定精度的地理哈希。

###### 地理映射

除了"路径"设置外，"geo"上下文映射还接受以下设置：

`precision`

|

这定义了要索引的地理哈希的精度，可以指定为距离值("5m"、"10km"等)或原始地理哈希精度("1")。'12').默认为原始地理哈希精度值"6"。   ---|--- 索引时间"精度"设置设置可在查询时使用的最大地理哈希精度。

###### 索引地理环境

"geo"上下文可以使用建议显式设置，也可以通过"path"参数从文档中的地理点字段进行索引，类似于"类别"上下文。将多个地理位置上下文与建议相关联，将为每个地理位置的建议编制索引。以下索引建议使用两个地理位置上下文：

    
    
    response = client.index(
      index: 'place',
      id: 1,
      body: {
        suggest: {
          input: "timmy's",
          contexts: {
            location: [
              {
                lat: 43.6624803,
                lon: -79.3863353
              },
              {
                lat: 43.6624718,
                lon: -79.3873227
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    PUT place/_doc/1
    {
      "suggest": {
        "input": "timmy's",
        "contexts": {
          "location": [
            {
              "lat": 43.6624803,
              "lon": -79.3863353
            },
            {
              "lat": 43.6624718,
              "lon": -79.3873227
            }
          ]
        }
      }
    }

###### 地理位置查询

可以根据建议与一个或多个地理点的接近程度对建议进行过滤和提升。以下筛选属于地理点的编码地理哈希所表示区域内的建议：

    
    
    response = client.search(
      index: 'place',
      body: {
        suggest: {
          place_suggestion: {
            prefix: 'tim',
            completion: {
              field: 'suggest',
              size: 10,
              contexts: {
                location: {
                  lat: 43.662,
                  lon: -79.38
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST place/_search
    {
      "suggest": {
        "place_suggestion": {
          "prefix": "tim",
          "completion": {
            "field": "suggest",
            "size": 10,
            "contexts": {
              "location": {
                "lat": 43.662,
                "lon": -79.380
              }
            }
          }
        }
      }
    }

如果指定了查询时精度较低的位置，则将考虑属于该区域的所有建议。

如果在查询上设置了多个类别或类别上下文，则它们将作为析取出现。这意味着，如果建议至少包含一个提供的上下文值，则建议匹配。

位于地理哈希表示区域内的建议也可以比其他建议提升得更高，如下所示：

    
    
    response = client.search(
      index: 'place',
      pretty: true,
      body: {
        suggest: {
          place_suggestion: {
            prefix: 'tim',
            completion: {
              field: 'suggest',
              size: 10,
              contexts: {
                location: [
                  {
                    lat: 43.6624803,
                    lon: -79.3863353,
                    precision: 2
                  },
                  {
                    context: {
                      lat: 43.6624803,
                      lon: -79.3863353
                    },
                    boost: 2
                  }
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST place/_search?pretty
    {
      "suggest": {
        "place_suggestion": {
          "prefix": "tim",
          "completion": {
            "field": "suggest",
            "size": 10,
            "contexts": {
              "location": [             __{
                  "lat": 43.6624803,
                  "lon": -79.3863353,
                  "precision": 2
                },
                {
                  "context": {
                    "lat": 43.6624803,
                    "lon": -79.3863353
                  },
                  "boost": 2
                }
              ]
            }
          }
        }
      }
    }

__

|

上下文查询会筛选属于地理位置的建议，这些建议由 _(43.662， -79.380)_ 表示，精度为 _2_，并将属于 _(43.6624803，-79.3863353)_ 的地理哈希表示形式的建议(默认精度为 _6_)提升系数为"2"---|--- 如果建议条目与多个上下文匹配，则最终分数将计算为任何匹配上下文生成的最大分数。

除了接受上下文值之外，上下文查询还可以由多个上下文子句组成。"geo"上下文子句支持以下参数：

`context`

|

用于筛选或提升建议的地理点对象或地理哈希字符串。这是强制性的。   ---|---"提升"

|

建议分数应提高的因子，分数通过将提升乘以建议权重来计算，默认为"1""精度"

|

用于对查询地理点进行编码的地理哈希的精度。这可以指定为距离值("5m"、"10km"等)，也可以指定为原始地理哈希精度("1")。'12').默认为索引时间精度级别。   "邻居"

|

接受精度值数组，在该值处应考虑相邻的地理哈希。精度值可以是距离值("5m"、"10km"等)或原始地理哈希精度("1")。'12').默认为为索引时间精度级别生成邻居。   精度字段不会导致距离匹配。指定距离值(如"10km")只会生成表示该大小的切片的地理哈希精度值。精度将用于将搜索地理点编码到地理哈希磁贴中，以实现完成匹配。这样做的结果是，该磁贴之外的点，即使非常靠近搜索点，也不会匹配。降低精度或增加距离可以降低发生这种情况的风险，但不能完全消除它。

### 返回建议器的类型

有时您需要知道建议器的确切类型才能解析其结果。"typed_keys"参数可用于更改响应中建议器的名称，以便以建议器的类型为前缀。

考虑以下示例，其中包含两个建议器"term"和"phrase"：

    
    
    response = client.search(
      typed_keys: true,
      body: {
        suggest: {
          text: 'some test mssage',
          "my-first-suggester": {
            term: {
              field: 'message'
            }
          },
          "my-second-suggester": {
            phrase: {
              field: 'message'
            }
          }
        }
      }
    )
    puts response
    
    
    POST _search?typed_keys
    {
      "suggest": {
        "text" : "some test mssage",
        "my-first-suggester" : {
          "term" : {
            "field" : "message"
          }
        },
        "my-second-suggester" : {
          "phrase" : {
            "field" : "message"
          }
        }
      }
    }

在响应中，建议者名称将分别更改为"term#my-first-suggester"和"phrase#my-second-suggester"，以反映每个建议的类型：

    
    
    {
      "suggest": {
        "term#my-first-suggester": [ __{
            "text": "some",
            "offset": 0,
            "length": 4,
            "options": []
          },
          {
            "text": "test",
            "offset": 5,
            "length": 4,
            "options": []
          },
          {
            "text": "mssage",
            "offset": 10,
            "length": 6,
            "options": [
              {
                "text": "message",
                "score": 0.8333333,
                "freq": 4
              }
            ]
          }
        ],
        "phrase#my-second-suggester": [ __{
            "text": "some test mssage",
            "offset": 0,
            "length": 16,
            "options": [
              {
                "text": "some test message",
                "score": 0.030227963
              }
            ]
          }
        ]
      },
      ...
    }

__

|

名称"我的第一个建议者"现在包含"术语"前缀。   ---|---    __

|

名称"我的第二个建议器"现在包含"短语"前缀。   « 搜索分片 API 多搜索 API »