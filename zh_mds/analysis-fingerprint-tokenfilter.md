

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Elision token filter](analysis-elision-tokenfilter.md) [Flatten graph
token filter »](analysis-flatten-graph-tokenfilter.md)

## 指纹令牌过滤器

对令牌流中的重复令牌进行排序并删除，然后将流连接到单个输出令牌。

例如，此筛选器更改"[ the， fox， was， 非常、非常、快速 ]' 令牌流，如下所示：

1. 按字母顺序对标记进行排序，以"[ fox， quick， the， 非常， 非常， was ]" 2.删除"非常"令牌的重复实例。  3. 将令牌流连接到输出单个令牌："[狐狸快速非常是]"

此筛选器生成的输出令牌对于对文本正文进行指纹识别和聚类非常有用，如 OpenRefineproject 中所述。

此过滤器使用 Lucene 的指纹过滤器。

###Example

以下分析 API 请求使用"指纹"筛选器为文本"斑马跳跃在休息的休息狗上"创建单个输出令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'fingerprint'
        ],
        text: 'zebra jumps over resting resting dog'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "whitespace",
      "filter" : ["fingerprint"],
      "text" : "zebra jumps over resting resting dog"
    }

筛选器生成以下令牌：

    
    
    [ dog jumps over resting zebra ]

### 添加到分析器

以下创建索引 APIrequest 使用"指纹"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'fingerprint_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_fingerprint: {
                tokenizer: 'whitespace',
                filter: [
                  'fingerprint'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT fingerprint_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_fingerprint": {
              "tokenizer": "whitespace",
              "filter": [ "fingerprint" ]
            }
          }
        }
      }
    }

### 可配置参数

`max_output_size`

     (Optional, integer) Maximum character length, including whitespace, of the output token. Defaults to `255`. Concatenated tokens longer than this will result in no token output. 
`separator`

     (Optional, string) Character to use to concatenate the token stream input. Defaults to a space. 

###Customize

要自定义"指纹"筛选器，请复制它，为新的自定义令牌筛选器创建基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义"指纹"筛选器，该筛选器使用"+"连接令牌流。筛选器还将输出令牌限制为"100"个字符或更少。

    
    
    response = client.indices.create(
      index: 'custom_fingerprint_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_: {
                tokenizer: 'whitespace',
                filter: [
                  'fingerprint_plus_concat'
                ]
              }
            },
            filter: {
              fingerprint_plus_concat: {
                type: 'fingerprint',
                max_output_size: 100,
                separator: '+'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT custom_fingerprint_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_": {
              "tokenizer": "whitespace",
              "filter": [ "fingerprint_plus_concat" ]
            }
          },
          "filter": {
            "fingerprint_plus_concat": {
              "type": "fingerprint",
              "max_output_size": 100,
              "separator": "+"
            }
          }
        }
      }
    }

[« Elision token filter](analysis-elision-tokenfilter.md) [Flatten graph
token filter »](analysis-flatten-graph-tokenfilter.md)
