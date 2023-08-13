

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Aliases API](indices-aliases.md) [Analyze index disk usage API
»](indices-disk-usage.md)

## 分析接口

对文本字符串执行分析并返回生成的标记。

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'standard',
        text: 'Quick Brown Foxes!'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "analyzer" : "standard",
      "text" : "Quick Brown Foxes!"
    }

###Request

"获取/_analyze"

"发布/_analyze"

"得到/<index>/_analyze"

"发布/<index>/_analyze"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须具有指定索引的"管理"索引权限。

### 路径参数

`<index>`

    

(可选，字符串)用于派生分析器的索引。

如果指定，"分析器"或<field>""参数将覆盖此值。

如果未指定分析器或字段，则分析 API 对索引使用默认分析器。

如果未指定索引或索引没有默认分析器，则分析 API 将使用标准分析器。

### 查询参数

`analyzer`

    

(可选，字符串)应应用于提供的"文本"的分析器的名称。这可以是内置分析器，也可以是在索引中配置的分析器。

如果未指定此参数，则分析 API 将使用字段映射中定义的分析器。

如果未指定字段，则分析 API 对索引使用默认分析器。

如果未指定索引，或者索引没有默认分析器，则分析 API 将使用标准分析器。

`attributes`

     (Optional, array of strings) Array of token attributes used to filter the output of the `explain` parameter. 
`char_filter`

     (Optional, array of strings) Array of character filters used to preprocess characters before the tokenizer. See [_Character filters reference_](analysis-charfilters.html "Character filters reference") for a list of character filters. 
`explain`

     (Optional, Boolean) If `true`, the response includes token attributes and additional details. Defaults to `false`.  [preview]  The format of the additional detail information is labelled as experimental in Lucene and it may change in the future. 
`field`

    

(可选，字符串)用于派生分析器的字段。若要使用此参数，必须指定索引。

如果指定，"分析器"参数将覆盖此值。

如果未指定字段，则分析 API 对索引使用默认分析器。

如果未指定索引或索引没有默认分析器，则分析 API 将使用标准分析器。

`filter`

     (Optional, Array of strings) Array of token filters used to apply after the tokenizer. See [_Token filter reference_](analysis-tokenfilters.html "Token filter reference") for a list of token filters. 
`normalizer`

     (Optional, string) Normalizer to use to convert text into a single token. See [_Normalizers_](analysis-normalizers.html "Normalizers") for a list of normalizers. 
`text`

     (Required, string or array of strings) Text to analyze. If an array of strings is provided, it is analyzed as a multi-value field. 
`tokenizer`

     (Optional, string) Tokenizer to use to convert text into tokens. See [_Tokenizer reference_](analysis-tokenizers.html "Tokenizer reference") for a list of tokenizers. 

###Examples

#### 未指定索引

可以将任何内置分析器应用于文本字符串，而无需指定索引。

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'standard',
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "analyzer" : "standard",
      "text" : "this is a test"
    }

#### 文本字符串数组

如果 'text' 参数作为字符串数组提供，则将其分析为多值字段。

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'standard',
        text: [
          'this is a test',
          'the second text'
        ]
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "analyzer" : "standard",
      "text" : ["this is a test", "the second text"]
    }

#### 自定义分析器

可以使用分析 API 测试由令牌器、令牌筛选器和字符筛选器生成的自定义瞬态分析器。令牌筛选器使用"筛选器"参数：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        filter: [
          'lowercase'
        ],
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "keyword",
      "filter" : ["lowercase"],
      "text" : "this is a test"
    }
    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        filter: [
          'lowercase'
        ],
        char_filter: [
          'html_strip'
        ],
        text: 'this is a test</b>'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "keyword",
      "filter" : ["lowercase"],
      "char_filter" : ["html_strip"],
      "text" : "this is a <b>test</b>"
    }

可以在请求正文中指定自定义分词器、令牌筛选器和字符筛选器，如下所示：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'lowercase',
          {
            type: 'stop',
            stopwords: [
              'a',
              'is',
              'this'
            ]
          }
        ],
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "whitespace",
      "filter" : ["lowercase", {"type": "stop", "stopwords": ["a", "is", "this"]}],
      "text" : "this is a test"
    }

#### 特定索引

