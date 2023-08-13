

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« SSLHandshakeException causes connections to fail](trb-security-
sslhandshake.md) [Common Kerberos exceptions »](trb-security-kerberos.md)

## 常见的 SSL/TLS 异常

**Symptoms:**

* 您可能会在日志中看到一些与 SSL/TLS 相关的异常。下面显示了一些常见的异常情况，并提供了有关如何解决这些问题的提示。 

**Resolution:**

"WARN：在 https 通道上收到明文 http 流量，正在关闭连接"

    

指示存在传入的纯文本 http 请求。当外部应用程序尝试对 REST 接口进行未加密的调用时，通常会发生这种情况。请确保所有应用程序在调用启用了 SSL 的 REST 接口时都使用"https"。

'org.elasticsearch.common.netty.handler.ssl.NotSslRecordException： not anSSL/TLS record：'

    

指示 SSL 连接上存在传入的明文通信。当节点未配置为使用加密通信并尝试连接到使用加密通信的节点时，通常会发生这种情况。请验证所有节点是否对"xpack.security.transport.ssl.enabled"使用相同的设置。

有关此设置的详细信息，请参阅安全设置。

'java.io.StreamCorruptedException： 无效的内部传输消息格式，got'

    

指示在传输接口上以未知格式接收的数据存在问题。当启用了加密通信的节点连接到已禁用加密通信的节点时，可能会发生这种情况。请验证所有节点是否对"xpack.security.transport.ssl.enabled"使用相同的设置。

有关此设置的详细信息，请参阅安全设置。

'java.lang.IllegalArgumentException： empty text'

    

当向不使用"https"的节点发出"https"请求时，通常会出现此异常。如果需要"https"，请确保在"elasticsearch.yml"中设置以下设置：

    
    
    xpack.security.http.ssl.enabled: true

有关此设置的详细信息，请参阅安全设置。

"错误：请求了不支持的密码 [...]，但不能在此JVM中使用"

    

当指定的 SSL/TLS 密码套件无法被运行 Elasticsearch 的 JVM 支持时，会发生此错误。安全性尝试使用此 JVM 支持的指定密码套件。使用安全默认值时可能会发生此错误，因为默认情况下，OpenJDK 的某些发行版不启用 PKCS11 提供程序。在这种情况下，我们建议查阅 JVM 文档，了解有关如何启用 PKCS11 提供程序的详细信息。

此错误的另一个常见来源是请求在 OracleJDK 上运行时使用密钥长度大于 128 位的加密的密码套件。在这种情况下，您必须安装 JCE 无限强度管辖策略文件。

[« SSLHandshakeException causes connections to fail](trb-security-
sslhandshake.md) [Common Kerberos exceptions »](trb-security-kerberos.md)
