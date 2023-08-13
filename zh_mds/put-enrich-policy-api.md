

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Enrich APIs](enrich-apis.md)

[« Enrich APIs](enrich-apis.md) [Delete enrich policy API »](delete-enrich-
policy-api.md)

## 创建扩充策略接口

创建扩充策略。

    
    
    response = client.enrich.put_policy(
      name: 'my-policy',
      body: {
        match: {
          indices: 'users',
          match_field: 'email',
          enrich_fields: [
            'first_name',
            'last_name',
            'city',
            'zip',
            'state'
          ]
        }
      }
    )
    puts response
    
    
    PUT /_enrich/policy/my-policy
    {
      "match": {
        "indices": "users",
        "match_field": "email",
        "enrich_fields": ["first_name", "last_name", "city", "zip", "state"]
      }
    }

###Request

'PUT /_enrich/policy/<enrich-policy>'

###Prerequisites

如果您使用 Elasticsearch 安全功能，则必须具备：

* 使用的任何索引的"读取"索引权限 * "enrich_user"内置角色

###Description

使用创建扩充策略 API 创建扩充策略。

创建后，无法更新或更改扩充策略。相反，您可以：

1. 创建并执行新的扩充策略。  2. 在任何正在使用的扩充处理器中，将以前的扩充策略替换为新的扩充策略。  3. 使用删除扩充策略 API 删除以前的扩充策略。

### 路径参数

`<enrich-policy>`

     (Required, string) Name of the enrich policy to create or update. 

### 请求正文

`<policy-type>`

    

(必填，对象)配置扩充策略。字段键是扩充策略类型。有效的键值为：

`geo_match`

     Matches enrich data to incoming documents based on a [`geo_shape` query](query-dsl-geo-shape-query.html "Geoshape query"). For an example, see [Example: Enrich your data based on geolocation](geo-match-enrich-policy-type.html "Example: Enrich your data based on geolocation"). 
`match`

     Matches enrich data to incoming documents based on a [`term` query](query-dsl-term-query.html "Term query"). For an example, see [Example: Enrich your data based on exact values](match-enrich-policy-type.html "Example: Enrich your data based on exact values"). 
`range`

     Matches a number, date, or IP address in incoming documents to a range in the enrich index based on a [`term` query](query-dsl-term-query.html "Term query"). For an example, see [Example: Enrich your data by matching a value to a range](range-enrich-policy-type.html "Example: Enrich your data by matching a value to a range"). 

""的属性<policy-type>

`indices`

    

(必需、字符串或字符串数组)用于创建扩充索引的一个或多个源索引。

如果指定了多个索引，则它们必须共享一个公共"match_field"。

`match_field`

     (Required, string) Field in source indices used to match incoming documents. 
`enrich_fields`

     (Required, Array of strings) Fields to add to matching incoming documents. These fields must be present in the source indices. 
`query`

     (Optional, [Query DSL query object](query-dsl.html "Query DSL")) Query used to filter documents in the enrich index. The policy only uses documents matching this query to enrich incoming documents. Defaults to a [`match_all`](query-dsl-match-all-query.html "Match all query") query. 

[« Enrich APIs](enrich-apis.md) [Delete enrich policy API »](delete-enrich-
policy-api.md)
