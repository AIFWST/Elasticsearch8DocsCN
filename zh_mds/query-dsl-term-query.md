

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Regexp query](query-dsl-regexp-query.md) [Terms query »](query-dsl-terms-
query.md)

## 术语查询

返回在提供的字段中包含 **精确** 术语的文档。

您可以使用"term"查询根据精确值(如价格、产品 ID 或用户名)查找文档。

避免对"文本"字段使用"术语"查询。

默认情况下，Elasticsearch 会更改"文本"字段的值作为分析的一部分。这会使查找"文本"字段值的完全匹配项变得困难。

要搜索"文本"字段值，请改用"匹配"查询。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          term: {
            "user.id": {
              value: 'kimchy',
              boost: 1
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "term": {
          "user.id": {
            "value": "kimchy",
            "boost": 1.0
          }
        }
      }
    }

### "术语"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`value`

     (Required, string) Term you wish to find in the provided `<field>`. To return a document, the term must exactly match the field value, including whitespace and capitalization. 
`boost`

    

(可选，浮动)用于减少或增加查询的相关性分数的浮点数。默认为"1.0"。

您可以使用"boost"参数来调整包含两个或多个查询的搜索的相关性分数。

提升值相对于默认值"1.0"。介于"0"和"1.0"之间的提升值会降低相关性分数。大于"1.0"的值会增加相关性分数。

"case_insensitive" [7.10.0] 在 7.10.0 中添加。

     (Optional, Boolean) Allows ASCII case insensitive matching of the value with the indexed field values when set to true. Default is false which means the case sensitivity of matching depends on the underlying field's mapping. 

###Notes

#### 避免对"文本"字段使用"术语"查询

默认情况下，Elasticsearch 会在分析过程中更改"文本"字段的值。例如，默认标准分析器更改"文本"字段值，如下所示：

* 删除了大多数标点符号 * 将剩余内容划分为单独的单词，称为标记 * 标记小写

为了更好地搜索"文本"字段，"匹配"查询还会在执行搜索之前分析您提供的搜索词。这意味着"匹配"查询可以在"文本"字段中搜索分析的令牌，而不是确切的术语。

"term"查询不会分析搜索词。"term"查询仅搜索您提供的 **确切** 术语。这意味着"term"查询在搜索"文本"字段时可能会返回较差的结果或没有结果。

若要查看搜索结果的差异，请尝试以下示例。

1. 使用名为"full_text"的"文本"字段创建一个索引。           响应 = client.indices.create( index： 'my-index-000001'， body： { mappings： { properties： { full_text： { type： 'text' } } } } ) put response res， err ：= es.Indices.Create( "my-index-000001"， es.Indices.Create.WithBody(strings.NewReader('{ "mappings"： { "properties"： { "full_text"： { "type"： "text" } } } }'))， ) fmt.Println(res， err) PUT my-index-000001 { "mappings"： { "properties"： { "full_text"： { "type"： "text" } } } }

2. 在"full_text"字段中为值为"Quick Brown Foxes！"的文档编制索引。           响应 = client.index( index： 'my-index-000001'， id： 1， body： { full_text： 'Quick Brown Foxes！'     } ) 放置响应 res， err ：= es.索引( "my-index-000001"， 字符串.NewReader('{ "full_text"： "Quick Brown Foxes！"   	}')， es.Index.WithDocumentID("1")， es.Index.WithPretty()， ) fmt.Println(res， err) PUT my-index-000001/_doc/1 { "full_text"： "Quick Brown Foxes！"   }

因为"full_text"是一个"文本"字段，所以Elasticsearch在分析过程中将"Quick BrownFoxes！"更改为"[quick， brown， fox]"。

3. 使用"术语"查询在"full_text"字段中搜索"快速棕色狐狸！包括"漂亮"参数，以便响应更具可读性。           响应 = client.search( index： 'my-index-000001'， 漂亮： true， body： { query： { term： { full_text： 'Quick Brown Foxes！'         } } } ) 把响应 res， err ：= es.搜索( es.Search.WithIndex("my-index-000001")， es.Search.WithBody(strings.NewReader('{ "query"： { "term"： { "full_text"： "Quick Brown Foxes！"   	    } } }'))， es.Search.WithPretty()， ) fmt.Println(res， err) GET my-index-000001/_search？pretty { "query"： { "term"： { "full_text"： "Quick Brown Foxes！"       }      }    }

由于"full_text"字段不再包含"精确"术语"QuickBrown Foxes！"，因此"term"查询搜索不会返回任何结果。

4. 使用"匹配"查询在"full_text"字段中搜索"快速棕色狐狸！           响应 = client.search( index： 'my-index-000001'， 漂亮： true， body： { query： { match： { full_text： 'Quick Brown Foxes！'         } } } ) 把响应 res， err ：= es.搜索( es.Search.WithIndex("my-index-000001")， es.Search.WithBody(strings.NewReader('{ "query"： { "match"： { "full_text"： "Quick Brown Foxes！"   	    } } }'))， es.Search.WithPretty()， ) fmt.Println(res， err) GET my-index-000001/_search？pretty { "query"： { "match"： { "full_text"： "Quick Brown Foxes！"       }      }    }

与"term"查询不同，"match"查询在执行搜索之前会分析您提供的搜索词"Quick Brown Foxes！"。然后，"match"查询返回"full_text"字段中包含"快速"、"棕色"或"fox"标记的任何文档。

下面是结果中包含索引文档的"匹配"查询搜索的响应。

    
        {
      "took" : 1,
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
        "max_score" : 0.8630463,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "1",
            "_score" : 0.8630463,
            "_source" : {
              "full_text" : "Quick Brown Foxes!"
            }
          }
        ]
      }
    }

[« Regexp query](query-dsl-regexp-query.md) [Terms query »](query-dsl-terms-
query.md)
