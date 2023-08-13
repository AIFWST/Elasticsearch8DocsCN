

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Retrieve inner hits](inner-hits.md) [Search across clusters »](modules-
cross-cluster-search.md)

## 从搜索中检索所选字段

默认情况下，搜索响应中的每个命中都包含文档"_source"，这是为文档编制索引时提供的完整 JSON 对象。有两种推荐的方法可以从搜索查询中检索所选字段：

* 使用"字段"选项提取索引映射中存在的字段值 * 如果您需要访问索引时传递的原始数据，请使用"_source"选项

您可以使用这两种方法，但首选"字段"选项，因为它同时查询文档数据和索引映射。在某些情况下，您可能希望使用其他方法来检索数据。

### "字段"选项

要检索搜索响应中的特定字段，请使用"fields"参数。由于它查询索引映射，因此与直接引用"_source"相比，"fields"参数具有几个优点。具体来说，"字段"参数：

* 以与其映射类型匹配的标准化方式返回每个值 * 接受多字段和字段别名 * 设置日期和空间数据类型的格式 * 检索运行时字段值 * 返回脚本在索引时计算的字段 * 使用查找运行时字段从相关索引返回字段

还考虑其他映射选项，包括"ignore_above"、"ignore_malformed"和"null_value"。

"fields"选项以与Elasticsearch索引它们的方式匹配的方式返回值。对于标准字段，这意味着"字段"选项在"_source"中查找值，然后使用映射解析和格式化它们。在"_source"中找不到的选定字段将被跳过。

#### 检索特定字段

以下搜索请求使用"fields"参数检索"user.id"字段、以"http.response."开头的所有字段和"@timestamp"字段的值。

使用对象表示法，可以传递"format"参数来自定义返回日期或地理空间值的格式。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        fields: [
          'user.id',
          'http.response.*',
          {
            field: '@timestamp',
            format: 'epoch_millis'
          }
        ],
        _source: false
      }
    )
    puts response
    
    
    POST my-index-000001/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      },
      "fields": [
        "user.id",
        "http.response.*",         __{
          "field": "@timestamp",
          "format": "epoch_millis" __}
      ],
      "_source": false
    }

__

|

接受完整字段名称和通配符模式。   ---|---    __

|

使用"format"参数为字段的值应用自定义格式。   默认情况下，当请求的"字段"选项使用通配符模式(如"*")时，不会返回"_id"或"_index"等文档元数据字段。但是，当使用字段名称显式请求时，可以检索"_id"、"_routing"、"_ignored"、"_index"和"_version"元数据字段。

#### 响应始终返回数组

"fields"响应始终为每个字段返回一个值数组，即使"_source"中只有一个值也是如此。这是因为 Elasticsearch 没有专用的数组类型，任何字段都可以包含多个值。"fields"参数也不保证按特定顺序返回数组值。有关更多背景信息，请参阅有关数组的映射文档。

响应在每次命中的"字段"部分中以平面列表的形式包含值。由于"fields"参数不会获取整个对象，因此仅返回叶字段。

    
    
    {
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "0",
            "_score" : 1.0,
            "fields" : {
              "user.id" : [
                "kimchy"
              ],
              "@timestamp" : [
                "4098435132000"
              ],
              "http.response.bytes": [
                1070000
              ],
              "http.response.status_code": [
                200
              ]
            }
          }
        ]
      }
    }

#### 检索嵌套字段

Details

"嵌套"字段的"字段"响应与常规对象字段的响应略有不同。常规"对象"字段中的叶值作为平面列表返回，而"嵌套"字段中的值则分组以保持原始嵌套数组中每个对象的独立性。对于嵌套字段数组中的每个条目，值将再次作为平面列表返回，除非父嵌套对象内还有其他"嵌套"字段，在这种情况下，将对更深的嵌套字段再次重复相同的过程。

