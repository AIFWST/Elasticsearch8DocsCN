

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Filter search results](filter-search-results.md) [Long-running searches
»](async-search-intro.md)

##Highlighting

通过荧光笔，您可以从搜索结果中的一个或多个字段中获取突出显示的代码段，以便向用户显示查询匹配项的位置。当您请求突出显示时，响应会为每个搜索匹配包含一个额外的"突出显示"元素，其中包括突出显示的字段和突出显示的片段。

突出显示器在提取要突出显示的术语时不反映查询的布尔逻辑。因此，对于一些复杂的布尔查询(例如嵌套布尔查询、使用"minimum_should_match"的查询等)，文档的某些部分可能会突出显示与查询匹配不对应的部分。

突出显示需要字段的实际内容。如果未存储字段(映射未将"store"设置为"true")，则会加载实际的"_source"，并从"_source"中提取相关字段。

例如，要使用默认荧光笔获取每个搜索中"内容"字段的突出显示，请在指定"内容"字段的请求正文中包含"突出显示"对象：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            content: 'kimchy'
          }
        },
        highlight: {
          fields: {
            content: {}
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match": { "content": "kimchy" }
      },
      "highlight": {
        "fields": {
          "content": {}
        }
      }
    }

Elasticsearch支持三种荧光笔："统一"，"普通"和"fvh"(快速矢量荧光笔)。您可以为每个字段指定要使用的荧光笔"类型"。

### 统一荧光笔

"统一"荧光笔使用 Lucene 统一荧光笔。此荧光笔将文本分解为句子，并使用 BM25 算法对单个句子进行评分，就好像它们是语料库中的文档一样。它还支持准确的短语和多术语(模糊、前缀、正则表达式)突出显示。这是默认荧光笔。

### 普通荧光笔

"普通"荧光笔使用标准的Lucene荧光笔。它尝试在理解单词重要性和短语查询中的任何单词定位条件方面反映查询匹配逻辑。

"普通"荧光笔最适合突出显示单个字段中的简单查询匹配项。为了准确反映查询逻辑，它创建了一个微小的内存索引，并通过 Lucene 的查询执行计划器重新运行原始查询条件，以访问当前文档的低级匹配信息。对需要突出显示的每个字段和每个文档重复此操作。如果要突出显示具有复杂查询的大量文档中的大量字段，我们建议在"帖子"或"term_vector"字段中使用"统一"荧光笔。

### 快速矢量荧光笔

"fvh"荧光笔使用Lucene快速矢量荧光笔。此荧光笔可用于映射中"term_vector"设置为"with_positions_offsets"的字段。快速矢量荧光笔：

*可以用"boundary_scanner"定制。  * 需要将"term_vector"设置为"with_positions_offsets"，这会增加索引的大小 * 可以将多个字段的匹配项合并为一个结果。请参阅"matched_fields" * 可以为不同位置的匹配项分配不同的权重，允许在突出显示提升查询时将短语匹配排序在术语匹配之上，从而在术语匹配中提升短语匹配项的增强查询时，将短语匹配项排序在术语匹配项之上

"fvh"荧光笔不支持跨度查询。如果您需要支持 forspan 查询，请尝试使用其他荧光笔，例如"统一"荧光笔。

### 偏移策略

为了从被查询的术语中创建有意义的搜索片段，荧光笔需要知道原始文本中每个单词的开始和结束字符偏移量。这些偏移可以从以下位置获得：

* 帖子列表。如果在映射中将"index_options"设置为"偏移"，则"统一"荧光笔会使用此信息突出显示文档，而无需重新分析文本。它直接在过帐上重新运行原始查询，并从索引中提取匹配的偏移量，从而将集合限制为突出显示的文档。如果您有较大的字段，这一点很重要，因为它不需要重新分析要突出显示的文本。与使用"term_vectors"相比，它还需要更少的磁盘空间。  * 术语向量。如果在映射中将"term_vector"设置为"with_positions_offsets"来提供"term_vector"信息，则"统一"荧光笔会自动使用"term_vector"突出显示该字段。它的速度特别快，特别是对于大字段(>"1MB")和突出显示"前缀"或"通配符"等多术语查询，因为它可以访问每个文档的术语字典。"fvh"荧光笔始终使用术语向量。  *普通突出显示。当没有其他选择时，"统一"使用此模式。它创建一个微小的内存索引，并通过 Lucene 的查询执行计划器重新运行原始查询条件，以访问当前文档的低级匹配信息。对需要突出显示的每个字段和每个文档重复此操作。"普通"荧光笔始终使用普通高光。

