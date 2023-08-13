

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Alias field type](field-alias.md) [Binary field type »](binary.md)

##Arrays

在Elasticsearch中，没有专用的"数组"数据类型。默认情况下，任何字段都可以包含零个或多个值，但是，数组中的所有值都必须具有相同的数据类型。例如：

* 字符串数组： [ '"一"， "二"' ] * 整数数组： [ '1'， '2' ] * 数组数组： [ '1'， [ '2'， '3' ]] 相当于 [ '1'， '2'， '3' ] * 对象数组： [ '{ "name"： "Mary"， "age"： 12 }'， '{ "name"： "John"， "age"： 10 }']

### 对象数组

对象数组无法按预期工作：您无法独立于数组中的其他对象查询每个对象。如果您需要能够执行此操作，则应使用"嵌套"数据类型而不是"对象"数据类型。

这在嵌套中有更详细的解释。

动态添加字段时，数组中的第一个值确定字段"类型"。所有后续值必须具有相同的数据类型，或者至少必须能够将后续值强制为相同的数据类型。

_不支持混合数据类型的数组：[ '10'， ''somestring'' ]

数组可能包含"null"值，这些值要么被配置的"null_value"替换，要么被完全跳过。空数组 '[]' 被视为缺少字段 - 没有值的字段。

无需预先配置即可在文档中使用数组，它们是开箱即用的：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        message: 'some arrays in this document...',
        tags: [
          'elasticsearch',
          'wow'
        ],
        lists: [
          {
            name: 'prog_list',
            description: 'programming list'
          },
          {
            name: 'cool_list',
            description: 'cool stuff list'
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        message: 'no arrays in this document...',
        tags: 'elasticsearch',
        lists: {
          name: 'prog_list',
          description: 'programming list'
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            tags: 'elasticsearch'
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "message": "some arrays in this document...",
    	  "tags": [
    	    "elasticsearch",
    	    "wow"
    	  ],
    	  "lists": [
    	    {
    	      "name": "prog_list",
    	      "description": "programming list"
    	    },
    	    {
    	      "name": "cool_list",
    	      "description": "cool stuff list"
    	    }
    	  ]
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "message": "no arrays in this document...",
    	  "tags": "elasticsearch",
    	  "lists": {
    	    "name": "prog_list",
    	    "description": "programming list"
    	  }
    	}`),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "tags": "elasticsearch"
    	    }
    	  }
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT my-index-000001/_doc/1
    {
      "message": "some arrays in this document...",
      "tags":  [ "elasticsearch", "wow" ], __"lists": [ __{
          "name": "prog_list",
          "description": "programming list"
        },
        {
          "name": "cool_list",
          "description": "cool stuff list"
        }
      ]
    }
    
    PUT my-index-000001/_doc/2 __{
      "message": "no arrays in this document...",
      "tags":  "elasticsearch",
      "lists": {
        "name": "prog_list",
        "description": "programming list"
      }
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "tags": "elasticsearch" __}
      }
    }

__

|

"标签"字段作为"字符串"字段动态添加。   ---|---    __

|

"列表"字段作为"对象"字段动态添加。   __

|

第二个文档不包含数组，但可以索引到相同的字段中。   __

|

查询在"标签"字段中查找"弹性搜索"，并匹配两个文档。   « 别名字段类型 二进制字段类型 »