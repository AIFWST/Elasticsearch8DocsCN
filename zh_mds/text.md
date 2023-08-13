

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Shape field type](shape.md) [Token count field type »](token-count.md)

## 文本类型族

文本系列包括以下字段类型：

* "text"，全文内容的传统字段类型，例如电子邮件正文或产品描述。  * "match_only_text"，一种空间优化的"文本"变体，可禁用评分，并在需要位置的查询上执行较慢的速度。它最适合为日志消息编制索引。

### 文本字段类型

用于索引全文值的字段，例如电子邮件正文或产品说明。这些字段被"分析"，即它们通过分析器传递，在编制索引之前将字符串转换为单个术语的列表。分析过程允许 Elasticsearch 在每个完整文本字段中搜索单个单词。文本字段不用于排序，也很少用于聚合(尽管重要的文本聚合是一个值得注意的例外)。

"文本"字段最适合非结构化但人类可读的内容。如果需要为非结构化计算机生成的内容编制索引，请参阅映射非结构化内容。

如果您需要索引结构化内容，例如电子邮件地址、主机名、状态代码或标签，则可能应该使用"关键字"字段。

下面是文本字段的映射示例：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            full_name: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "full_name": {
            "type":  "text"
          }
        }
      }
    }

### 将字段用作文本和关键字

有时，同时具有同一字段的全文("文本")和关键字("关键字")版本很有用：一个用于全文搜索，另一个用于聚合和排序。这可以通过多字段来实现。

### 文本字段的参数

"文本"字段接受以下参数：

"分析器"

|

应在索引时和搜索时用于"文本"字段的分析器(除非被"search_analyzer"覆盖)。默认为默认索引分析器或"标准"分析器。   ---|--- "eager_global_ordinals"

|

刷新时是否应该急切地加载全局序数？接受"真"或"假"(默认值)。在经常用于(重要)术语聚合的字段上启用此功能是一个好主意。   "现场数据"

|

字段是否可以使用内存中的字段数据进行排序、聚合或编写脚本？接受"真"或"假"(默认值)。   "fielddata_frequency_filter"

|

专家设置，允许决定在启用"字段数据"时在内存中加载哪些值。默认情况下，将加载所有值。   "字段"

|

多字段允许以多种方式为同一字符串值编制索引以实现不同的目的，例如一个字段用于搜索，多字段用于排序和聚合，或者由不同的分析器分析相同的字符串值。   "索引"

|

该字段是否应可搜索？接受"真"(默认值)或"假"。   "index_options"

|

索引中应存储哪些信息，以便进行搜索和突出显示。默认为"仓位"。   "index_prefixes"

|

如果启用，则 2 到 5 个字符之间的术语前缀将索引到单独的字段中。这允许前缀搜索更有效地运行，但代价是更大的索引。   "index_phrases"

|

如果启用，两个术语组合 ( _s带状疱疹_ ) 将被索引到一个单独的字段中。这允许精确短语查询(无 slop)更有效地运行，但代价是更大的索引。请注意，这在不删除停用词时效果最佳，因为包含非索引字的短语将不会使用附属字段，而是将回退到标准短语查询。接受"真"或"假"(默认值)。   "规范"

|

对查询进行评分时是否应考虑字段长度。接受"真"(默认值)或"假"。   "position_increment_gap"

|

应在字符串数组的每个元素之间插入的假术语位置的数量。默认为分析器上配置的"position_increment_gap"，默认为"100"。之所以选择"100"，是因为它可以防止具有相当大的 slop(小于 100)的短语查询跨字段值匹配术语。   "商店"

|

字段值是否应与"_source"字段分开存储和检索。接受"真"或"假"(默认值)。   "search_analyzer"

|

应在搜索时使用的"分析器"在"文本"字段中。默认为"分析器"设置。   "search_quote_analyzer"

|

遇到短语时应在搜索时使用的"分析器"。默认为"search_analyzer"设置。   "相似性"

|

应使用哪种评分算法或_相似性_。默认为"BM25"。   "term_vector"

|

是否应为字段存储术语向量。默认为"否"。   "元"

|

有关字段的元数据。   ### 合成'_source'编辑

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

如果"文本"字段具有支持合成"_source"的"关键字"子字段，或者"文本"字段将"store"设置为"true"，则它们支持合成"_source"。无论哪种方式，它都可能没有"copy_to"。

如果使用子"关键字"字段，则值的排序方式与"关键字"字段的值排序方式相同。默认情况下，这意味着在删除重复项的情况下排序。所以：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            text: {
              type: 'text',
              fields: {
                raw: {
                  type: 'keyword'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        text: [
          'the quick brown fox',
          'the quick brown fox',
          'jumped over the lazy dog'
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "text": {
            "type": "text",
            "fields": {
              "raw": {
                "type": "keyword"
              }
            }
          }
        }
      }
    }
    PUT idx/_doc/1
    {
      "text": [
        "the quick brown fox",
        "the quick brown fox",
        "jumped over the lazy dog"
      ]
    }

将成为：

    
    
    {
      "text": [
        "jumped over the lazy dog",
        "the quick brown fox"
      ]
    }

对文本字段重新排序可能会影响短语和跨度查询。有关更多详细信息，请参阅有关"position_increment_gap"的讨论。您可以通过确保短语查询上的"slop"参数低于"position_increment_gap"来避免这种情况。这是默认值。

如果"文本"字段将"存储"设置为 true，则保留顺序和重复项。

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            text: {
              type: 'text',
              store: true
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        text: [
          'the quick brown fox',
          'the quick brown fox',
          'jumped over the lazy dog'
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "text": { "type": "text", "store": true }
        }
      }
    }
    PUT idx/_doc/1
    {
      "text": [
        "the quick brown fox",
        "the quick brown fox",
        "jumped over the lazy dog"
      ]
    }