大文本的普通突出显示可能需要大量的时间和内存。为了防止这种情况，将分析的最大文本字符数已限制为 1000000。对于具有索引设置"index.highlight.max_analyzed_offset"的特定索引，可以更改此默认限制。

### 突出显示设置

可以在全局级别设置突出显示设置，也可以在字段级别覆盖突出显示设置。

boundary_chars

     A string that contains each boundary character. Defaults to `.,!? \t\n`. 
boundary_max_scan

     How far to scan for boundary characters. Defaults to `20`. 

boundary_scanner

    

指定如何断开突出显示的片段："字符"、"句子"或"单词"。仅适用于"统一"和"fvh"荧光笔。默认为"句子"作为"统一"荧光笔。默认为"字符"表示"fvh"荧光笔。

`chars`

     Use the characters specified by `boundary_chars` as highlighting boundaries. The `boundary_max_scan` setting controls how far to scan for boundary characters. Only valid for the `fvh` highlighter. 
`sentence`

    

在下一个句子边界处的 Break 突出显示片段，由 Java 的 BreakIterator 确定。您可以指定要与"boundary_scanner_locale"一起使用的区域设置。

当与"统一"荧光笔一起使用时，"句子"扫描仪会在"fragment_size"旁边的第一个单词边界处拆分大于"fragment_size"的句子。您可以将"fragment_size"设置为 0 以永不拆分任何句子。

`word`

     Break highlighted fragments at the next word boundary, as determined by Java's [BreakIterator](https://docs.oracle.com/javase/8/docs/api/java/text/BreakIterator.html). You can specify the locale to use with `boundary_scanner_locale`. 

