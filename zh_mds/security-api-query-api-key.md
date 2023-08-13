

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« OpenID Connect logout API](security-api-oidc-logout.md) [Update API key
API »](security-api-update-api-key.md)

## 查询 API 密钥信息API

以分页方式检索具有查询 DSL 的 API 密钥的信息。

###Request

"获取/_security/_query/api_key"

"发布/_security/_query/api_key"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_own_api_key"或"read_security"群集权限。  * 如果您只有"manage_own_api_key"权限，则此 API 仅返回您拥有的 API 密钥。如果您拥有"read_security"、"manage_api_key"或更高权限(包括"manage_security")，则此 API 将返回所有 API 密钥，无论所有权如何。

###Description

使用此 API 以分页方式检索使用创建 API 密钥 API 创建的 API 密钥。您可以选择使用查询筛选结果。

### 路径参数

`with_limited_by`

     (Optional, Boolean) A boolean flag to return the snapshot of the owner user's role descriptors associated with the API key. An API key's actual permission is the intersection of its [assigned role descriptors](security-api-create-api-key.html#api-key-role-descriptors) and the owner user's role descriptors (effectively limited by it). An API key cannot retrieve any API key's limited-by role descriptors (including itself) unless it has `manage_api_key` or higher privileges. 

### 请求正文

您可以在请求正文中指定以下参数：

`query`

    

(可选，字符串)用于筛选要返回的 API 密钥的查询。查询支持查询类型的子集，包括"match_all"、"布尔"、"术语"、"术语"、"id"、"前缀"、"通配符"、"存在"和"范围"。

您可以查询以下与 API 密钥关联的公有值。

"查询"的有效值

`id`

     ID of the API key. Note `id` must be queried with the [`ids`](query-dsl-ids-query.html "IDs") query. 
`name`

     Name of the API key. 
`creation`

     Creation time of the API key in milliseconds. 
`expiration`

     Expiration time of the API key in milliseconds. 
`invalidated`

     Indicates whether the API key is invalidated. If `true`, the key is invalidated. Defaults to `false`. 
`username`

     Username of the API key owner. 
`realm`

     Realm name of the API key owner. 
`metadata`

     Metadata field associated with the API key, such as `metadata.my_field`. Because metadata is stored as a [flattened](flattened.html "Flattened field type") field type, all fields act like `keyword` fields when querying and sorting. 

您无法查询 API 密钥的角色描述符。

`from`

    

(可选，整数)起始文档偏移量。需要为非负数并默认为"0"。

默认情况下，您不能使用"发件人"和"大小"参数翻阅超过 10，000 次点击。要翻阅更多点击，请使用"search_after"参数。

`size`

    

(可选，整数)要返回的命中数。不得为负数，默认为"10"。

默认情况下，您不能使用"发件人"和"大小"参数翻阅超过 10，000 次点击。要翻阅更多点击，请使用"search_after"参数。

`sort`

     (Optional, object) [Sort definition](sort-search-results.html "Sort search results"). Other than `id`, all public fields of an API key are eligible for sorting. In addition, sort can also be applied to the `_doc` field to sort by index order. 
`search_after`

     (Optional, array) [Search after](paginate-search-results.html#search-after "Search after") definition. 

### 响应正文

此 API 返回以下顶级字段：

`total`

     The total number of API keys found. 
`count`

     The number of API keys returned in the response. 
`api_keys`

     A list of API key information. 

###Examples

以下请求列出了所有 API 密钥，假设您具有"manage_api_key"权限：

    
    
    GET /_security/_query/api_key

成功的调用会返回一个 JSON 结构，其中包含从一个或多个 API 密钥检索的信息：

    
    
    {
      "total": 3,
      "count": 3,
      "api_keys": [ __{
          "id": "nkvrGXsB8w290t56q3Rg",
          "name": "my-api-key-1",
          "creation": 1628227480421,
          "expiration": 1629091480421,
          "invalidated": false,
          "username": "elastic",
          "realm": "reserved",
          "metadata": {
            "letter": "a"
          },
          "role_descriptors": { __"role-a": {
              "cluster": [
                "monitor"
              ],
              "indices": [
                {
                  "names": [
                    "index-a"
                  ],
                  "privileges": [
                    "read"
                  ],
                  "allow_restricted_indices": false
                }
              ],
              "applications": [ ],
              "run_as": [ ],
              "metadata": { },
              "transient_metadata": {
                "enabled": true
              }
            }
          }
        },
        {
          "id": "oEvrGXsB8w290t5683TI",
          "name": "my-api-key-2",
          "creation": 1628227498953,
          "expiration": 1628313898953,
          "invalidated": false,
          "username": "elastic",
          "realm": "reserved",
          "metadata": {
            "letter": "b"
          },
          "role_descriptors": { } __}
      ]
    }

__

|

为此请求检索的 API 密钥列表 ---|--- __

|

创建或上次更新时分配给此 API 密钥的角色描述符。请注意，API 密钥的有效权限是其分配的权限和所有者用户权限的时间点快照的交集。   __

|

空角色描述符表示 API 密钥继承所有者用户的权限。   如果您创建具有以下详细信息的 API 密钥：

    
    
    POST /_security/api_key
    {
      "name": "application-key-1",
      "metadata": { "application": "my-application"}
    }

成功的调用会返回提供 API 密钥信息的 JSON 结构。例如：

    
    
    {
      "id": "VuaCfGcBCdbkQm-e5aOx",
      "name": "application-key-1",
      "api_key": "ui2lp2axTNmsyakw9tvNnw",
      "encoded": "VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw=="
    }

使用响应中的信息按 ID 检索 API 密钥：

    
    
    GET /_security/_query/api_key?with_limited_by=true
    {
      "query": {
        "ids": {
          "values": [
            "VuaCfGcBCdbkQm-e5aOx"
          ]
        }
      }
    }

成功的调用会返回 API 密钥信息的 JSON 结构，包括其受角色限制的描述符：

    
    
    {
      "api_keys": [
        {
          "id": "VuaCfGcBCdbkQm-e5aOx",
          "name": "application-key-1",
          "creation": 1548550550158,
          "expiration": 1548551550158,
          "invalidated": false,
          "username": "myuser",
          "realm": "native1",
          "metadata": {
            "application": "my-application"
          },
          "role_descriptors": { },
          "limited_by": [ __{
              "role-power-user": {
                "cluster": [
                  "monitor"
                ],
                "indices": [
                  {
                    "names": [
                      "*"
                    ],
                    "privileges": [
                      "read"
                    ],
                    "allow_restricted_indices": false
                  }
                ],
                "applications": [ ],
                "run_as": [ ],
                "metadata": { },
                "transient_metadata": {
                  "enabled": true
                }
              }
            }
          ]
        }
      ]
    }

__

|

所有者用户与 API 密钥关联的权限。它是在创建和后续更新时捕获的时间点快照。API 密钥的有效权限是其分配的权限和所有者用户权限的交集。   ---|--- 您还可以按名称检索 API 密钥：

    
    
    GET /_security/_query/api_key
    {
      "query": {
        "term": {
          "name": {
            "value": "application-key-1"
          }
        }
      }
    }

使用"bool"查询发出复杂的逻辑条件，并使用"from"，"size"，"sort"来帮助对结果进行分页：

    
    
    GET /_security/_query/api_key
    {
      "query": {
        "bool": {
          "must": [
            {
              "prefix": {
                "name": "app1-key-" __}
            },
            {
              "term": {
                "invalidated": "false" __}
            }
          ],
          "must_not": [
            {
              "term": {
                "name": "app1-key-01" __}
            }
          ],
          "filter": [
            {
              "wildcard": {
                "username": "org-*-user" __}
            },
            {
              "term": {
                "metadata.environment": "production" __}
            }
          ]
        }
      },
      "from": 20, __"size": 10, __"sort": [ __{ "creation": { "order": "desc", "format": "date_time" } },
        "name"
      ]
    }

__

|

API 密钥名称必须以"app1-key-"开头---|--- __

|

API 密钥必须仍然有效 __

|

API 密钥名称不得为"app1-key-01"__

|

API 密钥必须由通配符模式"org-*-user"__ 的用户名拥有

|

API 密钥必须具有值为"生产"__ 的元数据字段"环境"

|

搜索结果开头的偏移量是第 20 个(从零开始的索引)API 键 __

|

响应的页面大小为 10 个 API 密钥 __

|

结果首先按"创建"日期降序排序，然后按名称升序排序 响应包含匹配的 API 键列表及其排序值：

    
    
    {
      "total": 100,
      "count": 10,
      "api_keys": [
        {
          "id": "CLXgVnsBOGkf8IyjcXU7",
          "name": "app1-key-79",
          "creation": 1629250154811,
          "invalidated": false,
          "username": "org-admin-user",
          "realm": "native1",
          "metadata": {
            "environment": "production"
          },
          "role_descriptors": { },
          "_sort": [
            "2021-08-18T01:29:14.811Z",  __"app1-key-79" __]
        },
        {
          "id": "BrXgVnsBOGkf8IyjbXVB",
          "name": "app1-key-78",
          "creation": 1629250153794,
          "invalidated": false,
          "username": "org-admin-user",
          "realm": "native1",
          "metadata": {
            "environment": "production"
          },
          "role_descriptors": { },
          "_sort": [
            "2021-08-18T01:29:13.794Z",
            "app1-key-78"
          ]
        },
        ...
      ]
    }

__

|

第一个排序值是创建时间，它以请求 ---|--- __ 中定义的"date_time"格式显示

|

第二个排序值是 API 密钥名称 您可以使用以下请求来检索所有有效的 API 密钥，即已失效且未过期的密钥：

    
    
    GET /_security/_query/api_key
    {
      "query": {
        "bool": {
          "must": {
            "term": {
              "invalidated": false  __}
          },
          "should": [ __{
              "range": {
                "expiration": {
                  "gte": "now"
                }
              }
            },
            {
              "bool": {
                "must_not": {
                  "exists": {
                    "field": "expiration"
                  }
                }
              }
            }
          ],
          "minimum_should_match": 1
        }
      }
    }

__

|

匹配的 API 密钥不得失效 ---|--- __

|

匹配的 API 密钥必须未过期或没有过期日期 « OpenID 连接注销 API 更新 API 密钥API »