将成为：

    
    
    {
      "text": [
        "the quick brown fox",
        "the quick brown fox",
        "jumped over the lazy dog"
      ]
    }

### '字段数据' 映射参数

默认情况下，"text"字段是可搜索的，但默认情况下不可用于聚合、排序或脚本编写。如果您尝试使用脚本对"文本"字段中的值进行排序、聚合或访问，您将看到一个异常，指示默认情况下在文本字段上禁用字段数据。要在内存中加载字段数据，请在字段上设置"字段数据=true"。

在内存中加载字段数据可能会消耗大量内存。

字段数据是从聚合、排序或脚本编写中的全文字段访问分析的令牌的唯一方法。例如，像"纽约"这样的全文字段将被分析为"新"和"约克"。在这些令牌上进行聚合需要字段数据。

### 启用字段数据之前

在文本字段上启用字段数据通常没有意义。字段数据与字段数据缓存一起存储在堆中，因为计算成本很高。计算字段数据可能会导致延迟峰值，而增加堆使用率是导致集群性能问题的原因。

大多数想要对文本字段执行更多操作的用户都使用多字段映射，同时具有用于全文搜索的"文本"字段和用于聚合的未分析的"关键字"字段，如下所示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_field: {
              type: 'text',
              fields: {
                keyword: {
                  type: 'keyword'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "my_field": {
    	        "type": "text",
    	        "fields": {
    	          "keyword": {
    	            "type": "keyword"
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "my_field": { __"type": "text",
            "fields": {
              "keyword": { __"type": "keyword"
              }
            }
          }
        }
      }
    }

__

|

使用"my_field"字段进行搜索。   ---|---    __

|

使用"my_field.关键字"字段进行聚合、排序或在脚本中。   ### 在"文本"字段编辑上启用字段数据

您可以使用更新映射 API 在现有"文本"字段上启用字段数据，如下所示：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          my_field: {
            type: 'text',
            fielddata: true
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.PutMapping(
    	[]string{"my-index-000001"},
    	strings.NewReader(`{
    	  "properties": {
    	    "my_field": {
    	      "type": "text",
    	      "fielddata": true
    	    }
    	  }
    	}`),
    )
    fmt.Println(res, err)
    
    
    PUT my-index-000001/_mapping
    {
      "properties": {
        "my_field": { __"type":     "text",
          "fielddata": true
        }
      }
    }

__

|

您为"my_field"指定的映射应包含该字段的现有映射以及"字段数据"参数。   ---|--- ### 'fielddata_frequency_filter' 映射参数编辑

字段数据过滤可用于减少加载到内存中的术语数，从而减少内存使用量。术语可以按 _频率_ 过滤：

频率过滤器允许您仅加载文档频率介于"最小"和"最大"值之间的术语，该值可以表示为绝对数(当数字大于 1.0 时)或百分比(例如"0.01"是"1%"和"1.0"是"100%")。频率按每段计算。百分比基于具有字段值的文档数量，而不是细分中的所有文档。

可以通过使用"min_segment_size"指定细分应包含的最小文档数来完全排除小段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            tag: {
              type: 'text',
              fielddata: true,
              fielddata_frequency_filter: {
                min: 0.001,
                max: 0.1,
                min_segment_size: 500
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "tag": {
    	        "type": "text",
    	        "fielddata": true,
    	        "fielddata_frequency_filter": {
    	          "min": 0.001,
    	          "max": 0.1,
    	          "min_segment_size": 500
    	        }
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "tag": {
            "type": "text",
            "fielddata": true,
            "fielddata_frequency_filter": {
              "min": 0.001,
              "max": 0.1,
              "min_segment_size": 500
            }
          }
        }
      }
    }

### 仅匹配文本字段类型

"文本"的一种变体，用于权衡位置查询的评分和效率以获得空间效率。此字段有效地存储数据的方式与仅索引文档("index_options：文档")和禁用规范("规范：假")的"文本"字段相同。术语查询的执行速度与"文本"字段一样快，如果不是更快的话，但是需要诸如"match_phrase"查询之类的位置的查询执行速度较慢，因为它们需要查看"_source"文档以验证短语是否匹配。所有查询都返回等于 1.0 的常量分数。

分析不可配置：始终使用默认分析器(默认为"标准")分析文本。

此字段不支持跨度查询，请改用间隔查询，或者如果您绝对需要跨度查询，则使用"文本"字段类型。

除此之外，"match_only_text"支持与"文本"相同的查询。与"文本"一样，它不支持排序，并且仅对聚合提供有限的支持。

    
    
    response = client.indices.create(
      index: 'logs',
      body: {
        mappings: {
          properties: {
            "@timestamp": {
              type: 'date'
            },
            message: {
              type: 'match_only_text'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT logs
    {
      "mappings": {
        "properties": {
          "@timestamp": {
            "type": "date"
          },
          "message": {
            "type": "match_only_text"
          }
        }
      }
    }

#### 仅匹配文本字段的参数

接受以下映射参数：

"字段"

|

多字段允许以多种方式为同一字符串值编制索引以实现不同的目的，例如一个字段用于搜索，多字段用于排序和聚合，或者由不同的分析器分析相同的字符串值。   ---|--- "元"

|

有关字段的元数据。   « 形状字段类型 令牌计数字段类型 »