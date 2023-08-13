

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Normalization token filters](analysis-normalization-tokenfilter.md)
[Pattern replace token filter »](analysis-pattern_replace-tokenfilter.md)

## 模式捕获令牌筛选器

与"模式"标记器不同，"pattern_capture"标记筛选器为正则表达式中的每个捕获组发出 atoken。模式不锚定到字符串的开头和结尾，因此每个模式可以匹配多次，并且允许匹配重叠。

### 当心病态正则表达式

模式捕获令牌筛选器使用 Java 正则表达式。

一个写得不好的正则表达式可能会运行得非常慢，甚至抛出 aStackOverflowError 并导致它运行的节点突然退出。

阅读更多关于病理正则表达式以及如何避免它们的信息。

例如，像这样的模式：

    
    
    "(([a-z]+)(\d*))"

匹配时：

    
    
    "abc123def456"

将生成令牌：[ 'abc123'， 'abc'， '123'， 'def456'， 'def'， '456' ]

如果"preserve_original"设置为"true"(默认值)，那么它还将发出原始令牌："abc123def456"。

这对于索引像驼峰大小写代码这样的文本特别有用，例如"stripHTML"，用户可以在其中搜索"strip html"或"striphtml"：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        settings: {
          analysis: {
            filter: {
              code: {
                type: 'pattern_capture',
                preserve_original: true,
                patterns: [
                  '(\\p{Ll}+|\\p{Lu}\\p{Ll}+|\\p{Lu}+)',
                  '(\\d+)'
                ]
              }
            },
            analyzer: {
              code: {
                tokenizer: 'pattern',
                filter: [
                  'code',
                  'lowercase'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT test
    {
       "settings" : {
          "analysis" : {
             "filter" : {
                "code" : {
                   "type" : "pattern_capture",
                   "preserve_original" : true,
                   "patterns" : [
                      "(\\p{Ll}+|\\p{Lu}\\p{Ll}+|\\p{Lu}+)",
                      "(\\d+)"
                   ]
                }
             },
             "analyzer" : {
                "code" : {
                   "tokenizer" : "pattern",
                   "filter" : [ "code", "lowercase" ]
                }
             }
          }
       }
    }

用于分析文本时

    
    
    import static org.apache.commons.lang.StringEscapeUtils.escapeHtml

这将发出令牌：[ 'import'， 'static'， 'org'， 'apache'， 'commons'， 'lang'， 'stringescapeutils'， 'string'， 'escape'， 'utils'， 'escapehtml'， 'escape'， 'html' ]

另一个例子是分析电子邮件地址：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        settings: {
          analysis: {
            filter: {
              email: {
                type: 'pattern_capture',
                preserve_original: true,
                patterns: [
                  '([^@]+)',
                  '(\\p{L}+)',
                  '(\\d+)',
                  '@(.+)'
                ]
              }
            },
            analyzer: {
              email: {
                tokenizer: 'uax_url_email',
                filter: [
                  'email',
                  'lowercase',
                  'unique'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT test
    {
       "settings" : {
          "analysis" : {
             "filter" : {
                "email" : {
                   "type" : "pattern_capture",
                   "preserve_original" : true,
                   "patterns" : [
                      "([^@]+)",
                      "(\\p{L}+)",
                      "(\\d+)",
                      "@(.+)"
                   ]
                }
             },
             "analyzer" : {
                "email" : {
                   "tokenizer" : "uax_url_email",
                   "filter" : [ "email", "lowercase",  "unique" ]
                }
             }
          }
       }
    }

当上述分析器用于电子邮件地址时，例如：

    
    
    john-smith_123@foo-bar.com

它将生成以下令牌：

    
    
    john-smith_123@foo-bar.com, john-smith_123,
    john, smith, 123, foo-bar.com, foo, bar, com

需要多个模式才能允许重叠捕获，但也意味着模式密度较低且更易于理解。

**注意：** 所有令牌都在同一位置发出，并具有相同的字符偏移量。这意味着，例如，使用此分析器的"john-smith_123@foo-bar.com"的"匹配"查询将返回包含任何这些标记的文档，即使使用"and"运算符也是如此。此外，当与突出显示结合使用时，将突出显示整个原始令牌，而不仅仅是匹配的子集。例如，在上述电子邮件地址中查询"史密斯"将突出显示：

    
    
      <em>john-smith_123@foo-bar.com</em>

not:

    
    
      john-<em>smith</em>_123@foo-bar.com

[« Normalization token filters](analysis-normalization-tokenfilter.md)
[Pattern replace token filter »](analysis-pattern_replace-tokenfilter.md)
