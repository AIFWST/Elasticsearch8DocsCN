

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Disable users API](security-api-disable-user.md) [Enroll Kibana API
»](security-api-kibana-enrollment.md)

## 启用用户接口

启用本机域中的用户。

###Request

"放置/_security/用户/<username>/_enable"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

默认情况下，创建用户时，这些用户处于启用状态。您可以使用此启用用户 API 和禁用用户 API 来更改该属性。

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`username`

     (Required, string) An identifier for the user. 

###Examples

以下示例启用用户"jacknich"：

    
    
    PUT /_security/user/jacknich/_enable

[« Disable users API](security-api-disable-user.md) [Enroll Kibana API
»](security-api-kibana-enrollment.md)
