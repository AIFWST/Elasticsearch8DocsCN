

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Enroll Kibana API](security-api-kibana-enrollment.md) [Get API key
information API »](security-api-get-api-key.md)

## 注册节点接口

允许新节点加入启用了安全功能的现有群集。

###Request

'GET /_security/enroll/node'

###Description

注册节点 API 的目的是允许新节点加入启用了安全性的现有群集。注册节点 API 响应包含加入节点的所有必要信息，以引导发现和安全相关设置，以便它可以成功加入集群。

响应包含密钥和证书材料，允许调用方为群集中所有节点的 HTTP 层生成有效的签名证书。

###Examples

    
    
    GET /security/enroll/node

API 返回一个响应，例如

    
    
    {
      "http_ca_key" : "MIIJlAIBAzCCCVoGCSqGSIb3DQEHAaCCCUsEgglHMIIJQzCCA98GCSqGSIb3DQ....vsDfsA3UZBAjEPfhubpQysAICCAA=", __"http_ca_cert" : "MIIJlAIBAzCCCVoGCSqGSIb3DQEHAaCCCUsEgglHMIIJQzCCA98GCSqGSIb3DQ....vsDfsA3UZBAjEPfhubpQysAICCAA=", __"transport_ca_cert" : "MIIJlAIBAzCCCVoGCSqGSIb3DQEHAaCCCUsEgglHMIIJQzCCA98GCSqG....vsDfsA3UZBAjEPfhubpQysAICCAA=", __"transport_key" : "MIIEJgIBAzCCA98GCSqGSIb3DQEHAaCCA9AEggPMMIIDyDCCA8QGCSqGSIb3....YuEiOXvqZ6jxuVSQ0CAwGGoA==", __"transport_cert" : "MIIEJgIBAzCCA98GCSqGSIb3DQEHAaCCA9AEggPMMIIDyDCCA8QGCSqGSIb3....YuEiOXvqZ6jxuVSQ0CAwGGoA==", __"nodes_addresses" : [ __"192.168.1.2:9300"
      ]
    }

__

|

新节点可用于对 HTTP 层的证书进行签名的 CA 私钥，作为密钥的 ASN.1 DERencoding 的 Base64 编码字符串。   ---|---    __

|

新节点可用于对 HTTP 层的证书进行签名的 CA 证书，作为证书的 ASN.1 DERencoding 的 Base64 编码字符串。   __

|

用于对传输层的 TLS 证书进行签名的 CA 证书，作为证书的 ASN.1 DER 编码的 Base64 编码字符串。   __

|

节点可用于其传输层的 TLS 的私钥，作为密钥的 ASN.1 DER 编码的 aBase64 编码字符串。   __

|

节点可用于其传输层的 TLS 的证书，作为证书的 ASN.1 DER 编码的 aBase64 编码字符串。   __

|

已是群集成员的节点的"host：port"形式的传输地址列表。   « 注册 Kibana API 获取 API 密钥信息 API »