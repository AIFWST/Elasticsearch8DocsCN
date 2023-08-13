

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« `rewrite` parameter](query-dsl-multi-term-rewrite.md) [Aggregations
»](search-aggregations.md)

## 正则表达式语法

正则表达式可以使用占位符字符(称为运算符)匹配数据中的模式。

Elasticsearch 支持以下查询中的正则表达式：

* "正则表达式" * "query_string"

Elasticsearch使用Apache Lucene的正则表达式引擎来解析这些查询。

### 保留字符

Lucene的正则表达式引擎支持所有Unicode字符。但是，以下字符保留为运算符：

    
    
    . ? + * | { } [ ] ( ) " \

根据启用的可选运算符，还可以保留以下字符：

    
    
    # @ & < >  ~

若要按字面意思使用这些字符之一，请使用前面的反斜杠将其转义，并用双引号将其括起来。例如：

    
    
    \@                  # renders as a literal '@'
    \\                  # renders as a literal '\'
    "john@smith.com"    # renders as 'john@smith.com'

反斜杠是 JSON 字符串和正则表达式中的转义字符。您需要在查询中转义两个反斜杠，除非您使用 alanguage 客户端来处理这个问题。例如，字符串"a\b"需要索引为"a\\b"：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        my_field: 'a\\b'
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "my_field": "a\\b"
    }

此文档与以下"正则表达式"查询匹配：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          regexp: {
            "my_field.keyword": 'a\\\\.*'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "regexp": {
          "my_field.keyword": "a\\\\.*"
        }
      }
    }

### 标准运算符

Lucene的正则表达式引擎不使用Perl兼容正则表达式(PCRE)库，但它确实支持以下标准运算符。

`.`

    

匹配任何字符。例如：

    
    
    ab.     # matches 'aba', 'abb', 'abz', etc.

`?`

    

将前面的字符重复零次或一次。通常用于使前面的字符可选。例如：

    
    
    abc?     # matches 'ab' and 'abc'

`+`

    

重复上述字符一次或多次。例如：

    
    
    ab+     # matches 'ab', 'abb', 'abbb', etc.

`*`

    

重复上述字符零次或多次。例如：

    
    
    ab*     # matches 'a', 'ab', 'abb', 'abbb', etc.

`{}`

    

前面的字符可以重复的最小和最大次数。例如：

    
    
    a{2}    # matches 'aa'
    a{2,4}  # matches 'aa', 'aaa', and 'aaaa'
    a{2,}   # matches 'a` repeated two or more times

`|`

    

OR 运算符。如果左侧或右侧的最长模式匹配，则匹配将成功。例如：

    
    
    abc|xyz  # matches 'abc' and 'xyz'

'( ... )`

    

形成一个组。可以使用组将表达式的一部分视为单个字符。例如：

    
    
    abc(def)?  # matches 'abc' and 'abcdef' but not 'abcd'

'[ ... ]`

    

匹配括号中的某个字符。例如：

    
    
    [abc]   # matches 'a', 'b', 'c'

在括号内，"-"表示范围，除非"-"是第一个转义的字符。例如：

    
    
    [a-c]   # matches 'a', 'b', or 'c'
    [-abc]  # '-' is first character. Matches '-', 'a', 'b', or 'c'
    [abc\-] # Escapes '-'. Matches 'a', 'b', 'c', or '-'

括号中字符前的"^"否定字符或范围。例如：

    
    
    [^abc]      # matches any character except 'a', 'b', or 'c'
    [^a-c]      # matches any character except 'a', 'b', or 'c'
    [^-abc]     # matches any character except '-', 'a', 'b', or 'c'
    [^abc\-]    # matches any character except 'a', 'b', 'c', or '-'

### 可选运算符

您可以使用"flags"参数为 Lucene 的正则表达式引擎启用更多可选运算符。

要启用多个运算符，请使用"|"分隔符。例如，"标志"值为"COMPLEMENT|INTERVAL"启用"补码"和"INTERVAL"运算符。

#### 有效值

"全部"(默认)

     Enables all optional operators. 
`""` (empty string)

     Alias for the `ALL` value. 
`COMPLEMENT`

    

启用"~"运算符。您可以使用"~"来否定最短的跟随模式。例如：

    
    
    a~bc   # matches 'adc' and 'aec' but not 'abc'

`EMPTY`

    

启用"#"(空语言)运算符。"#"运算符不匹配任何字符串，甚至不匹配空字符串。

如果通过以编程方式组合值来创建正则表达式，则可以传递"#"以指定"无字符串"。这样可以避免意外匹配空字符串或其他不需要的字符串。例如：

    
    
    #|abc  # matches 'abc' but nothing else, not even an empty string

`INTERVAL`

    

启用"<>"运算符。您可以使用"<>"来匹配数字范围。例如：

    
    
    foo<1-100>      # matches 'foo1', 'foo2' ... 'foo99', 'foo100'
    foo<01-100>     # matches 'foo01', 'foo02' ... 'foo99', 'foo100'

`INTERSECTION`

    

启用充当 AND 运算符的"&"运算符。如果左侧和右侧的模式匹配，则匹配将成功。例如：

    
    
    aaa.+&.+bbb  # matches 'aaabbb'

`ANYSTRING`

    

启用"@"运算符。您可以使用"@"来匹配任何整个字符串。

您可以将"@"运算符与"&"和"~"运算符组合在一起，以创建"除所有内容"逻辑。例如：

    
    
    @&~(abc.+)  # matches everything except terms beginning with 'abc'

`NONE`

     Disables all optional operators. 

### 不支持的运算符

Lucene 的正则表达式引擎不支持锚运算符，例如"^"(行首)或"$"(行尾)。若要匹配术语，正则表达式必须匹配整个字符串。

[« `rewrite` parameter](query-dsl-multi-term-rewrite.md) [Aggregations
»](search-aggregations.md)
