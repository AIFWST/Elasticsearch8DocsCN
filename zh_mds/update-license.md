

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Licensing APIs](licensing-apis.md)

[« Start basic API](start-basic.md) [Logstash APIs »](logstash-apis.md)

## 更新许可证接口

更新您的 Elasticsearch 集群的许可证。

###Request

"放_license"

"发布_license"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则需要"管理"集群权限才能安装许可证。  * 如果启用了 Elasticsearch 安全功能，并且您正在安装黄金或更高许可证，则在安装许可证之前，必须在传输网络层启用 TLS。请参阅使用 TLS 加密节点间通信。  * 如果启用了操作员权限功能，则只有操作员用户才能使用此 API。

###Description

您可以在运行时更新许可证，而无需关闭节点。许可证更新立即生效。但是，如果您要安装的许可证不支持先前许可证提供的所有功能，则会在响应中通知您。然后，您必须重新提交 API 请求，并将"确认"参数设置为"true"。

有关不同类型的许可证的详细信息，请参阅 seehttps://www.elastic.co/subscriptions。

### 查询参数

`acknowledge`

     (Optional, Boolean) Specifies whether you acknowledge the license changes. The default value is `false`. 

### 请求正文

`licenses`

     (Required, array) A sequence of one or more JSON documents containing the license information. 

###Examples

以下示例更新为基本许可证：

    
    
    PUT _license
    {
      "licenses": [
        {
          "uid":"893361dc-9749-4997-93cb-802e3d7fa4xx",
          "type":"basic",
          "issue_date_in_millis":1411948800000,
          "expiry_date_in_millis":1914278399999,
          "max_nodes":1,
          "issued_to":"issuedTo",
          "issuer":"issuer",
          "signature":"xx"
        }
        ]
    }

这些值无效;您必须替换许可证文件中的相应内容。

您也可以使用"curl"命令安装许可证文件。请务必在许可证文件路径之前添加"@"，以指示 curl 将其视为输入文件。

    
    
    curl -XPUT -u <user> 'http://<host>:<port>/_license' -H "Content-Type: application/json" -d @license.json

在 Windows 上，使用以下命令：

    
    
    Invoke-WebRequest -uri http://<host>:<port>/_license -Credential elastic -Method Put -ContentType "application/json" -InFile .\license.json

在这些示例中，

* '<user>' 是具有相应权限的用户 ID。  * '' 是 <host>Elasticsearch 集群中任何节点的主机名(如果在本地执行，则为"localhost") * '' 是 <port>http 端口(默认为 '9200') * 'license.json' 是许可证 JSON 文件

如果您的 Elasticsearch 节点在 HTTP 接口上启用了 SSL，则必须以"https://"开头 URL。

如果您以前拥有的功能比基本许可证更多功能的许可证，您将收到以下响应：

    
    
      {
      "acknowledged": false,
      "license_status": "valid",
      "acknowledge": {
        "message": """This license update requires acknowledgement. To acknowledge the license, please read the following messages and update the license again, this time with the "acknowledge=true" parameter:""",
        "watcher": [
          "Watcher will be disabled"
        ],
        "logstash": [
          "Logstash will no longer poll for centrally-managed pipelines"
        ],
        "security": [
          "The following X-Pack security functionality will be disabled: ..." ]
        }
    }

要完成更新，您必须重新提交 API 请求并将"确认"参数设置为"true"。例如：

    
    
    PUT _license?acknowledge=true
    {
      "licenses": [
        {
          "uid":"893361dc-9749-4997-93cb-802e3d7fa4xx",
          "type":"basic",
          "issue_date_in_millis":1411948800000,
          "expiry_date_in_millis":1914278399999,
          "max_nodes":1,
          "issued_to":"issuedTo",
          "issuer":"issuer",
          "signature":"xx"
        }
        ]
    }

Alternatively:

    
    
    curl -XPUT -u elastic 'http://<host>:<port>/_license?acknowledge=true' -H "Content-Type: application/json" -d @license.json

有关许可证到期时禁用的功能的详细信息，请参阅许可证过期。

[« Start basic API](start-basic.md) [Logstash APIs »](logstash-apis.md)
