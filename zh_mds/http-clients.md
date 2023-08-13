

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Securing clients and
integrations](security-clients-integrations.md)

[« Securing clients and integrations](security-clients-integrations.md) [ES-
Hadoop and Security »](hadoop.md)

## HTTP/REST 客户端和安全性

Elasticsearch 安全功能与标准 HTTP basicauthenticationheaders 配合使用，对用户进行身份验证。由于 Elasticsearch 是无状态的，因此必须随每个请求一起发送此标头：

    
    
    Authorization: Basic <TOKEN> __

__

|

""<TOKEN>计算为"base64(用户名：密码)"---|--- 或者，您可以使用基于令牌的身份验证服务。

#### 客户端示例

此示例使用不带基本身份验证的"curl"来创建索引：

    
    
    curl -XPUT 'localhost:9200/idx'
    
    
    {
      "error":  "AuthenticationException[Missing authentication token]",
      "status": 401
    }

由于没有用户与上述请求相关联，因此返回身份验证错误。现在我们将使用带有基本身份验证的"curl"来创建作为"rdeniro"用户的索引：

    
    
    curl --user rdeniro:taxidriver -XPUT 'localhost:9200/idx'
    
    
    {
      "acknowledged": true
    }

#### 辅助授权

某些 API 支持辅助授权标头，适用于您希望使用一组不同的凭据运行任务的情况。例如，除了基本身份验证标头之外，您还可以发送以下标头：

    
    
    es-secondary-authorization: Basic <TOKEN> __

__

|

""<TOKEN>计算为"base64(用户名：密码)"---|--- "es-secondary-authorization"标头与"授权"标头具有相同的语法。因此，它还支持使用基于令牌的身份验证服务。例如：

    
    
    es-secondary-authorization: ApiKey <TOKEN> __

__

|

"<TOKEN>"计算为"base64(API key ID：API key)" ---|--- #### 客户端库 overHTTPedit

有关将安全功能与特定于语言的客户端配合使用的详细信息，请参阅：

* Java * JavaScript * .NET * Perl * PHP * Python * Ruby

[« Securing clients and integrations](security-clients-integrations.md) [ES-
Hadoop and Security »](hadoop.md)
