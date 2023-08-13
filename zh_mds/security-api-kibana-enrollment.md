

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Enable users API](security-api-enable-user.md) [Enroll Node API
»](security-api-node-enrollment.md)

## 注册 KibanaAPI

使 Kibana 实例能够自行配置自身，以便与安全的弹性搜索集群进行通信。

此 API 目前仅供 Kibana 内部使用。

###Request

'GET /_security/enroll/kibana'

###Description

Kibana 在内部使用此 API 来配置自身，以便与已启用安全功能的 Elasticsearch 集群进行通信。

###Examples

以下示例演示如何注册 Kibana 实例。

    
    
    GET /_security/enroll/kibana

API 返回以下响应：

    
    
    {
      "token" : {
        "name" : "enroll-process-token-1629123923000", __"value": "AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ" __},
      "http_ca" : "MIIJlAIBAzVoGCSqGSIb3...vsDfsA3UZBAjEPfhubpQysAICAA=", __}

__

|

"弹性/kibana"服务帐户的持有者令牌的名称。   ---|---    __

|

"弹性/kibana"服务帐户的持有者令牌的值。使用此值通过 Elasticsearch 对服务帐户进行身份验证。   __

|

用于签署 Elasticsearch 用于 HTTP 层 TLS 的节点证书的 CA 证书。证书作为证书的 ASN.1 DER 编码的 Base64 编码字符串返回。   « 启用用户 API 注册节点 API»