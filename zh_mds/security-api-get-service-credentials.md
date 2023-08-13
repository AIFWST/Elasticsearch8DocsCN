

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get service accounts API](security-api-get-service-accounts.md) [Get
token API »](security-api-get-token.md)

## 获取服务帐户凭据API

检索服务帐户的所有服务凭据。

###Request

'GET /_security/service/<namespace>/<service>/credential'

###Prerequisites

* 要使用此 API，您必须至少具有"read_security"群集权限(或更大的权限，例如"manage_service_account"或"manage_security")。

###Description

使用此 API 检索服务帐户的凭据列表。响应包括使用 createservice 帐户令牌 API 创建的服务帐户令牌，以及来自群集所有节点的文件支持的令牌。

对于由"service_tokens"文件支持的令牌，API 从群集的所有节点收集它们。来自不同节点的同名令牌假定为同一令牌，并且仅计入服务令牌总数一次。

### 路径参数

`namespace`

     (Required, string) Name of the namespace. 
`service`

     (Required, string) Name of the service name. 

###Examples

以下请求使用创建服务帐户令牌 API 在"弹性/队列服务器"服务帐户中创建名为"token1"的服务帐户令牌：

    
    
    POST /_security/service/elastic/fleet-server/credential/token/token1

以下请求返回"弹性/队列服务器"服务帐户的所有凭据：

    
    
    GET /_security/service/elastic/fleet-server/credential

响应包括与指定服务帐户相关的所有凭据：

    
    
    {
      "service_account": "elastic/fleet-server",
      "count": 3,
      "tokens": {
        "token1": {},        __"token42": {} __},
      "nodes_credentials": { __"_nodes": { __"total": 3,
          "successful": 3,
          "failed": 0
        },
        "file_tokens": { __"my-token": {
            "nodes": [ "node0", "node1" ] __}
        }
      }
    }

__

|

由".security"索引 ---|--- __ 支持的新服务帐户令牌

|

由".security"索引 __ 支持的现有服务帐户令牌

|

本部分包含从群集的所有节点收集的服务帐户凭据 __

|

显示节点如何响应上述收集请求的常规状态 __

|

从所有节点收集的文件支持的令牌 __

|

找到(文件支持的)"my-token"的节点列表 « 获取服务帐户 API 获取令牌 API »