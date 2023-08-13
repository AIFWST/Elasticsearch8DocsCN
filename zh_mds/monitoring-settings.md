

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Machine learning settings in Elasticsearch](ml-settings.md) [Node
»](modules-node.md)

## 弹性搜索中的监控设置

### 在 7.16 中已弃用。

不推荐使用 Elasticsearch 监控插件来收集和发送监控数据。Elastic 代理和 Metricbeat 是收集监控数据并将其传送到监控集群的推荐方法。如果您之前配置了旧版收集方法，则应迁移到使用 Elastic 代理或 Metricbeatcollection 方法。

默认情况下，Elasticsearch 监控功能处于启用状态，但数据收集处于禁用状态。要启用数据收集，请使用"xpack.monitoring.collection.enabled"设置。

除非另有说明，否则可以使用群集更新设置 API 在活动群集上动态更新这些设置。

要调整监控数据在监控 UI 中的显示方式，请在"kibana.yml"中配置"xpack.monitoring"设置。要控制如何从 Logstash 收集监控数据，请在"logstash.yml"中配置监控设置。

具体操作，请参见监控集群。

#### 常规监视设置

`xpack.monitoring.enabled`

     [7.8.0]  Deprecated in 7.8.0. Basic License features should always be enabled  ([Static](settings.html#static-cluster-setting)) This deprecated setting has no effect. 

#### 监视集合设置

"xpack.monitoring.collection"设置控制如何从Elasticsearch节点收集数据。

`xpack.monitoring.collection.enabled`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Set to `true` to enable the collection of monitoring data. When this setting is `false` (default), Elasticsearch monitoring data is not collected and all monitoring data from other sources such as Kibana, Beats, and Logstash is ignored. 

"xpack.monitoring.collection.interval"！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

6.3.0] 在 6.3.0 中已弃用。改用设置为"false"的"xpack.monitoring.collection.enabled"。 ([动态)从 7.0.0 开始，不再支持设置为"-1"以禁用数据收集。

控制收集数据样本的频率。默认为"10s"。如果修改收集间隔，请将"kibana.yml"中的"xpack.monitoring.min_interval_seconds"选项设置为相同值。

`xpack.monitoring.elasticsearch.collection.enabled`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Controls whether statistics about your Elasticsearch cluster should be collected. Defaults to `true`. This is different from `xpack.monitoring.collection.enabled`, which allows you to enable or disable all monitoring collection. However, this setting simply disables the collection of Elasticsearch data while still allowing other data (e.g., Kibana, Logstash, Beats, or APM Server monitoring data) to pass through this cluster. 
`xpack.monitoring.collection.cluster.stats.timeout`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Timeout for collecting the cluster statistics, in [time units](api-conventions.html#time-units "Time units"). Defaults to `10s`. 
`xpack.monitoring.collection.node.stats.timeout`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Timeout for collecting the node statistics, in [time units](api-conventions.html#time-units "Time units"). Defaults to `10s`. 
`xpack.monitoring.collection.indices`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Controls which indices the monitoring features collect data from. Defaults to all indices. Specify the index names as a comma-separated list, for example `test1,test2,test3`. Names can include wildcards, for example `test*`. You can explicitly exclude indices by prepending `-`. For example `test*,-test3` will monitor all indexes that start with `test` except for `test3`. System indices like .security* or .kibana* always start with a `.` and generally should be monitored. Consider adding `.*` to the list of indices ensure monitoring of system indices. For example: `.*,test*,-test3`
`xpack.monitoring.collection.index.stats.timeout`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Timeout for collecting index statistics, in [time units](api-conventions.html#time-units "Time units"). Defaults to `10s`. 
`xpack.monitoring.collection.index.recovery.active_only`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Controls whether or not all recoveries are collected. Set to `true` to collect only active recoveries. Defaults to `false`. 
`xpack.monitoring.collection.index.recovery.timeout`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API"))  [7.16.0]  Deprecated in 7.16.0.  Timeout for collecting the recovery information, in [time units](api-conventions.html#time-units "Time units"). Defaults to `10s`. 

"xpack.monitoring.history.duration"！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

(动态)7.16.0] 在 7.16.0 中已弃用。 保留期，超过该保留期，监视导出程序创建的索引将自动删除，以 [时间单位.默认为"7d"(7 天)。

此设置的最小值为"1d"(1 天)，以确保某些内容正在被监视并且无法禁用。

此设置目前仅影响"本地"类型的导出器。使用"http"导出器创建的索引不会自动删除。

`xpack.monitoring.exporters`

     ([Static](settings.html#static-cluster-setting)) Configures where the agent stores monitoring data. By default, the agent uses a local exporter that indexes monitoring data on the cluster where it is installed. Use an HTTP exporter to send data to a separate monitoring cluster. For more information, see [Local exporter settings](monitoring-settings.html#local-exporter-settings "Local exporter settings"), [HTTP exporter settings](monitoring-settings.html#http-exporter-settings "HTTP exporter settings"), and [_How it works_](how-monitoring-works.html "How monitoring works"). 

#### 本地导出器设置

"本地"导出器是监视功能使用的默认导出器。顾名思义，它将数据导出到 _local_ 集群，这意味着不需要太多配置。

如果您不提供 _any_ 导出器，则监控功能会自动为您创建一个。如果提供了任何导出器，则不添加默认值。

    
    
    xpack.monitoring.exporters.my_local:
      type: local

`type`

     [7.16.0]  Deprecated in 7.16.0.  The value for a Local exporter must always be `local` and it is required. 
`use_ingest`

     Whether to supply a placeholder pipeline to the cluster and a pipeline processor with every bulk request. The default value is `true`. If disabled, then it means that it will not use pipelines, which means that a future release cannot automatically upgrade bulk requests to future-proof them. 
`cluster_alerts.management.enabled`

     [7.16.0]  Deprecated in 7.16.0.  Whether to create cluster alerts for this cluster. The default value is `true`. To use this feature, Watcher must be enabled. If you have a basic license, cluster alerts are not displayed. 
`wait_master.timeout`

     [7.16.0]  Deprecated in 7.16.0.  Time to wait for the master node to setup `local` exporter for monitoring, in [time units](api-conventions.html#time-units "Time units"). After that wait period, the non-master nodes warn the user for possible missing configuration. Defaults to `30s`. 

#### HTTP 导出器设置

下面列出了可以通过"http"导出器提供的设置。所有设置都显示在您为导出器选择的名称后面：

    
    
    xpack.monitoring.exporters.my_remote:
      type: http
      host: ["host:port", ...]

`type`

     [7.16.0]  Deprecated in 7.16.0.  The value for an HTTP exporter must always be `http` and it is required. 
`host`

    

[7.16.0] 在 7.16.0 中已弃用。 主机支持多种格式，既可以是数组格式，也可以是单个值。支持的格式包括"主机名"、"主机名：端口"、"http://hostname"、"http：//hostname：port"、"https：//hostname"和"https：//hostname：port"。不能假定主机。默认方案始终为"http"，如果未作为"host"字符串的一部分提供，则默认端口始终为"9200"。

    
    
    xpack.monitoring.exporters:
      example1:
        type: http
        host: "10.1.2.3"
      example2:
        type: http
        host: ["http://10.1.2.4"]
      example3:
        type: http
        host: ["10.1.2.5", "10.1.2.6"]
      example4:
        type: http
        host: ["https://10.1.2.3:9200"]

`auth.username`

     [7.16.0]  Deprecated in 7.16.0.  The username is required if `auth.secure_password` is supplied. 
`auth.secure_password`

     ([Secure](secure-settings.html "Secure settings"), [reloadable](secure-settings.html#reloadable-secure-settings "Reloadable secure settings"))  [7.16.0]  Deprecated in 7.16.0.  The password for the `auth.username`. 
`connection.timeout`

     [7.16.0]  Deprecated in 7.16.0.  Amount of time that the HTTP connection is supposed to wait for a socket to open for the request, in [time units](api-conventions.html#time-units "Time units"). The default value is `6s`. 
`connection.read_timeout`

     [7.16.0]  Deprecated in 7.16.0.  Amount of time that the HTTP connection is supposed to wait for a socket to send back a response, in [time units](api-conventions.html#time-units "Time units"). The default value is `10 * connection.timeout` (`60s` if neither are set). 
`ssl`

     [7.16.0]  Deprecated in 7.16.0.  Each HTTP exporter can define its own TLS / SSL settings or inherit them. See [X-Pack monitoring TLS/SSL settings](monitoring-settings.html#ssl-monitoring-settings "X-Pack monitoring TLS/SSL settings"). 
`proxy.base_path`

     [7.16.0]  Deprecated in 7.16.0.  The base path to prefix any outgoing request, such as `/base/path` (e.g., bulk requests would then be sent as `/base/path/_bulk`). There is no default value. 
`headers`

    

[7.16.0] 在 7.16.0 中已弃用。 添加到每个请求的可选标头，可帮助通过代理路由请求。

    
    
    xpack.monitoring.exporters.my_remote:
      headers:
        X-My-Array: [abc, def, xyz]
        X-My-Header: abc123

基于数组的标头发送"n"次，其中"n"是数组的大小。无法设置"内容类型"和"内容长度"。监视代理创建的任何标头都将覆盖此处定义的任何内容。

`index.name.time_format`

     [7.16.0]  Deprecated in 7.16.0.  A mechanism for changing the default date suffix for daily monitoring indices. The default format is `yyyy.MM.dd`. For example, `.monitoring-es-7-2021.08.26`. 
`use_ingest`

     Whether to supply a placeholder pipeline to the monitoring cluster and a pipeline processor with every bulk request. The default value is `true`. If disabled, then it means that it will not use pipelines, which means that a future release cannot automatically upgrade bulk requests to future-proof them. 
`cluster_alerts.management.enabled`

     [7.16.0]  Deprecated in 7.16.0.  Whether to create cluster alerts for this cluster. The default value is `true`. To use this feature, Watcher must be enabled. If you have a basic license, cluster alerts are not displayed. 
`cluster_alerts.management.blacklist`

    

[7.16.0] 在 7.16.0 中已弃用。 阻止创建特定的群集警报。它还会删除当前群集中已存在的任何适用监视。

您可以将以下任何监视标识符添加到阻止警报列表中：

* "elasticsearch_cluster_status" * "elasticsearch_version_mismatch" * "elasticsearch_nodes" * "kibana_version_mismatch" * "logstash_version_mismatch" * "xpack_license_expiration"

例如："["elasticsearch_version_mismatch"，"xpack_license_expiration"]"。

### X-Pack 监控 TLS/SSL设置

您可以配置以下 TLS/SSL 设置。

`xpack.monitoring.exporters.$NAME.ssl.supported_protocols`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 支持的版本协议。有效协议："SSLv2Hello"、"SSLv3"、"TLSv1"、"TLSv1.1"、"TLSv1.2"、"TLSv1.3"。如果 JVM 的 SSL 提供程序支持 TLSv1.3，则缺省值为 'TLSv1.3，TLSv1.2，TLSv1.1'。否则，默认值为"TLSv1.2，TLSv1.1"。

Elasticsearch 依赖于 JDK 的 SSL 和 TLS 实现。有关详细信息，请查看 JDK 版本支持的 SSL/TLS 版本。

如果"xpack.security.fips_mode.enabled"为"true"，则不能使用"SSLv2Hello"或"SSLv3"。请参阅 FIPS 140-2。

`xpack.monitoring.exporters.$NAME.ssl.verification_mode`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 控制证书的验证。

有效值

`full`

     Validates that the provided certificate: has an issue date that's within the `not_before` and `not_after` dates; chains to a trusted Certificate Authority (CA); has a `hostname` or IP address that matches the names within the certificate. 
`certificate`

     Validates the provided certificate and verifies that it's signed by a trusted authority (CA), but doesn't check the certificate `hostname`. 
`none`

    

不执行证书验证。

将证书验证设置为"无"会禁用SSL / TLS的许多安全优势，这是非常危险的。仅当 ElasticSupport 指示在尝试解决 TLS 错误时作为临时诊断机制时，才设置此值。

默认为"full"。

`xpack.monitoring.exporters.$NAME.ssl.cipher_suites`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 支持的密码套件因您使用的 Java 版本而异。例如，对于版本 12，默认值为"TLS_AES_256_GCM_SHA384"、"TLS_AES_128_GCM_SHA256"、"TLS_CHACHA20_POLY1305_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"、"TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"、"TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"、"TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"、"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256"、""、""、""、""、""、""、""、""、""、"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384"、"TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256"、"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384"、"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA"、"TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"、"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"、""TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"、"TLS_RSA_WITH_AES_256_GCM_SHA384"、"TLS_RSA_WITH_AES_128_GCM_SHA256"、"TLS_RSA_WITH_AES_256_CBC_SHA256"、"TLS_RSA_WITH_AES_128_CBC_SHA256"、"TLS_RSA_WITH_AES_256_CBC_SHA"、"TLS_RSA_WITH_AES_128_CBC_SHA"。

有关更多信息，请参阅 Oracle 的 Java 加密体系结构文档。

#### X 包监控 TLS/SSL 密钥和受信任证书设置

以下设置用于指定通过 SSL/TLS 连接进行通信时应使用的私钥、证书和受信任证书。私钥和证书是可选的，如果服务器要求客户端身份验证以进行 PKI 身份验证，则会使用私钥和证书。

#### PEM 编码文件

使用 PEM 编码文件时，请使用以下设置：

`xpack.monitoring.exporters.$NAME.ssl.key`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 包含私钥的 PEM 编码文件的路径。

如果需要 HTTP 客户端身份验证，它将使用此文件。您不能同时使用此设置和"ssl.keystore.path"。

`xpack.monitoring.exporters.$NAME.ssl.key_passphrase`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 用于解密私钥的密码短语。由于密钥可能未加密，因此此值是可选的。

您不能同时使用此设置和"ssl.secure_key_passphrase"。

`xpack.monitoring.exporters.$NAME.ssl.secure_key_passphrase`

     ([Secure](secure-settings.html "Secure settings"))  [7.16.0]  Deprecated in 7.16.0.  The passphrase that is used to decrypt the private key. Since the key might not be encrypted, this value is optional. 
`xpack.monitoring.exporters.$NAME.ssl.certificate`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 指定与密钥关联的 PEM 编码证书(或证书链)的路径。

仅当设置了"ssl.key"时，才能使用此设置。

`xpack.monitoring.exporters.$NAME.ssl.certificate_authorities`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 应信任的 PEM 编码证书文件的路径列表。

此设置和"ssl.truststore.path"不能同时使用。

#### Java 密钥库文件

使用 Java 密钥库文件 (JKS) 时，其中包含应信任的私钥、证书和证书，请使用以下设置：

`xpack.monitoring.exporters.$NAME.ssl.keystore.path`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 包含专用密钥和证书的密钥库文件的路径。

它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。不能同时使用此设置和"ssl.key"。

`xpack.monitoring.exporters.$NAME.ssl.keystore.password`

     ([Static](settings.html#static-cluster-setting))  [7.16.0]  Deprecated in 7.16.0.  The password for the keystore. 
`xpack.monitoring.exporters.$NAME.ssl.keystore.secure_password`

     ([Secure](secure-settings.html "Secure settings"))  [7.16.0]  Deprecated in 7.16.0.  The password for the keystore. 
`xpack.monitoring.exporters.$NAME.ssl.keystore.key_password`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 密钥库中密钥的密码。缺省值为密钥库密码。

您不能同时使用此设置和"ssl.keystore.secure_password"。

`xpack.monitoring.exporters.$NAME.ssl.keystore.secure_key_password`

     ([Secure](secure-settings.html "Secure settings"))  [7.16.0]  Deprecated in 7.16.0.  The password for the key in the keystore. The default is the keystore password. 
`xpack.monitoring.exporters.$NAME.ssl.truststore.path`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 包含要信任的证书的密钥库的路径。它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。

您不能同时使用此设置和"ssl.certificate_authorities"。

`xpack.monitoring.exporters.$NAME.ssl.truststore.password`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 信任库的密码。

您不能同时使用此设置和"ssl.truststore.secure_password"。

`xpack.monitoring.exporters.$NAME.ssl.truststore.secure_password`

     ([Secure](secure-settings.html "Secure settings"))  [7.16.0]  Deprecated in 7.16.0.  Password for the truststore. 

#### PKCS#12文件

Elasticsearch 可以配置为使用 PKCS#12 容器文件(".p12"或".pfx"文件)，其中包含应信任的私钥、证书和证书。

PKCS#12 文件的配置方式与 Java 密钥库文件的配置方式相同：

`xpack.monitoring.exporters.$NAME.ssl.keystore.path`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 包含专用密钥和证书的密钥库文件的路径。

它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。不能同时使用此设置和"ssl.key"。

`xpack.monitoring.exporters.$NAME.ssl.keystore.type`

     ([Static](settings.html#static-cluster-setting))  [7.16.0]  Deprecated in 7.16.0.  The format of the keystore file. It must be either `jks` or `PKCS12`. If the keystore path ends in ".p12", ".pfx", or ".pkcs12", this setting defaults to `PKCS12`. Otherwise, it defaults to `jks`. 
`xpack.monitoring.exporters.$NAME.ssl.keystore.password`

     ([Static](settings.html#static-cluster-setting))  [7.16.0]  Deprecated in 7.16.0.  The password for the keystore. 
`xpack.monitoring.exporters.$NAME.ssl.keystore.secure_password`

     ([Secure](secure-settings.html "Secure settings"))  [7.16.0]  Deprecated in 7.16.0.  The password for the keystore. 
`xpack.monitoring.exporters.$NAME.ssl.keystore.key_password`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 密钥库中密钥的密码。缺省值为密钥库密码。

您不能同时使用此设置和"ssl.keystore.secure_password"。

`xpack.monitoring.exporters.$NAME.ssl.keystore.secure_key_password`

     ([Secure](secure-settings.html "Secure settings"))  [7.16.0]  Deprecated in 7.16.0.  The password for the key in the keystore. The default is the keystore password. 
`xpack.monitoring.exporters.$NAME.ssl.truststore.path`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 包含要信任的证书的密钥库的路径。它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。

您不能同时使用此设置和"ssl.certificate_authorities"。

`xpack.monitoring.exporters.$NAME.ssl.truststore.type`

     ([Static](settings.html#static-cluster-setting))  [7.16.0]  Deprecated in 7.16.0.  Set this to `PKCS12` to indicate that the truststore is a PKCS#12 file. 
`xpack.monitoring.exporters.$NAME.ssl.truststore.password`

    

(静态) [7.16.0] 在 7.16.0 中已弃用。 信任库的密码。

您不能同时使用此设置和"ssl.truststore.secure_password"。

`xpack.monitoring.exporters.$NAME.ssl.truststore.secure_password`

     ([Secure](secure-settings.html "Secure settings"))  [7.16.0]  Deprecated in 7.16.0.  Password for the truststore. 

[« Machine learning settings in Elasticsearch](ml-settings.md) [Node
»](modules-node.md)
