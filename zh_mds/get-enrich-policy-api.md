

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Enrich APIs](enrich-apis.md)

[« Delete enrich policy API](delete-enrich-policy-api.md) [Execute enrich
policy API »](execute-enrich-policy-api.md)

## 获取扩充策略接口

返回有关扩充策略的信息。

    
    
    response = client.enrich.get_policy(
      name: 'my-policy'
    )
    puts response
    
    
    GET /_enrich/policy/my-policy

###Request

'获取/_enrich/策略/<name>'

"获取/_enrich/策略"

'GET /_enrich/policy/policy1，policy2'

###Prerequisites

如果您使用 Elasticsearch 安全功能，则必须具备：

* 使用的任何索引的"读取"索引权限 * "enrich_user"内置角色

### 路径参数

`<name>`

    

(可选，字符串)用于限制请求的扩充策略名称的逗号分隔列表。

若要返回所有扩充策略的信息，请省略此参数。

###Examples

#### 获取单个策略

    
    
    response = client.enrich.get_policy(
      name: 'my-policy'
    )
    puts response
    
    
    GET /_enrich/policy/my-policy

API 返回以下响应：

    
    
    {
      "policies": [
        {
          "config": {
            "match": {
              "name": "my-policy",
              "indices": [ "users" ],
              "match_field": "email",
              "enrich_fields": [
                "first_name",
                "last_name",
                "city",
                "zip",
                "state"
              ]
            }
          }
        }
      ]
    }

#### 获取多个策略

    
    
    response = client.enrich.get_policy(
      name: 'my-policy,other-policy'
    )
    puts response
    
    
    GET /_enrich/policy/my-policy,other-policy

API 返回以下响应：

    
    
    {
      "policies": [
        {
          "config": {
            "match": {
              "name": "my-policy",
              "indices": [ "users" ],
              "match_field": "email",
              "enrich_fields": [
                "first_name",
                "last_name",
                "city",
                "zip",
                "state"
              ]
            }
          }
        },
        {
          "config": {
            "match": {
              "name": "other-policy",
              "indices": [ "users" ],
              "match_field": "email",
              "enrich_fields": [
                "first_name",
                "last_name",
                "city",
                "zip",
                "state"
              ]
            }
          }
        }
      ]
    }

#### 获取所有策略

    
    
    response = client.enrich.get_policy
    puts response
    
    
    GET /_enrich/policy

API 返回以下响应：

    
    
    {
      "policies": [
        {
          "config": {
            "match": {
              "name": "my-policy",
              "indices": [ "users" ],
              "match_field": "email",
              "enrich_fields": [
                "first_name",
                "last_name",
                "city",
                "zip",
                "state"
              ]
            }
          }
        },
        {
          "config": {
            "match": {
              "name": "other-policy",
              "indices": [ "users" ],
              "match_field": "email",
              "enrich_fields": [
                "first_name",
                "last_name",
                "city",
                "zip",
                "state"
              ]
            }
          }
        }
      ]
    }

[« Delete enrich policy API](delete-enrich-policy-api.md) [Execute enrich
policy API »](execute-enrich-policy-api.md)
