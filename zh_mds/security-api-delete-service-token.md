

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Delete roles API](security-api-delete-role.md) [Delete users API
»](security-api-delete-user.md)

## 删除服务帐号令牌API

删除指定"命名空间"中"服务"的服务帐户令牌。

###Request

`DELETE
/_security/service/<namespace>/<service>/credential/token/<token_name>`

###Prerequisites

* 要使用此 API，您必须至少具有"manage_service_account"群集权限。

###Description

API 响应指示是找到并删除指定的服务帐户令牌，还是找不到该令牌。

### 路径参数

`namespace`

     (Required, string) Name of the namespace. 
`service`

     (Required, string) Name of the service name. 
`token_name`

     (Required, string) Name of the service account token. 

###Examples

以下请求从"弹性/队列服务器"服务帐户中删除"token1"服务帐户令牌：

    
    
    DELETE /_security/service/elastic/fleet-server/credential/token/token42

如果成功删除服务帐户令牌，请求将返回"{"找到"：true}"。否则，响应的状态代码为"404"，发现"将设置为"false"。

    
    
    {
      "found" : true
    }

[« Delete roles API](security-api-delete-role.md) [Delete users API
»](security-api-delete-user.md)