给定以下映射，其中"user"是嵌套字段，在索引以下文档并检索"user"字段下的所有字段后：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            group: {
              type: 'keyword'
            },
            user: {
              type: 'nested',
              properties: {
                first: {
                  type: 'keyword'
                },
                last: {
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
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        group: 'fans',
        user: [
          {
            first: 'John',
            last: 'Smith'
          },
          {
            first: 'Alice',
            last: 'White'
          }
        ]
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          '*'
        ],
        _source: false
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "group" : { "type" : "keyword" },
          "user": {
            "type": "nested",
            "properties": {
              "first" : { "type" : "keyword" },
              "last" : { "type" : "keyword" }
            }
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1?refresh=true
    {
      "group" : "fans",
      "user" : [
        {
          "first" : "John",
          "last" :  "Smith"
        },
        {
          "first" : "Alice",
          "last" :  "White"
        }
      ]
    }
    
    POST my-index-000001/_search
    {
      "fields": ["*"],
      "_source": false
    }

响应将对"名字"和"姓氏"进行分组，而不是将它们作为平面列表返回。

    
    
    {
      "took": 2,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [{
          "_index": "my-index-000001",
          "_id": "1",
          "_score": 1.0,
          "fields": {
            "group" : ["fans"],
            "user": [{
                "first": ["John"],
                "last": ["Smith"]
              },
              {
                "first": ["Alice"],
                "last": ["White"]
              }
            ]
          }
        }]
      }
    }

嵌套字段将按其嵌套路径分组，无论用于检索它们的模式如何。例如，如果仅查询上一示例中的"user.first"字段：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          'user.first'
        ],
        _source: false
      }
    )
    puts response
    
    
    POST my-index-000001/_search
    {
      "fields": ["user.first"],
      "_source": false
    }

响应仅返回用户的名字，但仍保留嵌套"user"数组的结构：

    
    
    {
      "took": 2,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [{
          "_index": "my-index-000001",
          "_id": "1",
          "_score": 1.0,
          "fields": {
            "user": [{
                "first": ["John"]
              },
              {
                "first": ["Alice"]
              }
            ]
          }
        }]
      }
    }

但是，当"字段"模式直接针对嵌套的"用户"字段时，不会返回任何值，因为该模式与任何叶字段都不匹配。

#### 检索未映射的字段

Details

默认情况下，"fields"参数仅返回映射字段的值。但是，Elasticsearch 允许将未映射的字段存储在"_source"中，例如将动态字段映射设置为"false"或使用带有"enabled： false"的对象字段。这些选项禁用对象内容的分析和索引。

要从"_source"中检索对象中未映射的字段，请使用"字段"部分中的"include_unmapped"选项：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          enabled: false
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        user_id: 'kimchy',
        session_data: {
          object: {
            some_field: 'some_value'
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          'user_id',
          {
            field: 'session_data.object.*',
            include_unmapped: true
          }
        ],
        _source: false
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "enabled": false __}
    }
    
    PUT my-index-000001/_doc/1?refresh=true
    {
      "user_id": "kimchy",
      "session_data": {
         "object": {
           "some_field": "some_value"
         }
       }
    }
    
    POST my-index-000001/_search
    {
      "fields": [
        "user_id",
        {
          "field": "session_data.object.*",
          "include_unmapped" : true __}
      ],
      "_source": false
    }

__

|

禁用所有映射。   ---|---    __

|

包括与此字段模式匹配的未映射字段。   响应将包含"session_data.object.*"路径下的字段结果，即使字段未映射也是如此。"user_id"字段也是未映射的，但它不会包含在响应中，因为该字段模式的"include_unmapped"未设置为"true"。

    
    
    {
      "took" : 2,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "1",
            "_score" : 1.0,
            "fields" : {
              "session_data.object.some_field": [
                "some_value"
              ]
            }
          }
        ]
      }
    }

#### 忽略的字段值

Details

响应的"字段"部分仅返回在编制索引时有效的值。如果您的搜索请求请求从忽略某些值的字段中请求值，因为它们格式不正确或太大，这些值将在"ignored_field_values"部分中单独返回。

在此示例中，我们索引一个文档，该文档具有忽略且未添加到索引中的值，因此在搜索结果中单独显示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            "my-small": {
              type: 'keyword',
              ignore_above: 2
            },
            "my-large": {
              type: 'keyword'
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
        "my-small": [
          'ok',
          'bad'
        ],
        "my-large": 'ok content'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          'my-*'
        ],
        _source: false
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "my-small" : { "type" : "keyword", "ignore_above": 2 }, __"my-large" : { "type" : "keyword" }
        }
      }
    }
    
    PUT my-index-000001/_doc/1?refresh=true
    {
      "my-small": ["ok", "bad"], __"my-large": "ok content"
    }
    
    POST my-index-000001/_search
    {
      "fields": ["my-*"],
      "_source": false
    }

