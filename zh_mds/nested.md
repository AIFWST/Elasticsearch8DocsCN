

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Keyword type family](keyword.md) [Numeric field types »](number.md)

## 嵌套字段类型

"嵌套"类型是"对象"数据类型的专用版本，它允许以可以彼此独立查询的方式对对象数组进行索引。

当引入具有大型任意键集的键值对时，您可以考虑将每个键值对建模为具有"键"和"值"字段的自己的嵌套文档。相反，请考虑使用平展数据类型，它将整个对象映射为单个字段，并允许对其内容进行简单搜索。嵌套文档和查询通常很昂贵，因此在此用例中使用"平展"数据类型是更好的选择。

### 对象数组如何展平化

Elasticsearch没有内部对象的概念。因此，它将对象层次结构平展为字段名称和值的简单列表。例如，考虑以下文档：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
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
    
    
    res, err := es.Index(
    	"my-index-000001",
    	strings.NewReader(`{
    	  "group": "fans",
    	  "user": [
    	    {
    	      "first": "John",
    	      "last": "Smith"
    	    },
    	    {
    	      "first": "Alice",
    	      "last": "White"
    	    }
    	  ]
    	}`),
    	es.Index.WithDocumentID("1"),
    	es.Index.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    PUT my-index-000001/_doc/1
    {
      "group" : "fans",
      "user" : [ __{
          "first" : "John",
          "last" :  "Smith"
        },
        {
          "first" : "Alice",
          "last" :  "White"
        }
      ]
    }

__

|

"用户"字段作为"对象"类型的字段动态添加。   ---|--- 以前的文档将在内部转换为看起来更像这样的文档：

    
    
    {
      "group" :        "fans",
      "user.first" : [ "alice", "john" ],
      "user.last" :  [ "smith", "white" ]
    }

"user.first"和"user.last"字段被平展为多值字段，并且"alice"和"white"之间的关联丢失。此文档将错误地匹配"爱丽丝和史密斯"的查询：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          bool: {
            must: [
              {
                match: {
                  "user.first": 'Alice'
                }
              },
              {
                match: {
                  "user.last": 'Smith'
                }
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("my-index-000001"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "bool": {
    	      "must": [
    	        {
    	          "match": {
    	            "user.first": "Alice"
    	          }
    	        },
    	        {
    	          "match": {
    	            "user.last": "Smith"
    	          }
    	        }
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET my-index-000001/_search
    {
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "Smith" }}
          ]
        }
      }
    }

### 对对象数组使用"嵌套"字段

如果需要为对象数组编制索引并保持数组中每个对象的独立性，请使用"嵌套"数据类型而不是"对象"数据类型。

在内部，嵌套对象将数组中的每个对象索引为单独的隐藏文档，这意味着可以使用"嵌套"查询独立于其他对象查询每个嵌套对象：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            user: {
              type: 'nested'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
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
        query: {
          nested: {
            path: 'user',
            query: {
              bool: {
                must: [
                  {
                    match: {
                      "user.first": 'Alice'
                    }
                  },
                  {
                    match: {
                      "user.last": 'Smith'
                    }
                  }
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          nested: {
            path: 'user',
            query: {
              bool: {
                must: [
                  {
                    match: {
                      "user.first": 'Alice'
                    }
                  },
                  {
                    match: {
                      "user.last": 'White'
                    }
                  }
                ]
              }
            },
            inner_hits: {
              highlight: {
                fields: {
                  "user.first": {}
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Indices.Create(
    		"my-index-000001",
    		es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "user": {
    	        "type": "nested"
    	      }
    	    }
    	  }
    	}`)),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "group": "fans",
    	  "user": [
    	    {
    	      "first": "John",
    	      "last": "Smith"
    	    },
    	    {
    	      "first": "Alice",
    	      "last": "White"
    	    }
    	  ]
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "nested": {
    	      "path": "user",
    	      "query": {
    	        "bool": {
    	          "must": [
    	            {
    	              "match": {
    	                "user.first": "Alice"
    	              }
    	            },
    	            {
    	              "match": {
    	                "user.last": "Smith"
    	              }
    	            }
    	          ]
    	        }
    	      }
    	    }
    	  }
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "nested": {
    	      "path": "user",
    	      "query": {
    	        "bool": {
    	          "must": [
    	            {
    	              "match": {
    	                "user.first": "Alice"
    	              }
    	            },
    	            {
    	              "match": {
    	                "user.last": "White"
    	              }
    	            }
    	          ]
    	        }
    	      },
    	      "inner_hits": {
    	        "highlight": {
    	          "fields": {
    	            "user.first": {}
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "user": {
            "type": "nested" __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1
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
    
    GET my-index-000001/_search
    {
      "query": {
        "nested": {
          "path": "user",
          "query": {
            "bool": {
              "must": [
                { "match": { "user.first": "Alice" }},
                { "match": { "user.last":  "Smith" }} __]
            }
          }
        }
      }
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "nested": {
          "path": "user",
          "query": {
            "bool": {
              "must": [
                { "match": { "user.first": "Alice" }},
                { "match": { "user.last":  "White" }} __]
            }
          },
          "inner_hits": { __"highlight": {
              "fields": {
                "user.first": {}
              }
            }
          }
        }
      }
    }

__

|

"用户"字段映射为类型"嵌套"而不是类型"对象"。   ---|---    __

|

此查询不匹配，因为"Alice"和"Smith"不在同一嵌套对象中。   __

|

此查询匹配是因为"Alice"和"White"位于同一个嵌套对象中。   __

|

"inner_hits"允许我们突出显示匹配的嵌套文档。   ### 与"嵌套"文档交互编辑

嵌套文档可以是：

* 使用"嵌套"查询进行查询。  * 使用"嵌套"和"reverse_nested"聚合进行分析。  * 使用嵌套排序排序。  *检索并突出显示嵌套的内部命中。

由于嵌套文档作为单独的文档编制索引，因此只能在"嵌套"查询、"嵌套"/"reverse_nested"聚合或嵌套内部命中范围内访问它们。

例如，如果嵌套文档中的字符串字段将"index_options"设置为"偏移"以允许在突出显示期间使用过帐，则这些偏移在主突出显示阶段将不可用。相反，需要通过嵌套的内部命中来执行突出显示。在通过"docvalue_fields"或"stored_fields"搜索期间加载字段时，同样的注意事项也适用。

### "嵌套"字段的参数

"嵌套"字段接受以下参数：

"动态"

     (Optional, string) Whether or not new `properties` should be added dynamically to an existing nested object. Accepts `true` (default), `false` and `strict`. 
[`properties`](properties.html "properties")

     (Optional, object) The fields within the nested object, which can be of any [data type](mapping-types.html "Field data types"), including `nested`. New properties may be added to an existing nested object. 
`include_in_parent`

     (Optional, Boolean) If `true`, all fields in the nested object are also added to the parent document as standard (flat) fields. Defaults to `false`. 
`include_in_root`

     (Optional, Boolean) If `true`, all fields in the nested object are also added to the root document as standard (flat) fields. Defaults to `false`. 

### 对"嵌套"映射和对象的限制

如前所述，每个嵌套对象都作为单独的 Lucenedocument 进行索引。继续前面的示例，如果我们索引一个包含 100 个"user"对象的单个文档，那么将创建 101 个 Lucene 文档：一个用于父文档，一个用于每个嵌套对象。由于与"嵌套"映射相关的费用，Elasticsearch 设置了适当的设置来防止性能问题：

`index.mapping.nested_fields.limit`

     The maximum number of distinct `nested` mappings in an index. The `nested` type should only be used in special cases, when arrays of objects need to be queried independently of each other. To safeguard against poorly designed mappings, this setting limits the number of unique `nested` types per index. Default is `50`. 

在前面的示例中，"用户"映射将仅计为此限制的 1。

`index.mapping.nested_objects.limit`

     The maximum number of nested JSON objects that a single document can contain across all `nested` types. This limit helps to prevent out of memory errors when a document contains too many nested objects. Default is `10000`. 

为了说明此设置的工作原理，请考虑将另一个名为"注释"的"嵌套"类型添加到前面的示例映射中。对于每个文档，它包含的"用户"和"注释"对象的组合数量必须低于限制。

有关防止映射爆炸的其他设置，请参阅防止映射爆炸的设置。

[« Keyword type family](keyword.md) [Numeric field types »](number.md)
