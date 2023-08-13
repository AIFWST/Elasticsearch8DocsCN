

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md)

[« Field extraction](scripting-field-extraction.md) [Scripting and security
»](modules-scripting-security.md)

## 访问文档字段和特殊变量

根据脚本的使用位置，它将有权访问某些特殊变量和文档字段。

## 更新脚本

更新、按查询更新或重新索引 API 中使用的脚本将有权访问"ctx"变量，该变量公开：

`ctx._source`

|

访问文档"_source"字段。   ---|--- 'ctx.op'

|

应应用于文档的操作："索引"或"删除"。   "ctx._index"等

|

访问文档元数据字段，其中一些可能是只读的。   这些脚本无法访问"doc"变量，必须使用"ctx"来访问它们操作的文档。

## 搜索和聚合脚本

除了每次搜索命中执行一次的脚本字段外，搜索和聚合中使用的脚本将针对可能与查询或聚合匹配的每个文档执行一次。根据您拥有的文档数量，这可能意味着数百万或数十亿次执行：这些脚本需要快速！

可以使用文档值、"_source"字段或存储字段从脚本访问字段值，下面将逐一说明。

### 在脚本中访问文档的分数

在"function_score"查询、基于脚本的排序或聚合中使用的脚本可以访问表示文档当前相关性分数的"_score"变量。

下面是在"function_score"查询中使用脚本更改每个文档的相关性"_score"的示例：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        text: 'quick brown fox',
        popularity: 1
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      refresh: true,
      body: {
        text: 'quick fox',
        popularity: 5
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          function_score: {
            query: {
              match: {
                text: 'quick brown fox'
              }
            },
            script_score: {
              script: {
                lang: 'expression',
                source: "_score * doc['popularity']"
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "text": "quick brown fox",
      "popularity": 1
    }
    
    PUT my-index-000001/_doc/2?refresh
    {
      "text": "quick fox",
      "popularity": 5
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "function_score": {
          "query": {
            "match": {
              "text": "quick brown fox"
            }
          },
          "script_score": {
            "script": {
              "lang": "expression",
              "source": "_score * doc['popularity']"
            }
          }
        }
      }
    }

### 文档值

到目前为止，从脚本访问字段值的最快最有效的方法是使用"doc'field_name']"语法，该语法从[doc values.文档值是一个列式字段值存储，默认情况下在除分析的"文本"字段之外的所有字段上启用。

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        cost_price: 100
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        script_fields: {
          sales_price: {
            script: {
              lang: 'expression',
              source: "doc['cost_price'] * markup",
              params: {
                markup: 0.2
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "cost_price": 100
    }
    
    GET my-index-000001/_search
    {
      "script_fields": {
        "sales_price": {
          "script": {
            "lang":   "expression",
            "source": "doc['cost_price'] * markup",
            "params": {
              "markup": 0.2
            }
          }
        }
      }
    }

文档值只能返回"简单"字段值，如数字、日期、地理点、术语等，或者如果字段是多值的，则这些值的数组。它不能返回 JSON 对象。

### 缺少字段

如果映射中缺少"字段"，则"doc["字段"]"将引发错误。在"无痛"中，可以首先使用"doc.containsKey('field')"进行检查，以保护访问"doc"映射。不幸的是，无法在"表达式"脚本的映射中检查字段是否存在。

### 文档值和"文本"字段

"doc'field']"语法也可用于[如果启用了"fielddata"则分析的"文本"字段，但是**请注意**：在"文本"字段上启用字段数据需要将所有术语加载到JVM堆中，这在内存和CPU方面都非常昂贵。从脚本访问"文本"字段很少有意义。

### 文档"_source"

可以使用"_source.field_name"语法访问文档"_source"。"_source"作为地图的地图加载，因此可以像"_source.name.first"一样访问对象字段中的属性。

### 首选文档值而不是_source

访问"_source"字段比使用文档值慢得多。The_source字段经过优化，为每个结果返回多个字段，而文档值则针对访问许多文档中特定字段的值进行了优化。

在为搜索结果中的前十次点击生成脚本字段时，使用"_source"是有意义的，但对于其他搜索和聚合用例，始终更喜欢使用doc值。

例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            first_name: {
              type: 'text'
            },
            last_name: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        first_name: 'Barry',
        last_name: 'White'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        script_fields: {
          full_name: {
            script: {
              lang: 'painless',
              source: "params._source.first_name + ' ' + params._source.last_name"
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
          "first_name": {
            "type": "text"
          },
          "last_name": {
            "type": "text"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1?refresh
    {
      "first_name": "Barry",
      "last_name": "White"
    }
    
    GET my-index-000001/_search
    {
      "script_fields": {
        "full_name": {
          "script": {
            "lang": "painless",
            "source": "params._source.first_name + ' ' + params._source.last_name"
          }
        }
      }
    }

### 存储字段

_Stored fields_ - 在映射中明确标记为"存储"：true的字段 - 可以使用"_fields["field_name".value"或"_fields["field_name"]"语法访问：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            full_name: {
              type: 'text',
              store: true
            },
            title: {
              type: 'text',
              store: true
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        full_name: 'Alice Ball',
        title: 'Professor'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        script_fields: {
          name_with_title: {
            script: {
              lang: 'painless',
              source: "params._fields['title'].value + ' ' + params._fields['full_name'].value"
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
            "type": "text",
            "store": true
          },
          "title": {
            "type": "text",
            "store": true
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1?refresh
    {
      "full_name": "Alice Ball",
      "title": "Professor"
    }
    
    GET my-index-000001/_search
    {
      "script_fields": {
        "name_with_title": {
          "script": {
            "lang": "painless",
            "source": "params._fields['title'].value + ' ' + params._fields['full_name'].value"
          }
        }
      }
    }

### 存储与"_source"

"_source"字段只是一个特殊的存储字段，因此性能与其他存储字段相似。"_source"提供对已编制索引的原始文档正文的访问(包括区分"null"值与空字段、单值数组与纯标量等的能力)。

使用存储字段而不是"_source"字段真正有意义的唯一情况是当"_source"非常大并且访问几个小存储字段而不是整个"_source"的成本更低时。

[« Field extraction](scripting-field-extraction.md) [Scripting and security
»](modules-scripting-security.md)