您还可以针对特定索引运行分析 API：

    
    
    response = client.indices.analyze(
      index: 'analyze_sample',
      body: {
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /analyze_sample/_analyze
    {
      "text" : "this is a test"
    }

上面将使用与"analyze_sample"索引关联的默认索引分析器对"这是一个测试"文本运行分析。也可以提供"分析器"以使用不同的分析器：

    
    
    response = client.indices.analyze(
      index: 'analyze_sample',
      body: {
        analyzer: 'whitespace',
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /analyze_sample/_analyze
    {
      "analyzer" : "whitespace",
      "text" : "this is a test"
    }

#### 从字段映射派生分析器

分析器可以基于字段映射派生，例如：

    
    
    response = client.indices.analyze(
      index: 'analyze_sample',
      body: {
        field: 'obj1.field1',
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /analyze_sample/_analyze
    {
      "field" : "obj1.field1",
      "text" : "this is a test"
    }

将导致分析基于在映射中为"obj1.field1"配置的分析器(如果没有，则默认索引分析器)进行。

####Normalizer

可以为关键字字段提供"规范化器"，其中规范化器与"analyze_sample"索引相关联。

    
    
    response = client.indices.analyze(
      index: 'analyze_sample',
      body: {
        normalizer: 'my_normalizer',
        text: 'BaR'
      }
    )
    puts response
    
    
    GET /analyze_sample/_analyze
    {
      "normalizer" : "my_normalizer",
      "text" : "BaR"
    }

或者通过从令牌筛选器和字符筛选器构建自定义瞬态规范化程序。

    
    
    response = client.indices.analyze(
      body: {
        filter: [
          'lowercase'
        ],
        text: 'BaR'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "filter" : ["lowercase"],
      "text" : "BaR"
    }

#### 解释分析

如果要获取更高级的详细信息，请将"解释"设置为"true"(默认为"false")。它将输出每个令牌的所有令牌属性。您可以通过设置"属性"选项来过滤要输出的令牌属性。

附加详细信息的格式标记为实验性 inLucene，将来可能会发生变化。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'snowball'
        ],
        text: 'detailed output',
        explain: true,
        attributes: [
          'keyword'
        ]
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "standard",
      "filter" : ["snowball"],
      "text" : "detailed output",
      "explain" : true,
      "attributes" : ["keyword"] __}

__

|

设置"关键字"以仅输出"关键字"属性---|--- 请求返回以下结果：

    
    
    {
      "detail" : {
        "custom_analyzer" : true,
        "charfilters" : [ ],
        "tokenizer" : {
          "name" : "standard",
          "tokens" : [ {
            "token" : "detailed",
            "start_offset" : 0,
            "end_offset" : 8,
            "type" : "<ALPHANUM>",
            "position" : 0
          }, {
            "token" : "output",
            "start_offset" : 9,
            "end_offset" : 15,
            "type" : "<ALPHANUM>",
            "position" : 1
          } ]
        },
        "tokenfilters" : [ {
          "name" : "snowball",
          "tokens" : [ {
            "token" : "detail",
            "start_offset" : 0,
            "end_offset" : 8,
            "type" : "<ALPHANUM>",
            "position" : 0,
            "keyword" : false __}, {
            "token" : "output",
            "start_offset" : 9,
            "end_offset" : 15,
            "type" : " <ALPHANUM>",
            "position" : 1,
            "keyword" : false __} ]
        } ]
      }
    }

__

|

仅输出"关键字"属性，因为在请求中指定"属性"。   ---|--- #### 设置令牌限制它

生成过多的令牌可能会导致节点内存不足。以下设置允许限制可以生成的令牌数量：

`index.analyze.max_token_count`

     The maximum number of tokens that can be produced using `_analyze` API. The default value is `10000`. If more than this limit of tokens gets generated, an error will be thrown. The `_analyze` endpoint without a specified index will always use `10000` value as a limit. This setting allows you to control the limit for a specific index: 
    
    
    response = client.indices.create(
      index: 'analyze_sample',
      body: {
        settings: {
          "index.analyze.max_token_count": 20_000
        }
      }
    )
    puts response
    
    
    PUT /analyze_sample
    {
      "settings" : {
        "index.analyze.max_token_count" : 20000
      }
    }
    
    
    response = client.indices.analyze(
      index: 'analyze_sample',
      body: {
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /analyze_sample/_analyze
    {
      "text" : "this is a test"
    }

[« Aliases API](indices-aliases.md) [Analyze index disk usage API
»](indices-disk-usage.md)