boundary_scanner_locale

     Controls which locale is used to search for sentence and word boundaries. This parameter takes a form of a language tag, e.g. `"en-US"`, `"fr-FR"`, `"ja-JP"`. More info can be found in the [Locale Language Tag](https://docs.oracle.com/javase/8/docs/api/java/util/Locale.html#forLanguageTag-java.lang.String-) documentation. The default value is [ Locale.ROOT](https://docs.oracle.com/javase/8/docs/api/java/util/Locale.html#ROOT). 
encoder

     Indicates if the snippet should be HTML encoded: `default` (no encoding) or `html` (HTML-escape the snippet text and then insert the highlighting tags) 
fields

    

指定要检索其突出显示的字段。可以使用通配符指定字段。例如，您可以指定"comment_*"以获取以"comment_"开头的所有文本、match_only_text和关键字字段的突出显示。

使用通配符时，仅突出显示文本、match_only_text和关键字字段。如果使用自定义映射器并且仍然想在字段上突出显示，则必须显式指定该字段名称。

fragmenter

     Specifies how text should be broken up in highlight snippets: `simple` or `span`. Only valid for the `plain` highlighter. Defaults to `span`. 
force_source

    

荒废的;此参数不起作用

`simple`

     Breaks up text into same-sized fragments. 
`span`

     Breaks up text into same-sized fragments, but tries to avoid breaking up text between highlighted terms. This is helpful when you're querying for phrases. Default. 

fragment_offset

     Controls the margin from which you want to start highlighting. Only valid when using the `fvh` highlighter. 
fragment_size

     The size of the highlighted fragment in characters. Defaults to 100. 
highlight_query

    

突出显示搜索查询以外的查询的匹配项。如果使用重新评分查询，这将特别有用，因为默认情况下不会通过突出显示来考虑这些查询。

Elasticsearch 不会以任何方式验证"highlight_query"是否包含搜索查询，因此可以对其进行定义，以便不会突出显示合法的查询结果。通常，应将搜索查询作为"highlight_query"的一部分包含在内。

matched_fields

     Combine matches on multiple fields to highlight a single field. This is most intuitive for multifields that analyze the same string in different ways. All `matched_fields` must have `term_vector` set to `with_positions_offsets`, but only the field to which the matches are combined is loaded so only that field benefits from having `store` set to `yes`. Only valid for the `fvh` highlighter. 
no_match_size

     The amount of text you want to return from the beginning of the field if there are no matching fragments to highlight. Defaults to 0 (nothing is returned). 
number_of_fragments

     The maximum number of fragments to return. If the number of fragments is set to 0, no fragments are returned. Instead, the entire field contents are highlighted and returned. This can be handy when you need to highlight short texts such as a title or address, but fragmentation is not required. If `number_of_fragments` is 0, `fragment_size` is ignored. Defaults to 5. 
order

     Sorts highlighted fragments by score when set to `score`. By default, fragments will be output in the order they appear in the field (order: `none`). Setting this option to `score` will output the most relevant fragments first. Each highlighter applies its own logic to compute relevancy scores. See the document [How highlighters work internally](highlighting.html#how-es-highlighters-work-internally "How highlighters work internally") for more details how different highlighters find the best fragments. 
phrase_limit

     Controls the number of matching phrases in a document that are considered. Prevents the `fvh` highlighter from analyzing too many phrases and consuming too much memory. When using `matched_fields`, `phrase_limit` phrases per matched field are considered. Raising the limit increases query time and consumes more memory. Only supported by the `fvh` highlighter. Defaults to 256. 
pre_tags

     Use in conjunction with `post_tags` to define the HTML tags to use for the highlighted text. By default, highlighted text is wrapped in `<em>` and `</em>` tags. Specify as an array of strings. 
post_tags

     Use in conjunction with `pre_tags` to define the HTML tags to use for the highlighted text. By default, highlighted text is wrapped in `<em>` and `</em>` tags. Specify as an array of strings. 
require_field_match

     By default, only fields that contains a query match are highlighted. Set `require_field_match` to `false` to highlight all fields. Defaults to `true`. 

max_analyzed_offset

     By default, the maximum number of characters analyzed for a highlight request is bounded by the value defined in the [`index.highlight.max_analyzed_offset`](index-modules.html#index-max-analyzed-offset) setting, and when the number of characters exceeds this limit an error is returned. If this setting is set to a non-negative value, the highlighting stops at this defined maximum limit, and the rest of the text is not processed, thus not highlighted and no error is returned. The [`max_analyzed_offset`](highlighting.html#max-analyzed-offset) query setting does **not** override the [`index.highlight.max_analyzed_offset`](index-modules.html#index-max-analyzed-offset) which prevails when it's set to lower value than the query setting. 
tags_schema

    

设置为"样式"以使用内置标记架构。"样式"架构定义以下"pre_tags"并将"post_tags"定义为"</em>"。

    
    
    <em class="hlt1">, <em class="hlt2">, <em class="hlt3">,
    <em class="hlt4">, <em class="hlt5">, <em class="hlt6">,
    <em class="hlt7">, <em class="hlt8">, <em class="hlt9">,
    <em class="hlt10">

type

     The highlighter to use: `unified`, `plain`, or `fvh`. Defaults to `unified`. 

### 突出显示示例

* 覆盖全局设置 * 指定突出显示查询 * 设置荧光笔类型 * 配置突出显示标签 * 突出显示所有字段 * 合并多个字段上的匹配项 * 显式排序突出显示的字段 * 控制突出显示的片段 * 使用帖子列表突出显示 * 为普通荧光笔指定碎片

## 覆盖全局设置

您可以全局指定荧光笔设置，并有选择地覆盖各个字段的荧光笔设置。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          number_of_fragments: 3,
          fragment_size: 150,
          fields: {
            body: {
              pre_tags: [
                '<em>'
              ],
              post_tags: [
                '</em>'
              ]
            },
            "blog.title": {
              number_of_fragments: 0
            },
            "blog.author": {
              number_of_fragments: 0
            },
            "blog.comment": {
              number_of_fragments: 5,
              order: 'score'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "number_of_fragments" : 3,
        "fragment_size" : 150,
        "fields" : {
          "body" : { "pre_tags" : ["<em>"], "post_tags" : ["</em>"] },
          "blog.title" : { "number_of_fragments" : 0 },
          "blog.author" : { "number_of_fragments" : 0 },
          "blog.comment" : { "number_of_fragments" : 5, "order" : "score" }
        }
      }
    }

## 指定突出显示查询

您可以指定一个"highlight_query"，以便在突出显示时考虑其他信息。例如，以下查询在"highlight_query"中同时包含搜索查询和重新评分查询。如果没有"highlight_query"，突出显示只会考虑搜索查询。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            comment: {
              query: 'foo bar'
            }
          }
        },
        rescore: {
          window_size: 50,
          query: {
            rescore_query: {
              match_phrase: {
                comment: {
                  query: 'foo bar',
                  slop: 1
                }
              }
            },
            rescore_query_weight: 10
          }
        },
        _source: false,
        highlight: {
          order: 'score',
          fields: {
            comment: {
              fragment_size: 150,
              number_of_fragments: 3,
              highlight_query: {
                bool: {
                  must: {
                    match: {
                      comment: {
                        query: 'foo bar'
                      }
                    }
                  },
                  should: {
                    match_phrase: {
                      comment: {
                        query: 'foo bar',
                        slop: 1,
                        boost: 10
                      }
                    }
                  },
                  minimum_should_match: 0
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
          "comment": {
            "query": "foo bar"
          }
        }
      },
      "rescore": {
        "window_size": 50,
        "query": {
          "rescore_query": {
            "match_phrase": {
              "comment": {
                "query": "foo bar",
                "slop": 1
              }
            }
          },
          "rescore_query_weight": 10
        }
      },
      "_source": false,
      "highlight": {
        "order": "score",
        "fields": {
          "comment": {
            "fragment_size": 150,
            "number_of_fragments": 3,
            "highlight_query": {
              "bool": {
                "must": {
                  "match": {
                    "comment": {
                      "query": "foo bar"
                    }
                  }
                },
                "should": {
                  "match_phrase": {
                    "comment": {
                      "query": "foo bar",
                      "slop": 1,
                      "boost": 10.0
                    }
                  }
                },
                "minimum_should_match": 0
              }
            }
          }
        }
      }
    }

## 设置荧光笔类型

"类型"字段允许强制使用特定的荧光笔类型。允许的值为："统一"、"普通"和"fvh"。下面是强制使用普通荧光笔的示例：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          fields: {
            comment: {
              type: 'plain'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match": { "user.id": "kimchy" }
      },
      "highlight": {
        "fields": {
          "comment": { "type": "plain" }
        }
      }
    }

## 配置突出显示标签

默认情况下，突出显示会将突出显示的文本换行在""<em>和""</em>中。这可以通过设置"pre_tags"和"post_tags"来控制，例如：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          pre_tags: [
            '<tag1>'
          ],
          post_tags: [
            '</tag1>'
          ],
          fields: {
            body: {}
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "pre_tags" : ["<tag1>"],
        "post_tags" : ["</tag1>"],
        "fields" : {
          "body" : {}
        }
      }
    }

使用快速矢量荧光笔时，您可以指定其他标签，并对"重要性"进行排序。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          pre_tags: [
            '<tag1>',
            '<tag2>'
          ],
          post_tags: [
            '</tag1>',
            '</tag2>'
          ],
          fields: {
            body: {}
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
          "body" : {}
        }
      }
    }

