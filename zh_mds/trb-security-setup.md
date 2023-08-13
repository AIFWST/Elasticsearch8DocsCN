

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Internal Server Error in Kibana](trb-security-internalserver.md)
[Failures due to relocation of the configuration files »](trb-security-
path.md)

## 设置密码命令由于连接失败而失败

elasticsearch-setup-password 命令通过发送用户管理 API 请求为内置用户设置密码。如果您的集群将 SSL/TLS 用于 HTTP (REST) 接口，则该命令会尝试与 HTTPS 协议建立连接。如果连接尝试失败，则该命令将失败。

**Symptoms:**

1. Elasticsearch 正在运行 HTTPS，但命令无法检测到它并返回以下错误：无法连接到 elasticsearch 节点。   java.net.SocketException：来自服务器的文件意外结束...   错误：无法在 http://127.0.0.1:9200/_security/_authenticate?pretty 连接到弹性搜索。   URL 是否正确且弹性搜索是否正在运行？

2. 已配置 SSL/TLS，但无法建立信任。该命令返回以下错误： 与 https://127.0.0.1:9200/_security/_authenticate?pretty 的 SSL 连接失败：sun.security.validator.ValidatorException：PKIX 路径构建失败：sun.security.provider.certpath.SunCertPathBuilder异常：无法找到请求目标的有效证书路径 请检查 xpack.security.http.ssl 下的 elasticsearch SSL 设置。   ...   错误：无法在 https://127.0.0.1:9200/_security/_authenticate?pretty 建立与弹性搜索的 SSL 连接。

3. 该命令失败，因为主机名验证失败，这会导致以下错误：与 https://idp.localhost.test:9200/_security/_authenticate?pretty 的 SSL 连接失败：java.security.cert.Certificate异常：未找到 elasticsearch.example.com 主题备用 DNS 名称匹配。   请检查 xpack.security.http.ssl 下的 elasticsearch SSL 设置。   ...   错误：无法在 https://elasticsearch.example.com:9200/_security/_authenticate?pretty 建立与弹性搜索的 SSL 连接。

**Resolution:**

1. 如果您的集群对 HTTP 接口使用 TLS/SSL，但"弹性搜索设置密码"命令尝试建立非安全连接，请使用"--url"命令选项显式指定 HTTPS URL。或者，将"xpack.security.http.ssl.enabled"设置设置为"true"。  2. 如果该命令不信任 Elasticsearch 服务器，请验证您是否配置了"xpack.security.http.ssl.certificate_authorities"设置或"xpack.security.http.ssl.truststore.path"设置。  3. 如果主机名验证失败，您可以通过将"xpack.security.http.ssl.verification_mode"设置为"证书"来禁用此验证。

有关这些设置的详细信息，请参阅安全设置。

[« Internal Server Error in Kibana](trb-security-internalserver.md)
[Failures due to relocation of the configuration files »](trb-security-
path.md)
