

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Users are frequently locked out of Active Directory](trouble-shoot-active-
directory.md) [SSLHandshakeException causes connections to fail »](trb-
security-sslhandshake.md)

## Mac 上的 curl 证书验证失败

**Symptoms:**

* Mac 上的"curl"返回证书验证错误，即使使用"--cacert"选项也是如此。

**Resolution:**

苹果将"curl"与其钥匙串技术集成，禁用了"--cacert"选项。有关详细信息，请参阅<http://curl.haxx.se/mail/archive-2013-10/0036.html>。

您可以使用其他工具(例如"wget")来测试证书。或者，您可以使用类似于 Apple知识库中详细介绍的过程为签名证书颁发机构 MacOS 系统钥匙串添加证书。请务必添加签名 CA 的证书，而不是服务器的证书。

[« Users are frequently locked out of Active Directory](trouble-shoot-active-
directory.md) [SSLHandshakeException causes connections to fail »](trb-
security-sslhandshake.md)