__

|

此字段的大小限制为 ---|--- __

|

此文档字段的值超过大小限制，因此被忽略且未编制索引 响应将在"ignored_field_values"路径下包含忽略的字段值。这些值是从文档的原始 JSON 源中检索的，并且是原始的，因此无论如何都不会格式化或处理，这与在"字段"部分中返回的成功索引字段不同。

    
    
    {
      "took" : 2,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "1",
            "_score" : 1.0,
            "_ignored" : [ "my-small"],
            "fields" : {
              "my-large": [
                "ok content"
              ],
              "my-small": [
                "ok"
              ]
            },
            "ignored_field_values" : {
              "my-small": [
                "bad"
              ]
            }
          }
        ]
      }
    }

### "_source"选项

您可以使用"_source"参数选择返回源的哪些字段。这称为_source filtering_。

以下搜索 API 请求将"_source"请求正文参数设置为"false"。响应中不包含文档源。

    
    
    response = client.search(
      body: {
        _source: false,
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "_source": false,
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

要仅返回源字段的子集，请在"_source"参数中指定通配符 ('*') 模式。以下搜索 API 请求仅返回"obj"字段及其属性的源。

    
    
    response = client.search(
      body: {
        _source: 'obj.*',
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "_source": "obj.*",
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

您还可以在"_source"字段中指定通配符模式数组。以下搜索 API 请求仅返回"obj1"和"obj2"字段及其属性的源。

    
    
    response = client.search(
      body: {
        _source: [
          'obj1.*',
          'obj2.*'
        ],
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "_source": [ "obj1.*", "obj2.*" ],
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

为了进行更精细的控制，您可以在"_source"参数中指定一个包含"包含"和"排除"模式数组的对象。

如果指定了"include"属性，则仅返回与其模式之一匹配的源字段。您可以使用"excludes"属性从此子集中排除字段。

如果未指定"include"属性，则返回整个文档源，排除与"excludes"属性中的模式匹配的任何字段。

以下搜索 API 请求仅返回"obj1"和"obj2"字段及其属性的源，不包括任何子"说明"字段。

    
    
    response = client.search(
      body: {
        _source: {
          includes: [
            'obj1.*',
            'obj2.*'
          ],
          excludes: [
            '*.description'
          ]
        },
        query: {
          term: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "_source": {
        "includes": [ "obj1.*", "obj2.*" ],
        "excludes": [ "*.description" ]
      },
      "query": {
        "term": {
          "user.id": "kimchy"
        }
      }
    }

### 其他检索数据的方法

**使用"字段"通常更好**

这些选项通常不是必需的。使用"字段"选项通常是更好的选择，除非您绝对需要强制加载存储的 or'docvalue_fields'。

文档的"_source"在 Lucene 中存储为单个字段。此结构意味着必须加载和解析整个"_source"对象，即使您只请求它的一部分。要避免此限制，您可以尝试其他选项来加载字段：

* 使用"docvalue_fields"参数获取所选字段的值。当返回支持文档值的相当少量的字段(如关键字和日期)时，这可能是一个不错的选择。  * 使用"stored_fields"参数获取特定存储字段(使用"存储"映射选项的字段)的值。

Elasticsearch总是尝试从'_source'加载值。这种行为与源过滤具有相同的含义，其中 Elasticsearch 需要加载和解析整个"_source"以仅检索一个字段。

#### 文档值字段

您可以使用"docvalue_fields"参数返回搜索响应中一个或多个字段的文档值。

文档值存储与"_source"相同的值，但存储在磁盘上基于列的结构中，该结构针对排序和聚合进行了优化。由于每个字段都是单独存储的，因此 Elasticsearch 只读取请求的字段值，并且可以避免加载整个文档"_source"。

默认情况下，为支持的字段存储文档值。但是，"文本"或"text_annotated"字段不支持文档值。

以下搜索请求使用"docvalue_fields"参数检索"user.id"字段、以"http.response."开头的所有字段和"@timestamp"字段的doc值：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        docvalue_fields: [
          'user.id',
          'http.response.*',
          {
            field: 'date',
            format: 'epoch_millis'
          }
        ]
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      },
      "docvalue_fields": [
        "user.id",
        "http.response.*", __{
          "field": "date",
          "format": "epoch_millis" __}
      ]
    }

__

|

接受完整字段名称和通配符模式。   ---|---    __

|

使用对象表示法，您可以传递"format"参数，为字段的文档值应用自定义格式。日期字段支持日期"格式"。数值字段支持 DecimalFormatpattern。其他字段数据类型不支持"format"参数。   不能使用"docvalue_fields"参数检索嵌套对象的文档值。如果指定嵌套对象，则搜索将返回该字段的空数组 (' ]')。若要访问嵌套字段，请使用 ['inner_hits' 参数的'docvalue_fields' 属性。

#### 存储字段

也可以使用"存储"映射选项存储单个字段的值。您可以使用"stored_fields"参数将这些存储的值包含在搜索响应中。

"stored_fields"参数用于映射中显式标记为存储的字段，默认情况下处于关闭状态，通常不建议使用。请改用源筛选来选择要返回的原始源文档的子集。

允许有选择地为每个文档加载特定的存储字段，由搜索命中表示。

    
    
    response = client.search(
      body: {
        stored_fields: [
          'user',
          'postDate'
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "stored_fields" : ["user", "postDate"],
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

"*"可用于从文档中加载所有存储的字段。

空数组将导致每次命中仅返回"_id"和"_type"，例如：

    
    
    response = client.search(
      body: {
        stored_fields: [],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "stored_fields" : [],
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

如果未存储请求的字段("store"映射设置为"false")，则它们将被忽略。

从文档本身获取的存储字段值始终以数组形式返回。相反，像"_routing"这样的元数据字段永远不会作为数组返回。

此外，只能通过"stored_fields"选项返回叶字段。如果指定了对象字段，则将忽略该字段。

就其本身而言，"stored_fields"不能用于加载嵌套对象中的字段 - 如果字段在其路径中包含嵌套对象，则不会返回该存储字段的数据。要访问嵌套字段，必须在"inner_hits"块中使用"stored_fields"。

##### 禁用存储字段

要完全禁用存储字段(和元数据字段)，请使用："_none_"：

    
    
    response = client.search(
      body: {
        stored_fields: '_none_',
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "stored_fields": "_none_",
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

如果使用"_none_"，则无法激活"_source"和"版本"参数。

#### 脚本字段

您可以使用"script_fields"参数检索每个命中的脚本评估(基于不同的字段)。例如：

    
    
    response = client.search(
      body: {
        query: {
          match_all: {}
        },
        script_fields: {
          "test1": {
            script: {
              lang: 'painless',
              source: "doc['price'].value * 2"
            }
          },
          "test2": {
            script: {
              lang: 'painless',
              source: "doc['price'].value * params.factor",
              params: {
                factor: 2
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
        "match_all": {}
      },
      "script_fields": {
        "test1": {
          "script": {
            "lang": "painless",
            "source": "doc['price'].value * 2"
          }
        },
        "test2": {
          "script": {
            "lang": "painless",
            "source": "doc['price'].value * params.factor",
            "params": {
              "factor": 2.0
            }
          }
        }
      }
    }

脚本字段可以处理未存储的字段(在上述情况下为"价格")，并允许返回要返回的自定义值(脚本的评估值)。

脚本字段还可以访问实际的"_source"文档，并使用"params[_source"]"提取要从中返回的特定元素。下面是一个例子：

    
    
    response = client.search(
      body: {
        query: {
          match_all: {}
        },
        script_fields: {
          "test1": {
            script: "params['_source']['message']"
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match_all": {}
      },
      "script_fields": {
        "test1": {
          "script": "params['_source']['message']"
        }
      }
    }

请注意此处的"_source"关键字以导航类似 json 的模型。

了解"doc['my_field'].value"和"params['_source']['my_field']"之间的区别很重要。第一个使用 doc 关键字，将导致将该字段的术语加载到内存(缓存)，这将导致更快的执行速度，但更多的内存消耗。此外，"文档[...]'notation 只允许简单的值字段(你不能从它返回 JSON 对象)，并且只对未分析或基于单个术语的字段有意义。但是，如果可能的话，使用"doc"仍然是从文档中访问值的推荐方法，因为每次使用时都必须加载和解析"_source"。使用"_source"非常慢。

[« Retrieve inner hits](inner-hits.md) [Search across clusters »](modules-
cross-cluster-search.md)
