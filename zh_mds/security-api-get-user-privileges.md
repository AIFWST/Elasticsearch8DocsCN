

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get token API](security-api-get-token.md) [Get users API »](security-api-
get-user.md)

## 获取用户权限API

检索登录用户的安全权限。

###Request

"获取/_security/用户/_privileges"

###Prerequisites

* 所有用户都可以使用此 API，但只能确定自己的权限。若要检查其他用户的权限，必须使用运行方式功能。有关更多信息，请参阅代表其他用户提交请求。

###Description

要检查用户是否具有特定的权限列表，请使用 hasprivileges API。

###Examples

    
    
    GET /_security/user/_privileges
    
    
    {
      "cluster" : [
        "all"
      ],
      "global" : [ ],
      "indices" : [
        {
          "names" : [
            "*"
          ],
          "privileges" : [
            "all"
          ],
          "allow_restricted_indices" : true
        }
      ],
      "applications" : [
        {
          "application" : "*",
          "privileges" : [
            "*"
          ],
          "resources" : [
            "*"
          ]
        }
      ],
      "run_as" : [
        "*"
      ]
    }

[« Get token API](security-api-get-token.md) [Get users API »](security-api-
get-user.md)
