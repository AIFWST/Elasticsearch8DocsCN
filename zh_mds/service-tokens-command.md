

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-saml-metadata](saml-metadata.md) [elasticsearch-setup-
passwords »](setup-passwords.md)

## 弹性搜索服务令牌

使用"弹性搜索服务令牌"命令创建、列出和删除基于文件的服务帐户令牌。

###Synopsis

    
    
    bin/elasticsearch-service-tokens
    ([create <service_account_principal> <token_name>]) |
    ([list] [<service_account_principal>]) |
    ([delete <service_account_principal> <token_name>])

###Description

管理服务令牌的建议方法是通过创建服务帐户令牌 API。基于文件的令牌旨在与编排器一起使用，例如 Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud

此命令在创建第一个服务帐户令牌时在"$ES_HOME/config"目录中创建一个"service_tokens"文件。默认情况下，此文件不存在。Elasticsearch 监控此文件的更改并动态重新加载它。

此命令仅对本地节点上的"service_tokens"文件进行更改。如果服务令牌将用于对群集中多个节点的请求进行身份验证，则必须将"service_tokens"文件复制到每个节点。

有关服务帐户的行为和服务令牌管理的详细信息，请参阅服务帐户。

要确保 Elasticsearch 可以在启动时读取服务帐户令牌信息，请以用于运行 Elasticsearch 的同一用户身份运行"elasticsearch-service-tokens"。以"root"或其他用户身份运行此命令会更新"service_tokens"文件的权限，并阻止 Elasticsearch 访问它。

###Parameters

`create`

    

为指定的服务帐户创建服务帐户令牌。

"创建"的属性

`<service_account_principal>`

    

(必需，字符串)采用"/"格式的服务帐户主体，<namespace><service>其中"命名空间"是服务帐户的顶级分组，"服务"是服务的名称。例如，"弹性/队列服务器"。

服务帐户主体必须与已知服务帐户匹配。

`<token_name>`

    

(必需，字符串)令牌名称的标识符。

令牌名称必须至少为 1 个字符且不超过 256 个字符。它们可以包含字母数字字符("a-z"、"A-Z"、"0-9")、短划线 ("-") 和下划线，但不能以下划线('_')开头。

令牌名称在关联的服务帐户的上下文中必须是唯一的。

`list`

    

列出"service_tokens"文件中定义的所有服务帐户令牌。如果指定服务帐户主体，则该命令仅列出属于指定服务帐户的令牌。

"列表"的属性

`<service_account_principal>`

    

(可选，字符串)采用"/"格式的服务帐户主体，<namespace><service>其中"命名空间"是服务帐户的顶级分组，"服务"是服务的名称。例如，"弹性/队列服务器"。

服务帐户主体必须与已知服务帐户匹配。

`delete`

    

删除指定服务帐户的服务帐户令牌。

"删除"的属性

`<service_account_principal>`

    

(必需，字符串)采用"/"格式的服务帐户主体，<namespace><service>其中"命名空间"是服务帐户的顶级分组，"服务"是服务的名称。例如，"弹性/队列服务器"。

服务帐户主体必须与已知服务帐户匹配。

`<token_name>`

     (Required, string) Name of an existing token. 

###Examples

以下命令为"弹性/队列服务器"服务帐户创建名为"my-token"的服务帐户令牌。

    
    
    bin/elasticsearch-service-tokens create elastic/fleet-server my-token

输出是一个持有者令牌，它是一个 Base64 编码的字符串。

    
    
    SERVICE_TOKEN elastic/fleet-server/my-token = AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ

使用此持有者令牌向您的 Elasticsearch 集群进行身份验证。

    
    
    curl -H "Authorization: Bearer AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ" http://localhost:9200/_cluster/health

如果您的节点将"xpack.security.http.ssl.enabled"设置为"true"，则必须在请求URL中指定"https"。

以下命令列出在"service_tokens"文件中定义的所有服务帐户令牌。

    
    
    bin/elasticsearch-service-tokens list

终端中将显示所有服务帐户令牌的列表：

    
    
    elastic/fleet-server/my-token
    elastic/fleet-server/another-token

以下命令删除"弹性/队列服务器"服务帐户的"my-token"服务帐户令牌：

    
    
    bin/elasticsearch-service-tokens delete elastic/fleet-server my-token

[« elasticsearch-saml-metadata](saml-metadata.md) [elasticsearch-setup-
passwords »](setup-passwords.md)