您还可以使用内置的"样式化"标记架构：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          tags_schema: 'styled',
          fields: {
            comment: {}
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "tags_schema" : "styled",
        "fields" : {
          "comment" : {}
        }
      }
    }

## 在所有字段中突出显示

默认情况下，仅突出显示包含查询匹配项的字段。将"require_field_match"设置为"false"以突出显示所有字段。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          require_field_match: false,
          fields: {
            body: {
              pre_tags: [
                '<em>'
              ],
              post_tags: [
                '</em>'
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "require_field_match": false,
        "fields": {
          "body" : { "pre_tags" : ["<em>"], "post_tags" : ["</em>"] }
        }
      }
    }

## 合并多个字段上的匹配项

这仅由"fvh"荧光笔支持

快速矢量荧光笔可以组合多个字段上的匹配项以突出显示单个字段。这对于以不同方式分析同一字符串的多字段来说是最直观的。所有"matched_fields"都必须将"term_vector"设置为"with_positions_offsets"，但仅加载组合匹配项的字段，因此只有该字段才能从将"store"设置为"yes"中受益。

在以下示例中，"注释"由"英语"分析器分析，"comment.plain"由"标准"分析器分析。

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            query: 'comment.plain:running scissors',
            fields: [
              'comment'
            ]
          }
        },
        highlight: {
          order: 'score',
          fields: {
            comment: {
              matched_fields: [
                'comment',
                'comment.plain'
              ],
              type: 'fvh'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "query": "comment.plain:running scissors",
          "fields": [ "comment" ]
        }
      },
      "highlight": {
        "order": "score",
        "fields": {
          "comment": {
            "matched_fields": [ "comment", "comment.plain" ],
            "type": "fvh"
          }
        }
      }
    }

