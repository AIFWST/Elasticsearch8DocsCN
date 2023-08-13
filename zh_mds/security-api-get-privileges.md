

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get API key information API](security-api-get-api-key.md) [Get builtin
privileges API »](security-api-get-builtin-privileges.md)

## 获取应用程序权限API

检索应用程序权限。

###Request

"获取/_security/特权"

'获取/_security/特权/<application>'

'获取/_security/特权/<application>/<privilege>'

###Prerequisites

若要使用此 API，必须具有以下任一条件：

* "read_security"群集权限(或更大的权限，如"manage_security"或"全部");_or_ * 请求中引用的应用程序的 _"管理应用程序权限"_ 全局权限

###Description

要检查用户的应用程序权限，请使用具有权限 API。

### 路径参数

`application`

     (Optional, string) The name of the application. Application privileges are always associated with exactly one application. If you do not specify this parameter, the API returns information about all privileges for all applications. 
`privilege`

     (Optional, string) The name of the privilege. If you do not specify this parameter, the API returns information about all privileges for the requested application. 

###Examples

下面的示例检索有关"app01"应用程序的"读取"权限的信息：

    
    
    GET /_security/privilege/myapp/read

成功的调用将返回由应用程序名称和权限名称键控的对象。如果未定义权限，则请求将以 404 状态进行响应。

    
    
    {
      "myapp": {
        "read": {
          "application": "myapp",
          "name": "read",
          "actions": [
            "data:read/*",
            "action:login"
          ],
          "metadata": {
            "description": "Read access to myapp"
          }
        }
      }
    }

要检索应用程序的所有权限，请省略权限名称：

    
    
    GET /_security/privilege/myapp/

要检索每个权限，请省略应用程序和权限名称：

    
    
    GET /_security/privilege/

[« Get API key information API](security-api-get-api-key.md) [Get builtin
privileges API »](security-api-get-builtin-privileges.md)
