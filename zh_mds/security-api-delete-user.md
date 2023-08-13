

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Delete service account tokens API](security-api-delete-service-token.md)
[Disable users API »](security-api-disable-user.md)

## 删除用户接口

从本机领域中删除用户。

###Request

"删除/_security/用户/<username>"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`username`

     (Required, string) An identifier for the user. 

###Examples

以下示例删除用户"jacknich"：

    
    
    DELETE /_security/user/jacknich

如果成功删除用户，请求将返回"{"找到"：true}"。否则，"已找到"将设置为 false。

    
    
    {
      "found" : true
    }

[« Delete service account tokens API](security-api-delete-service-token.md)
[Disable users API »](security-api-disable-user.md)
