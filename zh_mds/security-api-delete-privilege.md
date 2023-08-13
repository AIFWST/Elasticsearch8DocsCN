

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Delegate PKI authentication API](security-api-delegate-pki-
authentication.md) [Delete role mappings API »](security-api-delete-role-
mapping.md)

## 删除应用程序权限API

删除应用程序权限。

###Request

"删除/_security/特权/<application>/<privilege>"

###Prerequisites

若要使用此 API，必须具有以下任一条件：

* "manage_security"群集权限(或更大的权限，如"全部");_or_ * 请求中引用的应用程序的 _"管理应用程序权限"_ 全局权限

### 路径参数

`application`

     (Required, string) The name of the application. Application privileges are always associated with exactly one application. 
`privilege`

     (Required, string) The name of the privilege. 

###Examples

以下示例从"myapp"应用程序中删除"读取"应用程序权限：

    
    
    DELETE /_security/privilege/myapp/read

如果成功删除权限，请求将返回"{"找到"：true}"。否则，"已找到"将设置为 false。

    
    
    {
      "myapp": {
        "read": {
          "found" : true
        }
      }
    }

[« Delegate PKI authentication API](security-api-delegate-pki-
authentication.md) [Delete role mappings API »](security-api-delete-role-
mapping.md)
