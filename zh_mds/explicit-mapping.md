

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md)

[« Dynamic templates](dynamic-templates.md) [Runtime fields »](runtime.md)

## 显式映射

您对数据的了解比 Elasticsearch 所能猜测的要多，因此虽然动态映射对于入门很有用，但在某些时候，您会需要指定自己的显式映射。

您可以在创建索引并将字段添加到现有索引时创建字段映射。

### 使用显式映射创建索引

您可以使用创建索引 API 创建具有显式映射的新索引。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            age: {
              type: 'integer'
            },
            email: {
              type: 'keyword'
            },
            name: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "age": {
    	        "type": "integer"
    	      },
    	      "email": {
    	        "type": "keyword"
    	      },
    	      "name": {
    	        "type": "text"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "age":    { "type": "integer" },  __"email":  { "type": "keyword"  }, __"name":   { "type": "text"  } __}
      }
    }

__

|

创建"age"，一个"整数"字段 ---|--- __

|

创建"电子邮件"，即"关键字"字段 __

|

创建"名称"，即"文本"字段 ### 将字段添加到现有映射编辑

可以使用更新映射 API 向现有索引添加一个或多个新字段。

以下示例添加"employee-id"，这是一个"关键字"字段，其"索引"映射参数值为"false"。这意味着"员工 ID"字段的值已存储，但未编制索引或可用于搜索。

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          "employee-id": {
            type: 'keyword',
            index: false
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.PutMapping(
    	[]string{"my-index-000001"},
    	strings.NewReader(`{
    	  "properties": {
    	    "employee-id": {
    	      "type": "keyword",
    	      "index": false
    	    }
    	  }
    	}`),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001/_mapping
    {
      "properties": {
        "employee-id": {
          "type": "keyword",
          "index": false
        }
      }
    }

### 更新字段的映射

除支持的映射参数外，您无法更改现有字段的映射或字段类型。更改现有字段可能会使已编制索引的数据无效。

如果需要更改数据流的 backingindex 中字段的映射，请参阅更改数据流的映射和设置。

如果需要更改其他索引中字段的映射，请使用正确的映射创建一个新索引，并将数据重新索引到该索引中。

重命名字段将使已在旧字段名称下编制索引的数据无效。相反，添加"别名"字段以创建备用字段名称。

### 查看索引的映射

可以使用获取映射 API 查看现有索引的映射。

    
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    res, err := es.Indices.GetMapping(es.Indices.GetMapping.WithIndex("my-index-000001"))
    fmt.Println(res, err)
    
    
    GET /my-index-000001/_mapping

API 返回以下响应：

    
    
    {
      "my-index-000001" : {
        "mappings" : {
          "properties" : {
            "age" : {
              "type" : "integer"
            },
            "email" : {
              "type" : "keyword"
            },
            "employee-id" : {
              "type" : "keyword",
              "index" : false
            },
            "name" : {
              "type" : "text"
            }
          }
        }
      }
    }

### 查看特定字段的映射

如果只想查看一个或多个特定字段的映射，则可以使用 get 字段映射 API。

如果您不需要索引的完整映射或您的索引包含大量字段，这将非常有用。

以下请求检索"员工 ID"字段的映射。

    
    
    response = client.indices.get_field_mapping(
      index: 'my-index-000001',
      fields: 'employee-id'
    )
    puts response
    
    
    res, err := es.Indices.GetMapping(es.Indices.GetMapping.WithIndex("my-index-000001"))
    fmt.Println(res, err)
    
    
    GET /my-index-000001/_mapping/field/employee-id

API 返回以下响应：

    
    
    {
      "my-index-000001" : {
        "mappings" : {
          "employee-id" : {
            "full_name" : "employee-id",
            "mapping" : {
              "employee-id" : {
                "type" : "keyword",
                "index" : false
              }
            }
          }
        }
      }
    }

[« Dynamic templates](dynamic-templates.md) [Runtime fields »](runtime.md)
