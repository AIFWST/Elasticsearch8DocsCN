

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Built-in users](built-in-users.md) [Internal users »](internal-
users.md)

## 服务帐户

Elastic Stack 安全功能专门针对与连接到 Elasticsearch 的外部服务(如 Fleet 服务器)集成提供了_service accounts_。服务帐户具有一组固定的权限，并且在为它们创建服务帐户令牌之前无法进行身份验证。此外，服务帐户在代码中预定义，并且始终处于启用状态。

服务帐户对应于特定的外部服务。为服务帐户创建服务帐户令牌。然后，该服务可以使用令牌进行身份验证并执行相关操作。例如，Fleetserver 可以使用其服务令牌通过 Elasticsearch 进行身份验证，然后管理自己的 API 密钥。

您可以为同一服务帐户创建多个服务令牌，从而防止在同一外部服务的多个实例之间共享凭据。每个实例都可以采用相同的标识，同时使用其自己的不同服务令牌进行身份验证。

与内置用户相比，服务帐户提供了灵活性，因为它们：

* 不依赖于内部"本机"领域，也并不总是需要依赖".security"索引 * 使用以服务帐户主体命名的角色描述符，而不是传统角色 * 通过服务帐户令牌支持多个凭据

服务帐户不包括在获取用户 API 的响应中。若要检索服务帐户，请使用获取服务帐户 API。使用获取服务帐户凭据 API 检索服务帐户的所有服务凭据。

### 服务帐户使用情况

服务帐户具有唯一的主体，其格式为"/"，其中"命名空间"是服务<namespace><service>帐户的顶级分组，"服务"是服务的名称，并且在其命名空间中必须是唯一的。

服务帐户在代码中预定义。以下服务帐户可用：

`elastic/fleet-server`

     The service account used by the Fleet server to communicate with Elasticsearch. 
`elastic/kibana`

     The service account used by Kibana to communicate with Elasticsearch. 
`elastic/enterprise-search-server`

     The service account used by Enterprise Search to communicate with Elasticsearch. 

不要尝试使用服务帐户对单个用户进行身份验证。服务帐户只能使用服务令牌进行身份验证，这不适用于普通用户。

### 服务帐户令牌

服务帐户令牌或服务令牌是服务用于向 Elasticsearch 进行身份验证的唯一字符串。对于给定的服务帐户，每个令牌必须具有唯一的名称。由于令牌包含访问凭据，因此使用令牌的任何客户端都应始终对它们保密。

服务令牌可以由".security"索引(推荐)或"service_tokens"文件支持。您可以为单个服务帐户创建多个服务令牌，这样就可以使用不同的凭据运行同一服务的多个实例。

必须创建服务令牌才能使用服务帐户。您可以使用以下任一方式创建服务令牌：

* 创建服务帐户令牌 API，它将新的服务令牌保存在".security"索引中，并在 HTTP 响应中返回持有者令牌。  * 弹性搜索服务令牌 CLI 工具，它将新的服务令牌保存在 '$ES_HOME/config/service_tokens' 文件中，并将持有者令牌输出到您的终端

我们建议您通过 REST API 而不是 CLI 创建服务令牌。API 将服务令牌存储在".security"索引中，这意味着令牌可用于所有节点上的身份验证，并将在群集快照中备份。CLI 的使用适用于存在外部编排流程(例如 Elastic CloudEnterprise 或 Elastic Cloud onKubernetes)来管理"service_tokens"文件的创建和分发的情况。

这两种方法(API 和 CLI)都会创建保证机密字符串长度为"22"的服务令牌。服务令牌的机密字符串的最小可接受长度为"10"。如果机密字符串不符合此最小长度，则使用 Elasticsearch 进行身份验证将失败，甚至不会检查服务令牌的值。

服务令牌永不过期。如果不再需要它们，则必须主动删除它们。

### 使用服务令牌进行身份验证

服务帐户当前不支持基本身份验证。

要使用服务帐号令牌，请在请求中包含生成的令牌值，标头为"授权：持有者"：

    
    
    curl -H "Authorization: Bearer AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ" http://localhost:9200/_security/_authenticate

成功的身份验证响应包括一个"令牌"字段，其中包含一个用于服务令牌名称的"name"字段和一个用于服务令牌类型的"类型"字段：

    
    
    {
      "username": "elastic/fleet-server",
      "roles": [],
      "full_name": "Service account - elastic/fleet-server",
      "email": null,
      "token": {
        "name": "token1",                 __"type": "_service_account_index" __},
      "metadata": {
        "_elastic_service_account": true
      },
      "enabled": true,
      "authentication_realm": {
        "name": "_service_account",
        "type": "_service_account"
      },
      "lookup_realm": {
        "name": "_service_account",
        "type": "_service_account"
      },
      "authentication_type": "token"
    }

__

|

服务帐户令牌的名称。   ---|---    __

|

服务帐户令牌的类型。该值始终以"_service_account_"开头，后跟一个字符串，指示正在使用的服务令牌后端(可以是"文件"或"索引")。   « 内置用户 内部用户 »