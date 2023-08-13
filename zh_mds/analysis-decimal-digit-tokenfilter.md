

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Conditional token filter](analysis-condition-tokenfilter.md) [Delimited
payload token filter »](analysis-delimited-payload-tokenfilter.md)

## 十进制数字标记筛选器

将 Unicode "Decimal_Number"常规类别中的所有数字转换为"0-9"。例如，筛选器将孟加拉语数字"৩"更改为"3"。

此过滤器使用 Lucene 的十进制数字过滤器。

###Example

以下分析 API 请求使用"decimal_digit"筛选器将梵文数字转换为"0-9"：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'decimal_digit'
        ],
        text: '१-one two-२ ३'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "whitespace",
      "filter" : ["decimal_digit"],
      "text" : "१-one two-२ ३"
    }

筛选器生成以下标记：

    
    
    [ 1-one, two-2, 3]

### 添加到分析器

以下创建索引 APIrequest 使用"decimal_digit"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'decimal_digit_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_decimal_digit: {
                tokenizer: 'whitespace',
                filter: [
                  'decimal_digit'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /decimal_digit_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_decimal_digit": {
              "tokenizer": "whitespace",
              "filter": [ "decimal_digit" ]
            }
          }
        }
      }
    }

[« Conditional token filter](analysis-condition-tokenfilter.md) [Delimited
payload token filter »](analysis-delimited-payload-tokenfilter.md)
