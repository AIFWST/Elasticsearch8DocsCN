

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Grant API key API](security-api-grant-api-key.md) [Invalidate API key API
»](security-api-invalidate-api-key.md)

## 具有权限API

确定登录用户是否具有指定的权限列表。

###Request

'获取/_security/用户/_has_privileges"

"发布/_security/用户/_has_privileges"

###Prerequisites

* 所有用户都可以使用此 API，但只能确定自己的权限。若要检查其他用户的权限，必须使用运行方式功能。有关更多信息，请参阅代表其他用户提交请求。

###Description

有关可在此 API 中指定的权限的列表，请参阅安全权限。

成功的调用会返回一个 JSON 结构，该结构显示是否将每个指定的权限分配给用户。

### 请求正文

`cluster`

     (list) A list of the cluster privileges that you want to check. 
`index`

    

`names`

     (list) A list of indices. 
`allow_restricted_indices`

     (Boolean) This needs to be set to `true` (default is `false`) if using wildcards or regexps for patterns that cover restricted indices. Implicitly, restricted indices do not match index patterns because restricted indices usually have limited privileges and including them in pattern tests would render most such tests `false`. If restricted indices are explicitly included in the `names` list, privileges will be checked against them regardless of the value of `allow_restricted_indices`. 
`privileges`

     (list) A list of the privileges that you want to check for the specified indices. 

`application`

    

`application`

     (string) The name of the application. 
`privileges`

     (list) A list of the privileges that you want to check for the specified resources. May be either application privilege names, or the names of actions that are granted by those privileges 
`resources`

     (list) A list of resource names against which the privileges should be checked 

###Examples

以下示例检查当前用户是否具有一组特定的群集、索引和应用程序权限：

    
    
    GET /_security/user/_has_privileges
    {
      "cluster": [ "monitor", "manage" ],
      "index" : [
        {
          "names": [ "suppliers", "products" ],
          "privileges": [ "read" ]
        },
        {
          "names": [ "inventory" ],
          "privileges" : [ "read", "write" ]
        }
      ],
      "application": [
        {
          "application": "inventory_manager",
          "privileges" : [ "read", "data:write/inventory" ],
          "resources" : [ "product/1852563" ]
        }
      ]
    }

以下示例输出指示"rdeniro"用户具有哪些权限：

    
    
    {
      "username": "rdeniro",
      "has_all_requested" : false,
      "cluster" : {
        "monitor" : true,
        "manage" : false
      },
      "index" : {
        "suppliers" : {
          "read" : true
        },
        "products" : {
          "read" : true
        },
        "inventory" : {
          "read" : true,
          "write" : false
        }
      },
      "application" : {
        "inventory_manager" : {
          "product/1852563" : {
            "read": false,
            "data:write/inventory": false
          }
        }
      }
    }

[« Grant API key API](security-api-grant-api-key.md) [Invalidate API key API
»](security-api-invalidate-api-key.md)