以上匹配"用剪刀跑步"和"用剪刀跑步"，并且会突出显示"跑步"和"剪刀"而不是"跑步"。如果两个短语都出现在一个大文档中，那么"用剪刀运行"在片段列表中排序在"用剪刀运行"之上，因为该片段中有更多的匹配项。

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            query: 'running scissors',
            fields: [
              'comment',
              'comment.plain^10'
            ]
          }
        },
        highlight: {
          order: 'score',
          fields: {
            comment: {
              matched_fields: [
                'comment',
                'comment.plain'
              ],
              type: 'fvh'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "query": "running scissors",
          "fields": ["comment", "comment.plain^10"]
        }
      },
      "highlight": {
        "order": "score",
        "fields": {
          "comment": {
            "matched_fields": ["comment", "comment.plain"],
            "type" : "fvh"
          }
        }
      }
    }

上面突出显示了"跑步"以及"跑步"和"剪刀"，但仍然将"用剪刀跑步"排序在"用剪刀跑步"之上，因为普通匹配("跑步")得到了提升。

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            query: 'running scissors',
            fields: [
              'comment',
              'comment.plain^10'
            ]
          }
        },
        highlight: {
          order: 'score',
          fields: {
            comment: {
              matched_fields: [
                'comment.plain'
              ],
              type: 'fvh'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "query": "running scissors",
          "fields": [ "comment", "comment.plain^10" ]
        }
      },
      "highlight": {
        "order": "score",
        "fields": {
          "comment": {
            "matched_fields": [ "comment.plain" ],
            "type": "fvh"
          }
        }
      }
    }

上面的查询不会突出显示"run"或"剪刀"，但表明在匹配的字段中不列出匹配项组合到的字段("注释")是可以的。

从技术上讲，也可以将字段添加到"matched_fields"中，这些字段与匹配项组合到的字段不共享相同的基础字符串。结果可能没有多大意义，如果其中一个匹配项不在文本末尾，则整个查询将失败。

将"matched_fields"设置为非空数组涉及少量开销，因此始终首选

    
    
        "highlight": {
            "fields": {
                "comment": {}
            }
        }

to

    
    
        "highlight": {
            "fields": {
                "comment": {
                    "matched_fields": ["comment"],
                    "type" : "fvh"
                }
            }
        }

## 显式排序突出显示的字段

