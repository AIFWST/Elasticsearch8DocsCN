

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Terms query](query-dsl-terms-query.md) [Wildcard query »](query-dsl-
wildcard-query.md)

## 术语集查询

返回在提供的字段中包含最小数量的**精确**术语的文档。

"terms_set"查询与"terms"查询相同，只是您可以定义返回文档所需的匹配术语数。例如：

* 字段"programming_languages"包含已知编程语言的列表，例如求职者的"c++"、"java"或"php"。您可以使用"terms_set"查询返回至少与其中两种语言匹配的文档。  * 字段"权限"包含应用程序可能的用户权限列表。可以使用"terms_set"查询返回与这些权限的子集匹配的文档。

### 示例请求

#### 索引设置

在大多数情况下，您需要在索引中包含数值字段映射才能使用"terms_set"查询。此数字字段包含返回文档所需的匹配术语数。

若要了解如何为"terms_set"查询设置索引，请尝试以下示例。

1. 使用以下字段映射创建索引"求职者"：

    * `name`, a [`keyword`](keyword.html "Keyword type family") field. This field contains the name of the job candidate. 
    * `programming_languages`, a [`keyword`](keyword.html "Keyword type family") field. This field contains programming languages known by the job candidate. 
    * `required_matches`, a [numeric](number.html "Numeric field types") `long` field. This field contains the number of matching terms required to return a document. 
    
        response = client.indices.create(
      index: 'job-candidates',
      body: {
        mappings: {
          properties: {
            name: {
              type: 'keyword'
            },
            programming_languages: {
              type: 'keyword'
            },
            required_matches: {
              type: 'long'
            }
          }
        }
      }
    )
    puts response
    
        PUT /job-candidates
    {
      "mappings": {
        "properties": {
          "name": {
            "type": "keyword"
          },
          "programming_languages": {
            "type": "keyword"
          },
          "required_matches": {
            "type": "long"
          }
        }
      }
    }

2. 为 ID 为"1"和以下值的文档编制索引：

    * `Jane Smith` in the `name` field. 
    * `["c++", "java"]` in the `programming_languages` field. 
    * `2` in the `required_matches` field. 

包括"？刷新"参数，以便文档立即可供搜索。

    
        PUT /job-candidates/_doc/1?refresh
    {
      "name": "Jane Smith",
      "programming_languages": [ "c++", "java" ],
      "required_matches": 2
    }

3. 索引另一个 ID 为"2"且值为以下的文档：

    * `Jason Response` in the `name` field. 
    * `["java", "php"]` in the `programming_languages` field. 
    * `2` in the `required_matches` field. 
    
        PUT /job-candidates/_doc/2?refresh
    {
      "name": "Jason Response",
      "programming_languages": [ "java", "php" ],
      "required_matches": 2
    }

现在，您可以使用"required_matches"字段值作为在"terms_set"查询中返回文档所需的匹配术语数。

#### 示例查询

以下搜索返回文档，其中"programming_languages"字段至少包含以下两个术语：

* 'C++' * 'Java' * 'php'

"minimum_should_match_field"是"required_matches"。这意味着所需的匹配字词数为"2"，即"required_matches"字段的值。

    
    
    response = client.search(
      index: 'job-candidates',
      body: {
        query: {
          terms_set: {
            programming_languages: {
              terms: [
                'c++',
                'java',
                'php'
              ],
              minimum_should_match_field: 'required_matches'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /job-candidates/_search
    {
      "query": {
        "terms_set": {
          "programming_languages": {
            "terms": [ "c++", "java", "php" ],
            "minimum_should_match_field": "required_matches"
          }
        }
      }
    }

### terms_set"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`terms`

    

(必需，字符串数组)您希望在提供的"'"中找到的术语数组<field>。要返回文档，所需数量的术语必须与字段值完全匹配，包括空格和大小写。

所需的匹配项数在"minimum_should_match_field"或"minimum_should_match_script"参数中定义。

`minimum_should_match_field`

     (Optional, string) [Numeric](number.html "Numeric field types") field containing the number of matching terms required to return a document. 
`minimum_should_match_script`

    

(可选，字符串)包含返回文档所需的匹配术语数的自定义脚本。

有关参数和有效值，请参阅脚本。

有关使用"minimum_should_match_script"参数的示例查询，请参阅如何使用"minimum_should_match_script"参数。

###Notes

#### 如何使用"minimum_should_match_script"参数

您可以使用"minimum_should_match_script"通过脚本定义所需数量的匹配术语。如果您需要动态设置所需术语的数量，这将非常有用。

##### 使用"minimum_should_match_script"的示例查询

以下搜索返回文档，其中"programming_languages"字段至少包含以下两个术语：

* 'C++' * 'Java' * 'php'

此查询的"源"参数指示：

* 匹配的所需术语数不能超过"params.num_terms"，即"条款"字段中提供的术语数。  * 所需的匹配术语数为"2"，即"required_matches"字段的值。

    
    
    response = client.search(
      index: 'job-candidates',
      body: {
        query: {
          terms_set: {
            programming_languages: {
              terms: [
                'c++',
                'java',
                'php'
              ],
              minimum_should_match_script: {
                source: "Math.min(params.num_terms, doc['required_matches'].value)"
              },
              boost: 1
            }
          }
        }
      }
    )
    puts response
    
    
    GET /job-candidates/_search
    {
      "query": {
        "terms_set": {
          "programming_languages": {
            "terms": [ "c++", "java", "php" ],
            "minimum_should_match_script": {
              "source": "Math.min(params.num_terms, doc['required_matches'].value)"
            },
            "boost": 1.0
          }
        }
      }
    }

[« Terms query](query-dsl-terms-query.md) [Wildcard query »](query-dsl-
wildcard-query.md)
