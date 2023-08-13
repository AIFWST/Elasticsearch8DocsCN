

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Update user profile data API](security-api-update-user-profile-data.md)
[Snapshot and restore APIs »](snapshot-restore-apis.md)

## 具有权限的用户配置文件API

用户配置文件功能仅供 Kibana 和 Elastic 的可观测性、企业级搜索和 Elastic 安全解决方案使用。个人用户和外部应用程序不应直接调用此 API。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

确定与指定用户配置文件标识关联的用户是否具有所有请求的权限。

###Request

'获取/_security/配置文件/_has_privileges"

"发布/_security/个人资料/_has_privileges"

###Prerequisites

要使用此 API，您必须具有_at least_"read_security"群集特权(或更大的特权，例如"manage_user_profile"或"manage_security")。

###Description

此 API 使用激活用户配置文件返回的配置文件 ID 来标识要检查其权限的用户。它类似于 Have privilegesAPI，但与它不同的是，此 API 检查其他用户的权限，而不是调用它的用户的特权。

有关可在此 API 中指定的权限列表，请参阅安全权限。

成功的调用将返回具有 **所有** 请求权限的配置文件 ID 的子集列表。

### 请求正文

`uids`

     (list) A list of [profile IDs](security-api-activate-user-profile.html#security-api-activate-user-profile-response-body "Response body"). The privileges are checked for associated users of the profiles. 
`privileges`

    

包含要检查的所有权限的对象。

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

     (list) A list of the privileges that you want to check for the specified resources. May be either application privilege names, or the names of actions that are granted by those privileges. 
`resources`

     (list) A list of resource names against which the privileges should be checked. 

请注意，上面的"权限"部分与其他具有权限 API 的请求正文相同。

### 响应正文

成功的具有权限用户配置文件 API 调用将返回包含两个字段的 JSON 结构：

`has_privilege_uids`

     (list) The subset of the requested profile IDs of the users that have **all** the requested privileges. 
`errors`

    

(对象)完成请求时遇到的错误。如果没有错误，则此字段不存在。它不包括不具有所有请求权限的用户的配置文件 ID。

"错误"中对象的属性

`count`

     (number) Total number of errors 
`details`

     (object) The detailed error report with keys being profile IDs and values being the exact errors. 

###Examples

以下示例检查与指定配置文件关联的两个用户是否具有所有请求的群集、索引和应用程序权限集：

    
    
    POST /_security/user/_has_privileges
    {
      "uids": [
        "u_LQPnxDxEjIH0GOUoFkZr5Y57YUwSkL9Joiq-g4OCbPc_0",
        "u_rzRnxDgEHIH0GOUoFkZr5Y27YUwSk19Joiq=g4OCxxB_1",
        "u_does-not-exist_0"
      ],
      "cluster": [ "monitor", "create_snapshot", "manage_ml" ],
      "index" : [
        {
          "names": [ "suppliers", "products" ],
          "privileges": [ "create_doc"]
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

以下示例输出指示三个用户中只有一个具有所有权限，并且找不到其中一个用户：

    
    
    {
      "has_privilege_uids": ["u_rzRnxDgEHIH0GOUoFkZr5Y27YUwSk19Joiq=g4OCxxB_1"],
      "errors": {
        "count": 1,
        "details": {
          "u_does-not-exist_0": {
            "type": "resource_not_found_exception",
            "reason": "profile document not found"
          }
        }
      }
    }

[« Update user profile data API](security-api-update-user-profile-data.md)
[Snapshot and restore APIs »](snapshot-restore-apis.md)