Elasticsearch按发送顺序突出显示字段，但根据JSON规范，对象是无序的。如果您需要明确字段突出显示的顺序，请将"字段"指定为数组：

    
    
    response = client.search(
      body: {
        highlight: {
          fields: [
            {
              title: {}
            },
            {
              text: {}
            }
          ]
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "highlight": {
        "fields": [
          { "title": {} },
          { "text": {} }
        ]
      }
    }

Elasticsearch内置的荧光笔都不关心字段突出显示的顺序，但插件可能会。

## 控件突出显示的片段

突出显示的每个字段都可以控制突出显示的片段字符的大小(默认为"100")和要返回的最大片段数(默认为"5")。例如：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          fields: {
            comment: {
              fragment_size: 150,
              number_of_fragments: 3
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "fields" : {
          "comment" : {"fragment_size" : 150, "number_of_fragments" : 3}
        }
      }
    }

最重要的是，可以指定突出显示的片段需要按分数排序：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          order: 'score',
          fields: {
            comment: {
              fragment_size: 150,
              number_of_fragments: 3
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "order" : "score",
        "fields" : {
          "comment" : {"fragment_size" : 150, "number_of_fragments" : 3}
        }
      }
    }

如果"number_of_fragments"值设置为"0"，则不会生成片段，而是返回字段的全部内容，当然也会突出显示。如果需要突出显示短文本(如文档标题或地址)但不需要碎片，这将非常方便。请注意，在这种情况下，将忽略"fragment_size"。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          fields: {
            body: {},
            "blog.title": {
              number_of_fragments: 0
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query" : {
        "match": { "user.id": "kimchy" }
      },
      "highlight" : {
        "fields" : {
          "body" : {},
          "blog.title" : {"number_of_fragments" : 0}
        }
      }
    }

使用"fvh"时，可以使用"fragment_offset"参数来控制边距以开始突出显示。

如果没有要突出显示的匹配片段，则默认值为不返回任何内容。相反，我们可以通过将"no_match_size"(默认为"0")设置为要返回的文本长度，从字段开头返回一段文本。实际长度可能比指定的长度短或长，因为它试图在单词边界上中断。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        highlight: {
          fields: {
            comment: {
              fragment_size: 150,
              number_of_fragments: 3,
              no_match_size: 150
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match": { "user.id": "kimchy" }
      },
      "highlight": {
        "fields": {
          "comment": {
            "fragment_size": 150,
            "number_of_fragments": 3,
            "no_match_size": 150
          }
        }
      }
    }

## 使用帖子列表突出显示

下面是在索引映射中设置"注释"字段的示例，以允许使用帖子突出显示：

    
    
    response = client.indices.create(
      index: 'example',
      body: {
        mappings: {
          properties: {
            comment: {
              type: 'text',
              index_options: 'offsets'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /example
    {
      "mappings": {
        "properties": {
          "comment" : {
            "type": "text",
            "index_options" : "offsets"
          }
        }
      }
    }

下面是设置"注释"字段以允许突出显示使用"term_vectors"的示例(这将导致索引变大)：

    
    
    response = client.indices.create(
      index: 'example',
      body: {
        mappings: {
          properties: {
            comment: {
              type: 'text',
              term_vector: 'with_positions_offsets'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /example
    {
      "mappings": {
        "properties": {
          "comment" : {
            "type": "text",
            "term_vector" : "with_positions_offsets"
          }
        }
      }
    }

## 为普通荧光笔指定碎片器

使用"普通"荧光笔时，您可以在"简单"和"跨度"碎片之间进行选择：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match_phrase: {
            message: 'number 1'
          }
        },
        highlight: {
          fields: {
            message: {
              type: 'plain',
              fragment_size: 15,
              number_of_fragments: 3,
              fragmenter: 'simple'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match_phrase": { "message": "number 1" }
      },
      "highlight": {
        "fields": {
          "message": {
            "type": "plain",
            "fragment_size": 15,
            "number_of_fragments": 3,
            "fragmenter": "simple"
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.6011951,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "1",
            "_score": 1.6011951,
            "_source": {
              "message": "some message with the number 1",
              "context": "bar"
            },
            "highlight": {
              "message": [
                " with the <em>number</em>",
                " <em>1</em>"
              ]
            }
          }
        ]
      }
    }
    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match_phrase: {
            message: 'number 1'
          }
        },
        highlight: {
          fields: {
            message: {
              type: 'plain',
              fragment_size: 15,
              number_of_fragments: 3,
              fragmenter: 'span'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match_phrase": { "message": "number 1" }
      },
      "highlight": {
        "fields": {
          "message": {
            "type": "plain",
            "fragment_size": 15,
            "number_of_fragments": 3,
            "fragmenter": "span"
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.6011951,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "1",
            "_score": 1.6011951,
            "_source": {
              "message": "some message with the number 1",
              "context": "bar"
            },
            "highlight": {
              "message": [
                " with the <em>number</em> <em>1</em>"
              ]
            }
          }
        ]
      }
    }

如果"number_of_fragments"选项设置为"0"，则使用"NullFragmenter"这根本不会对文本进行碎片化。这对于突出显示文档或字段的全部内容非常有用。

## 荧光笔如何在内部工作

给定查询和文本(文档字段的内容)，ahighlight 的目标是查找查询的最佳文本片段，并突出显示找到的片段中的查询词。为此，荧光笔需要解决几个问题：

* 如何将文本分解成片段？  * 如何在所有片段中找到最好的片段？  * 如何突出显示片段中的查询词？

### 如何将文本分解为片段？

相关设置："fragment_size"、"碎片"、"荧光笔类型"、"boundary_chars"、"boundary_max_scan"、"boundary_scanner"、"boundary_scanner_locale"。

普通荧光笔首先使用给定的分析器分析文本，并从中创建令牌流。普通荧光笔使用非常简单的算法将令牌流分解为片段。它遍历令牌流中的术语，每次当前术语的end_offset超过"fragment_size"乘以创建的片段数时，就会创建一个新的片段。使用"span"碎片器可以完成更多的计算，以避免在突出显示的术语之间分解文本。但总的来说，由于中断仅由"fragment_size"完成，因此某些片段可能非常奇怪，例如以标点符号开头。

统一或FVH荧光笔通过使用Java的"BreakIterator"可以更好地将文本分解为片段。这确保了只要"fragment_size"允许，片段就是有效的句子。

### 如何找到最好的片段？

相关设置："number_of_fragments"。

为了找到最佳、最相关的片段，荧光笔需要根据给定查询对每个片段进行评分。目标是仅对那些参与生成文档上的 _hit_ 的术语进行评分。对于一些复杂的查询，这项工作仍在进行中。

普通荧光笔从当前令牌流创建内存中索引，并通过 Lucene 的查询执行计划器重新运行原始查询条件，以访问当前文本的低级匹配信息。对于更复杂的查询，可以将原始查询转换为 spanquery，因为 span 查询可以更准确地处理短语。然后，这些获得的低级匹配信息用于对每个单独的片段进行评分。普通荧光笔的评分方法非常简单。每个片段都按在此片段中找到的唯一查询词的数量进行评分。单个术语的分数等于其提升，默认情况下为 1。因此，默认情况下，包含一个唯一查询词的片段将获得 1 分;包含两个唯一查询词的片段将获得 2 分等。然后按分数对片段进行排序，因此将首先输出得分最高的片段。

FVH 不需要分析文本并构建内存中索引，因为它使用预先编制索引的文档术语向量，并在其中查找与查询对应的术语。FVH 根据在此片段中找到的查询词数对每个片段进行评分。与普通荧光笔类似，单个术语的分数等于其提升值。与普通荧光笔相比，将计算所有查询字词，而不仅仅是唯一字词。

统一荧光笔可以使用预先编制索引的术语向量或预先编制索引的术语偏移量(如果可用)。否则，与普通荧光笔类似，它必须从文本创建内存中索引。统一荧光笔使用 BM25 评分模型对片段进行评分。

### 如何在片段中突出显示查询词？

相关设置："前标签"、"后标签"。

目标是仅突出显示那些参与生成文档the_hit_的术语。对于一些复杂的布尔查询，这仍然是正在进行的工作，因为荧光笔不反映查询的布尔逻辑，并且只提取叶(术语、短语、前缀等)查询。

给定令牌流和原始文本的纯荧光笔将重构原始文本，以仅突出显示上一步中低级别匹配信息结构中包含的令牌流中的术语。

FVH 和统一荧光笔使用中间数据结构以某种原始形式表示片段，然后用实际文本填充它们。

荧光笔使用"前标记"、"后标记"对突出显示的术语进行编码。

### 统一荧光笔的工作示例

让我们更详细地了解统一荧光笔的工作原理。

首先，我们创建一个带有文本字段"content"的索引，该索引将使用"英语"分析器进行索引，并且将在没有偏移量或术语向量的情况下进行索引。

    
    
    PUT test_index
    {
      "mappings": {
        "properties": {
          "content": {
            "type": "text",
            "analyzer": "english"
          }
        }
      }
    }

我们将以下文档放入索引中：

    
    
    PUT test_index/_doc/doc1
    {
      "content" : "For you I'm only a fox like a hundred thousand other foxes. But if you tame me, we'll need each other. You'll be the only boy in the world for me. I'll be the only fox in the world for you."
    }

我们使用突出显示请求运行了以下查询：

    
    
    GET test_index/_search
    {
      "query": {
        "match_phrase" : {"content" : "only fox"}
      },
      "highlight": {
        "type" : "unified",
        "number_of_fragments" : 3,
        "fields": {
          "content": {}
        }
      }
    }

找到"doc1"作为此查询的命中后，此命中将传递到统一荧光笔，以突出显示文档的"内容"字段。由于字段"content"既没有使用偏移量也没有使用术语向量进行索引，因此将分析其原始字段值，并从与查询匹配的术语构建内存中索引：

    
    
    {"token":"onli","start_offset":12,"end_offset":16,"position":3},
    {"token":"fox","start_offset":19,"end_offset":22,"position":5},
    {"token":"fox","start_offset":53,"end_offset":58,"position":11},
    {"token":"onli","start_offset":117,"end_offset":121,"position":24},
    {"token":"onli","start_offset":159,"end_offset":163,"position":34},
    {"token":"fox","start_offset":164,"end_offset":167,"position":35}

我们的复杂短语查询将被转换为span查询：'spanNear([text：onli， text：fox]， 0， true)'，这意味着我们要查找彼此相距0 以内的术语 "onli： 和 "fox"，并且按给定顺序排列。span 查询将针对之前创建的内存中索引运行，以查找以下匹配项：

    
    
    {"term":"onli", "start_offset":159, "end_offset":163},
    {"term":"fox", "start_offset":164, "end_offset":167}

在我们的示例中，我们有一个匹配项，但可能有多个匹配项。给定匹配项，统一荧光笔将字段的文本分解为所谓的"段落"。每个段落必须至少包含一个匹配项。使用Java的"BreakIterator"的统一荧光笔确保每个段落代表一个完整的句子，只要它不超过"fragment_size"。对于我们的示例，我们得到了一个具有以下属性的段落(此处仅显示属性的子集)：

    
    
    Passage:
        startOffset: 147
        endOffset: 189
        score: 3.7158387
        matchStarts: [159, 164]
        matchEnds: [163, 167]
        numMatches: 2

请注意段落如何具有分数，该分数使用适用于段落的 BM25 评分公式计算得出。分数允许我们在可用的段落多于用户要求的段落时选择最佳评分段落number_of_fragments。分数还允许我们按"顺序："分数"对段落进行排序，如果用户要求。

作为最后一步，统一荧光笔将从字段的文本中提取对应于每个段落的字符串：

    
    
    "I'll be the only fox in the world for you."

并将使用段落的"matchStarts"和"matchEnds"信息格式化此字符串中的标签<em>和</em>所有匹配项：

    
    
    I'll be the <em>only</em> <em>fox</em> in the world for you.

这种格式化字符串是荧光笔返回给用户的最终结果。

[« Filter search results](filter-search-results.md) [Long-running searches
»](async-search-intro.md)
