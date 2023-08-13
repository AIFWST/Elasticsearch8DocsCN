

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Full text queries](full-text-queries.md) [Match query »](query-dsl-match-
query.md)

## 间隔查询

根据匹配术语的顺序和邻近性返回文档。

"间隔"查询使用**匹配规则**，由一小组定义构造而成。然后，这些规则将应用于指定"字段"中的术语。

这些定义生成跨越文本正文中的术语的最小间隔序列。这些间隔可以进一步组合并按父源过滤。

### 示例请求

以下"间隔"搜索返回包含"我最喜欢的食物"的文档，没有任何间隙，后跟"热水"或"冷粥"字段中的"my_text"。

此搜索将匹配"我最喜欢的食物是冷粥"的"my_text"值，但不匹配"当天气冷时，我最喜欢的食物是粥"。

    
    
    response = client.search(
      body: {
        query: {
          intervals: {
            my_text: {
              all_of: {
                ordered: true,
                intervals: [
                  {
                    match: {
                      query: 'my favorite food',
                      max_gaps: 0,
                      ordered: true
                    }
                  },
                  {
                    any_of: {
                      intervals: [
                        {
                          match: {
                            query: 'hot water'
                          }
                        },
                        {
                          match: {
                            query: 'cold porridge'
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST _search
    {
      "query": {
        "intervals" : {
          "my_text" : {
            "all_of" : {
              "ordered" : true,
              "intervals" : [
                {
                  "match" : {
                    "query" : "my favorite food",
                    "max_gaps" : 0,
                    "ordered" : true
                  }
                },
                {
                  "any_of" : {
                    "intervals" : [
                      { "match" : { "query" : "hot water" } },
                      { "match" : { "query" : "cold porridge" } }
                    ]
                  }
                }
              ]
            }
          }
        }
      }
    }

### "间隔"的顶级参数

`<field>`

    

(必需，规则对象)您要搜索的字段。

此参数的值是一个规则对象，用于根据匹配的术语、顺序和邻近度来匹配文档。

有效规则包括：

* "匹配" * "前缀" * "通配符" * "模糊" * "all_of" * "any_of"

### "匹配"规则参数

"匹配"规则匹配分析的文本。

`query`

     (Required, string) Text you wish to find in the provided `<field>`. 
`max_gaps`

    

(可选，整数)匹配项之间的最大位置数。比这更远的术语不被视为匹配项。默认为"-1"。

如果未指定或设置为"-1"，则匹配项没有宽度限制。如果设置为"0"，则字词必须彼此相邻显示。

`ordered`

     (Optional, Boolean) If `true`, matching terms must appear in their specified order. Defaults to `false`. 
`analyzer`

     (Optional, string) [analyzer](analysis.html "Text analysis") used to analyze terms in the `query`. Defaults to the top-level `<field>`'s analyzer. 
`filter`

     (Optional, [interval filter](query-dsl-intervals-query.html#interval_filter "filter rule parameters") rule object) An optional interval filter. 
`use_field`

     (Optional, string) If specified, then match intervals from this field rather than the top-level `<field>`. Terms are analyzed using the search analyzer from this field. This allows you to search across multiple fields as if they were all the same field; for example, you could index the same text into stemmed and unstemmed fields, and search for stemmed tokens near unstemmed ones. 

### "前缀"规则参数

"前缀"规则匹配以一组指定字符开头的字词。此前缀可以扩展以匹配最多 128 个术语。如果前缀匹配的术语超过 128 个，Elasticsearch 将返回错误。您可以在字段映射中使用"索引前缀"选项来避免此限制。

`prefix`

     (Required, string) Beginning characters of terms you wish to find in the top-level `<field>`. 
`analyzer`

     (Optional, string) [analyzer](analysis.html "Text analysis") used to normalize the `prefix`. Defaults to the top-level `<field>`'s analyzer. 
`use_field`

    

(可选，字符串)如果指定，则匹配此字段的间隔，而不是顶级 '<field>'。

"前缀"使用此字段中的搜索分析器进行规范化，除非指定了单独的"分析器"。

### "通配符"规则参数

"通配符"规则使用通配符模式匹配术语。此模式可以扩展以匹配最多 128 个术语。如果模式匹配的项超过 128 个，Elasticsearch 将返回错误。

`pattern`

    

(必需，字符串)用于查找匹配项的通配符模式。

此参数支持两个通配符运算符：

* '？'，匹配任何单个字符 * '*'，可以匹配零个或多个字符，包括空字符

避免以"*"或"？"开头模式。这可能会增加查找匹配字词所需的迭代次数，并降低搜索性能。

`analyzer`

     (Optional, string) [analyzer](analysis.html "Text analysis") used to normalize the `pattern`. Defaults to the top-level `<field>`'s analyzer. 
`use_field`

    

(可选，字符串)如果指定，则匹配此字段的间隔，而不是顶级 '<field>'。

"模式"使用此字段中的搜索分析器进行规范化，除非单独指定"分析器"。

### "模糊"规则参数

"模糊"规则匹配与提供的术语相似的术语，在模糊定义的编辑距离内。如果模糊扩展匹配的项超过 128 个，Elasticsearch 将返回错误。

`term`

     (Required, string) The term to match 
`prefix_length`

     (Optional, integer) Number of beginning characters left unchanged when creating expansions. Defaults to `0`. 
`transpositions`

     (Optional, Boolean) Indicates whether edits include transpositions of two adjacent characters (ab → ba). Defaults to `true`. 
`fuzziness`

     (Optional, string) Maximum edit distance allowed for matching. See [Fuzziness](common-options.html#fuzziness "Fuzziness") for valid values and more information. Defaults to `auto`. 
`analyzer`

     (Optional, string) [analyzer](analysis.html "Text analysis") used to normalize the `term`. Defaults to the top-level `<field>` 's analyzer. 
`use_field`

    

(可选，字符串)如果指定，则匹配此字段的间隔，而不是顶级 '<field>'。

"术语"使用此字段中的搜索分析器进行规范化，除非单独指定"分析器"。

### 'all_of' 规则参数

"all_of"规则返回跨越其他规则组合的匹配项。

`intervals`

     (Required, array of rule objects) An array of rules to combine. All rules must produce a match in a document for the overall source to match. 
`max_gaps`

    

(可选，整数)匹配项之间的最大位置数。规则产生的间隔比这更远，不被视为匹配。默认为"-1"。

如果未指定或设置为"-1"，则匹配项没有宽度限制。如果设置为"0"，则字词必须彼此相邻显示。

`ordered`

     (Optional, Boolean) If `true`, intervals produced by the rules should appear in the order in which they are specified. Defaults to `false`. 
`filter`

     (Optional, [interval filter](query-dsl-intervals-query.html#interval_filter "filter rule parameters") rule object) Rule used to filter returned intervals. 

### 'any_of' 规则参数

"any_of"规则返回由其任何子规则生成的间隔。

`intervals`

     (Required, array of rule objects) An array of rules to match. 
`filter`

     (Optional, [interval filter](query-dsl-intervals-query.html#interval_filter "filter rule parameters") rule object) Rule used to filter returned intervals. 

### "过滤器"规则参数

"筛选器"规则根据查询返回间隔。有关示例，请参阅筛选器示例。

`after`

     (Optional, query object) Query used to return intervals that follow an interval from the `filter` rule. 
`before`

     (Optional, query object) Query used to return intervals that occur before an interval from the `filter` rule. 
`contained_by`

     (Optional, query object) Query used to return intervals contained by an interval from the `filter` rule. 
`containing`

     (Optional, query object) Query used to return intervals that contain an interval from the `filter` rule. 
`not_contained_by`

     (Optional, query object) Query used to return intervals that are **not** contained by an interval from the `filter` rule. 
`not_containing`

     (Optional, query object) Query used to return intervals that do **not** contain an interval from the `filter` rule. 
`not_overlapping`

     (Optional, query object) Query used to return intervals that do **not** overlap with an interval from the `filter` rule. 
`overlapping`

     (Optional, query object) Query used to return intervals that overlap with an interval from the `filter` rule. 
`script`

     (Optional, [script object](modules-scripting-using.html "How to write scripts")) Script used to return matching documents. This script must return a boolean value, `true` or `false`. See [Script filters](query-dsl-intervals-query.html#interval-script-filter "Script filters") for an example. 

###Notes

#### 筛选器示例

以下搜索包括"筛选器"规则。它返回具有单词"热"和"粥"的文档，这些单词彼此相距 10 个位置，中间没有单词"咸"：

    
    
    response = client.search(
      body: {
        query: {
          intervals: {
            my_text: {
              match: {
                query: 'hot porridge',
                max_gaps: 10,
                filter: {
                  not_containing: {
                    match: {
                      query: 'salty'
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
    
    
    POST _search
    {
      "query": {
        "intervals" : {
          "my_text" : {
            "match" : {
              "query" : "hot porridge",
              "max_gaps" : 10,
              "filter" : {
                "not_containing" : {
                  "match" : {
                    "query" : "salty"
                  }
                }
              }
            }
          }
        }
      }
    }

#### 脚本筛选器

您可以使用脚本根据间隔的起始位置、结束位置和内部间隙计数来筛选间隔。以下"过滤器"脚本使用"间隔"变量和"开始"、"结束"和"间隙"方法：

    
    
    response = client.search(
      body: {
        query: {
          intervals: {
            my_text: {
              match: {
                query: 'hot porridge',
                filter: {
                  script: {
                    source: 'interval.start > 10 && interval.end < 20 && interval.gaps == 0'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST _search
    {
      "query": {
        "intervals" : {
          "my_text" : {
            "match" : {
              "query" : "hot porridge",
              "filter" : {
                "script" : {
                  "source" : "interval.start > 10 && interval.end < 20 && interval.gaps == 0"
                }
              }
            }
          }
        }
      }
    }

####Minimization

间隔查询始终最小化间隔，以确保查询可以在线性时间内运行。这有时会导致令人惊讶的结果，尤其是在使用"max_gaps"限制或过滤器时。例如，采用以下查询，搜索短语"热粥"中包含的"咸"：

    
    
    response = client.search(
      body: {
        query: {
          intervals: {
            my_text: {
              match: {
                query: 'salty',
                filter: {
                  contained_by: {
                    match: {
                      query: 'hot porridge'
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
    
    
    POST _search
    {
      "query": {
        "intervals" : {
          "my_text" : {
            "match" : {
              "query" : "salty",
              "filter" : {
                "contained_by" : {
                  "match" : {
                    "query" : "hot porridge"
                  }
                }
              }
            }
          }
        }
      }
    }

此查询**不**与包含短语"热粥是咸粥"的文档匹配，因为匹配查询返回的"热粥"间隔仅涵盖本文档中的前两个术语，并且这些间隔不会与涵盖"咸"的间隔重叠。

另一个需要注意的限制是包含重叠子规则的"any_of"规则的情况。特别是，如果其中一个规则是另一个规则的严格前缀，那么较长的规则永远无法匹配，当与"max_gaps"结合使用时，可能会导致意外。考虑以下查询，搜索"the"紧跟"big"或"big bad"，紧跟"wolf"：

    
    
    response = client.search(
      body: {
        query: {
          intervals: {
            my_text: {
              all_of: {
                intervals: [
                  {
                    match: {
                      query: 'the'
                    }
                  },
                  {
                    any_of: {
                      intervals: [
                        {
                          match: {
                            query: 'big'
                          }
                        },
                        {
                          match: {
                            query: 'big bad'
                          }
                        }
                      ]
                    }
                  },
                  {
                    match: {
                      query: 'wolf'
                    }
                  }
                ],
                max_gaps: 0,
                ordered: true
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST _search
    {
      "query": {
        "intervals" : {
          "my_text" : {
            "all_of" : {
              "intervals" : [
                { "match" : { "query" : "the" } },
                { "any_of" : {
                    "intervals" : [
                        { "match" : { "query" : "big" } },
                        { "match" : { "query" : "big bad" } }
                    ] } },
                { "match" : { "query" : "wolf" } }
              ],
              "max_gaps" : 0,
              "ordered" : true
            }
          }
        }
      }
    }

与直觉相反，此查询与文档"大坏狼"不匹配，因为中间的"any_of"规则仅产生"大"的间隔，"大坏蛋"的间隔比"大"的间隔长，同时从同一位置开始，因此被最小化。在这些情况下，最好重写查询，以便在顶层显式布置所有选项：

    
    
    response = client.search(
      body: {
        query: {
          intervals: {
            my_text: {
              any_of: {
                intervals: [
                  {
                    match: {
                      query: 'the big bad wolf',
                      ordered: true,
                      max_gaps: 0
                    }
                  },
                  {
                    match: {
                      query: 'the big wolf',
                      ordered: true,
                      max_gaps: 0
                    }
                  }
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST _search
    {
      "query": {
        "intervals" : {
          "my_text" : {
            "any_of" : {
              "intervals" : [
                { "match" : {
                    "query" : "the big bad wolf",
                    "ordered" : true,
                    "max_gaps" : 0 } },
                { "match" : {
                    "query" : "the big wolf",
                    "ordered" : true,
                    "max_gaps" : 0 } }
               ]
            }
          }
        }
      }
    }

[« Full text queries](full-text-queries.md) [Match query »](query-dsl-match-
query.md)
