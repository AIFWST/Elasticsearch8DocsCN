

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `doc_values`](doc-values.md) [`eager_global_ordinals` »](eager-global-
ordinals.md)

##'动态'

当您为包含新字段的文档编制索引时，Elasticsearch 会将该字段动态添加到文档或文档中的对象。以下文档在"name"对象下添加了字符串字段"用户名"、对象字段"name"和两个字符串字段：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        username: 'johnsmith',
        name: {
          first: 'John',
          last: 'Smith'
        }
      }
    )
    puts response
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "username": "johnsmith",
      "name": { __"first": "John",
        "last": "Smith"
      }
    }
    
    GET my-index-000001/_mapping __

__

|

将"name"对象下的字段称为"name.first"和"name.last"。   ---|---    __

|

检查映射以查看更改。   以下文档添加了两个字符串字段："电子邮件"和"name.middle"：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        username: 'marywhite',
        email: 'mary@white.com',
        name: {
          first: 'Mary',
          middle: 'Alice',
          last: 'White'
        }
      }
    )
    puts response
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    PUT my-index-000001/_doc/2
    {
      "username": "marywhite",
      "email": "mary@white.com",
      "name": {
        "first": "Mary",
        "middle": "Alice",
        "last": "White"
      }
    }
    
    GET my-index-000001/_mapping

### 在内部对象上设置"动态"

内部对象从其父对象继承"动态"设置。在以下示例中，动态映射在类型级别禁用，因此不会动态添加新的顶级字段。

但是，"user.social_networks"对象启用动态映射，因此您可以将字段添加到此内部对象。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic: false,
          properties: {
            user: {
              properties: {
                name: {
                  type: 'text'
                },
                social_networks: {
                  dynamic: true,
                  properties: {}
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic": false, __"properties": {
          "user": { __"properties": {
              "name": {
                "type": "text"
              },
              "social_networks": {
                "dynamic": true, __"properties": {}
              }
            }
          }
        }
      }
    }

__

|

在类型级别禁用动态映射。   ---|---    __

|

"user"对象继承类型级设置。   __

|

启用此内部对象的动态映射。   ### "动态"编辑的参数

"dynamic"参数控制是否动态添加新字段，并接受以下参数：

`true`

|

新字段将添加到映射中(默认)。   ---|---"运行时"

|

新字段将作为运行时字段添加到映射中。这些字段不编制索引，而是在查询时从"_source"加载。   "假"

|

新字段将被忽略。这些字段不会被编入索引或搜索，但仍会显示在返回的匹配的"_source"字段中。这些字段不会添加到映射中，并且必须显式添加新字段。   "严格"

|

如果检测到新字段，则会引发异常并拒绝文档。必须将新字段显式添加到映射中。   "doc_values""eager_global_ordinals"