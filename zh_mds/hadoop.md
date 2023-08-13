

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Securing clients and
integrations](security-clients-integrations.md)

[« HTTP/REST clients and security](http-clients.md) [Monitoring and security
»](secure-monitoring.md)

## ES-Hadoop and Security

Elasticsearch for Apache Hadoop("ES-Hadoop")能够在访问Elasticsearch集群时使用HTTP basicand PKI身份验证和/或TLS/SSL。有关完整的详细信息，请参阅 ES-Hadoop 文档，特别是"安全性"部分。

出于身份验证目的，请为 ES-Hadoop 客户端选择用户(出于维护目的，最好创建一个专用用户)。然后，将该用户分配给具有 Hadoop/Spark/Storm 作业所需权限的角色。将 ES-Hadoop 配置为通过"es.net.http.auth.user"和"es.net.http.auth.pass"属性使用用户名和密码。

如果启用了 PKI 身份验证，请通过"es.net.ssl.keystore.location"和"es.net.truststore.location"(以及它们各自的".pass"属性来指定密码)设置相应的"密钥库"和"信任库"。

对于安全传输，请通过"es.net.ssl"属性启用 SSL/TLS，方法是将其设置为"true"。根据您的SSL配置(密钥库，信任库等)，您可能还需要设置其他参数 - 请参阅ES-Hadoop文档，特别是"配置"和"安全性"章节。

[« HTTP/REST clients and security](http-clients.md) [Monitoring and security
»](secure-monitoring.md)
