

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Certificate verification fails for curl on Mac](trb-security-maccurl.md)
[Common SSL/TLS exceptions »](trb-security-ssl.md)

## SSLHandshakeException 导致连接失败

**Symptoms:**

* "SSLHandshakeException"会导致与节点的连接失败，并指示存在配置问题。下面显示了一些常见的异常情况，并提供了有关如何解决这些问题的提示。

**Resolution:**

'java.security.cert.CertificateException： No name match node01.example.comfound'

    

指示已与"node01.example.com"建立了客户端连接，但返回的证书不包含名称"node01.example.com"。在大多数情况下，可以通过确保在创建证书期间指定名称来解决此问题。有关详细信息，请参阅使用 TLS 加密节点间通信。另一种情况是当环境根本不希望在证书中使用 DNS 名称时。在这种情况下，"elasticsearch.yml"中的所有设置都应仅使用IP地址，包括"network.publish_host"设置。

'java.security.cert.CertificateException： no Subject alternative namespresent'

    

指示客户端连接到 IP 地址，但返回的证书不包含任何"主题可选名称"条目。IP 地址仅在证书创建期间指定为"主题备用名称"时用于主机名验证。如果目的是使用 IP 地址进行主机名验证，则需要使用适当的 IP 地址重新生成证书。请参阅使用 TLS 加密节点间通信。

'javax.net.ssl.SSLHandshakeException： null cert chain' 和 'javax.net.ssl.SSLException： 收到致命警报： bad_certificate'

    

"SSLHandshakeException"表示客户端返回了不受信任的自签名证书，因为它在"信任库"或"密钥库"中找不到。这种"SSLException"在连接的客户端上可见。

"sun.security.provider.certpath.SunCertPathBuilderException： 无法找到所请求目标的有效证书路径"和"javax.net.ssl.SSLException：收到致命警报：certificate_unknown"

    

此"SunCertPathBuilderException"表示在握手期间返回了不受信任的证书。此消息显示在连接的客户端上。"SSLException"显示在连接的服务器端。在"密钥库"或"信任库"中找不到签署返回证书的 CA 证书，需要添加该证书才能信任此证书。

'javax.net.ssl.SSLHandshakeException： Invalid ECDH ServerKeyExchangesignature'

    

"无效的 ECDH 服务器密钥交换签名"可能表示密钥和相应的证书不匹配，并导致握手失败。验证用于配置的证书颁发机构、证书和密钥的每个文件的内容。特别是，检查密钥和证书是否属于同一密钥对。

[« Certificate verification fails for curl on Mac](trb-security-maccurl.md)
[Common SSL/TLS exceptions »](trb-security-ssl.md)
