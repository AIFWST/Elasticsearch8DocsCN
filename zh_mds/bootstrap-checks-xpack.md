

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Discovery configuration check](_discovery_configuration_check.md)
[Starting Elasticsearch »](starting-elasticsearch.md)

## Bootstrap Check for X-Pack

除了 Elasticsearch 引导程序检查之外，还有特定于 X-Pack 功能的检查。

### 加密敏感数据检查

如果使用 Watcher 并选择加密敏感数据(通过将"xpack.watcher.encrypt_sensitive_data"设置为"true")，则还必须在安全设置存储中放置一个密钥。

要通过此引导程序检查，您必须在群集中的每个节点上设置"xpack.watcher.encryption_key"。有关详细信息，请参阅在观察程序中加密敏感数据。

### PKI 领域检查

如果使用 Elasticsearch 安全功能和公钥基础结构 (PKI) 领域，则必须在集群上配置传输层安全性 (TLS)，并在网络层(传输层或 http)上启用客户端身份验证。有关详细信息，请参阅 PKI 用户身份验证和设置基本安全性加 HTTPS。

要通过此引导程序检查，如果启用了 PKI 领域，则必须在至少一个网络通信层上配置 TLS 并启用客户端身份验证。

### 角色映射检查

如果使用"本机"或"文件"域以外的域对用户进行身份验证，则必须创建角色映射。这些角色映射定义哪些角色区域已签名给每个用户。

如果使用文件来管理角色映射，则必须配置 YAML 文件并将其复制到群集中的每个节点。默认情况下，角色映射存储在"ES_PATH_CONF/role_mapping.yml"中。或者，您可以为每种类型的领域指定一个不同的角色映射文件，并在 'elasticsearch.yml' 文件中指定它的位置。有关详细信息，请参阅使用角色映射文件。

若要通过此引导程序检查，角色映射文件必须存在且必须有效。角色映射文件中列出的可分辨名称 (DN) 也必须有效。

### SSL/TLScheck

如果您启用了 Elasticsearch 安全功能，除非您有试用许可证，否则您必须为 SSL/TLS 配置节点间通信。

使用环回接口的单节点群集没有此要求。有关更多信息，请参阅 _Start启用了安全性的弹性堆栈automatically_。

要通过此引导程序检查，您必须在集群中设置 SSL/TLS。

### 令牌 SSL检查

如果您使用 Elasticsearch 安全功能并且启用了内置令牌服务，则必须将集群配置为对 HTTP接口使用 SSL/TLS。要使用令牌服务，需要 HTTPS。

特别是，如果在"elasticsearch.yml"文件中将"xpack.security.authc.token.enabled"设置为"true"，则还必须将"xpack.security.http.ssl.enabled"设置为"true"。有关这些设置的详细信息，请参阅安全设置和高级 HTTP 设置。

若要通过此引导程序检查，必须启用 HTTPS 或禁用内置令牌服务。

[« Discovery configuration check](_discovery_configuration_check.md)
[Starting Elasticsearch »](starting-elasticsearch.md)
