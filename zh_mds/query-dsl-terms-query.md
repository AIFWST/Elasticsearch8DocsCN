

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Term query](query-dsl-term-query.md) [Terms set query »](query-dsl-terms-
set-query.md)

## 术语查询

返回在提供的字段中包含一个或多个"精确**"术语的文档。

"terms"查询与"term"查询相同，只是您可以搜索多个值。如果文档至少包含一个术语，则该文档将匹配。要搜索包含多个匹配术语的文档，请使用"terms_set"查询。

### 示例请求

以下搜索返回"user.id"字段包含"kimchy"或"elkbee"的文档。

    
    
    response = client.search(
      body: {
        query: {
          terms: {
            "user.id": [
              'kimchy',
              'elkbee'
            ],
            boost: 1
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "terms": {
          "user.id": [ "kimchy", "elkbee" ],
          "boost": 1.0
        }
      }
    }

### "术语"的顶级参数

`<field>`

    

(可选，对象)您要搜索的字段。

此参数的值是您希望在提供的字段中找到的术语数组。若要返回文档，一个或多个术语必须与字段值(包括空格和大小写)完全匹配。

默认情况下，Elasticsearch 将"terms"查询限制为最多 65，536 个术语。您可以使用"index.max_terms_count"设置更改此限制。

要将现有文档的字段值用作搜索词，请使用术语查找参数。

`boost`

    

(可选，浮动)用于减少或增加查询的相关性分数的浮点数。默认为"1.0"。

您可以使用"boost"参数来调整包含两个或多个查询的搜索的相关性分数。

提升值相对于默认值"1.0"。介于"0"和"1.0"之间的提升值会降低相关性分数。大于"1.0"的值会增加相关性分数。

###Notes

#### 突出显示"术语"查询

突出显示只是尽力而为。Elasticsearch 可能不会返回"术语"查询的突出显示结果，具体取决于：

* 荧光笔类型 * 查询中的字词数

#### 术语查找

术语查找提取现有文档的字段值。Elasticsearchthen使用这些值作为搜索词。这在搜索大量术语时非常有用。

要运行术语查找，必须启用字段的"_source"。不能使用跨集群搜索对远程索引运行术语查找。

默认情况下，Elasticsearch 将"terms"查询限制为最多 65，536 个术语。这包括使用术语查找获取的字词。您可以使用"索引.max_术语_计数"设置更改此限制。

为了减少网络流量，如果可能，术语查找将从本地数据节点上的分片中获取文档的值。如果术语数据不大，请考虑使用具有单个主分片的索引，该分片在所有适用的数据节点上完全复制，以最大程度地减少网络流量。

要执行术语查找，请使用以下参数。

##### 术语查找参数

`index`

     (Required, string) Name of the index from which to fetch field values. 
`id`

     (Required, string) [ID](mapping-id-field.html "_id field") of the document from which to fetch field values. 
`path`

    

(必需，字符串)要从中获取字段值的字段的名称。Elasticsearch 使用这些值作为查询的搜索词。

如果字段值包含嵌套内部对象的数组，则可以使用点表示法语法访问这些对象。

`routing`

     (Optional, string) Custom [routing value](mapping-routing-field.html "_routing field") of the document from which to fetch term values. If a custom routing value was provided when the document was indexed, this parameter is required. 

##### 术语查找示例

若要查看术语查找的工作原理，请尝试以下示例。

1. 使用名为"颜色"的"关键字"字段创建索引。           响应 = client.indices.create( index： 'my-index-000001'， body： { mappings： { properties： { color： { type： 'keyword' } } } } ) put response res， err ：= es.Indices.Create( "my-index-000001"， es.Indices.Create.WithBody(strings.NewReader('{ "mappings"： { "properties"： { "color"： { "type"： "keyword" } } } }'))， ) fmt.Println(res， err) PUT my-index-000001 { "mappings"： { "properties"： { "color"： { "type"： "keyword" } } } }

2. 在"颜色"字段中索引 ID 为 1 且值为"["蓝色"、"绿色"]"的文档。           响应 = client.index( index： 'my-index-000001'， id： 1， body： { color： [ 'blue'， 'green' ] } ) 把响应 res， err ：= es.索引( "my-index-000001"， 字符串.NewReader('{ "color"： [ "blue"， "green" ] }')， es.Index.WithDocumentID("1")， es.Index.WithPretty()， ) fmt.Println(res， err) PUT my-index-000001/_doc/1 { "color"： ["blue"， "green"] }

3. 索引另一个 ID 为 2 且"颜色"字段中值为"蓝色"的文档。           响应 = client.index( index： 'my-index-000001'， id： 2， body： { color： 'blue' } ) 放置响应 res， err ：= es.索引( "my-index-000001"， 字符串.NewReader('{ "color"： "blue" }')， es.Index.WithDocumentID("2")， es.Index.WithPretty()， ) fmt.Println(res， err) PUT my-index-000001/_doc/2 { "color"： "blue" }

4. 将"术语"查询与术语查找参数一起使用，以查找包含一个或多个与文档 2 相同的术语的文档。包括"漂亮"参数，以便响应更具可读性。           响应 = client.search( index： 'my-index-000001'， pretty： true， body： { query： { terms： { color： { index： 'my-index-000001'， id： '2'， path： 'color' } } } } ) 把响应 res， err ：= es.搜索( es.Search.WithIndex("my-index-000001")， es.Search.WithBody(strings.NewReader('{ "query"： { "terms"： { "color"： { "index"： "my-index-000001"， "id"： "2"， "path"： "color" } } } }'))， es.Search.WithPretty()， ) fmt.Println(res， err) GET my-index-000001/_search？pretty { "query"： { "terms"： { "color" ： { "index" ： "my-index-000001"， "id" ： "2"， "path" ： "color" } } }

由于文档 2 和文档 1 在"color"字段中都包含"blue"作为值，因此 Elasticsearch 会返回这两个文档。

    
        {
      "took" : 17,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 2,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "1",
            "_score" : 1.0,
            "_source" : {
              "color" : [
                "blue",
                "green"
              ]
            }
          },
          {
            "_index" : "my-index-000001",
            "_id" : "2",
            "_score" : 1.0,
            "_source" : {
              "color" : "blue"
            }
          }
        ]
      }
    }

[« Term query](query-dsl-term-query.md) [Terms set query »](query-dsl-terms-
set-query.md)
