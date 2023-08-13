

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Delete users API](security-api-delete-user.md) [Enable users API
»](security-api-enable-user.md)

## 禁用用户接口

禁用本机域中的用户。

###Request

"放置/_security/用户/<username>/_disable"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

默认情况下，创建用户时，这些用户处于启用状态。您可以使用此 API 来控制用户对 Elasticsearch 的访问权限。要重新启用用户，可以使用启用用户 API。

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`username`

     (Required, string) An identifier for the user. 

###Examples

以下示例禁用用户"jacknich"：

    
    
    PUT /_security/user/jacknich/_disable

[« Delete users API](security-api-delete-user.md) [Enable users API
»](security-api-enable-user.md)
