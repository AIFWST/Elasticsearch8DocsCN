

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md) ›[Collecting monitoring data
using legacy collectors](collecting-monitoring-data.md)

[« Local exporters](local-exporter.md) [Pausing data collection »](pause-
export.md)

## HTTP导出器

Elastic 代理和 Metricbeat 是收集监控数据并将其传送到监控集群的推荐方法。

如果您之前配置了旧版收集方法，则应迁移到使用 Elastic Agent 或 Metricbeat 收集。不要将旧收集与其他收集方法一起使用。

"http"导出器是 Elasticsearch 监控功能中的首选导出器，因为它允许使用单独的监控集群。作为次要好处，它避免使用生产群集节点作为索引监视数据的协调节点，因为所有请求都是对监视群集的 HTTP 请求。

"http"导出器使用低级Elasticsearch REST客户端，这使得它能够将其数据发送到它可以通过网络访问的任何Elasticsearch集群。它的请求利用"filter_path"参数尽可能减少带宽，这有助于确保生产和监控集群之间的通信尽可能轻量级。

"http"导出器支持许多设置，这些设置控制它如何通过 HTTP 与远程群集进行通信。在大多数情况下，没有必要显式配置这些设置。有关详细说明，请参阅监视设置。

    
    
    xpack.monitoring.exporters:
      my_local: __type: local
      my_remote: __type: http
        host: [ "10.1.2.3:9200", ... ] __auth: __username: my_username
          # "xpack.monitoring.exporters.my_remote.auth.secure_password" must be set in the keystore
        connection:
          timeout: 6s
          read_timeout: 60s
        ssl: ... __proxy:
          base_path: /some/base/path __headers: __My-Proxy-Header: abc123
          My-Other-Thing: [ def456, ... ]
        index.name.time_format: YYYY-MM __

__

|

显式定义的"本地"导出器，其任意名称为"my_local"。   ---|---    __

|

定义的"http"导出器，其任意名称为"my_remote"。此名称唯一定义导出器，但未使用。   __

|

"host"是"http"导出器的必需设置。它必须指定 HTTPport 而不是传输端口。默认端口值为"9200"。   __

|

用户身份验证，适用于使用 Elastic Stack 安全功能或其他形式的用户身份验证来保护集群的用户身份验证。   __

|

有关所有 TLS/SSL 设置，请参阅 HTTP 导出器设置。如果未提供，则使用默认节点级 TLS/SSL 设置。   __

|

可选基本路径，用于在任何传出请求前面加上前缀，以便使用代理。   __

|

任意键/值对，定义为要随每个请求一起发送的标头。基于数组的键/值格式为每个值发送一个标头。   __

|

用于更改默认使用的日期后缀的机制。   "http"导出器接受"主机"数组，它将轮询列表。当监控群集包含多个节点时，最好利用该功能。

与"本地"导出器不同，使用"http"导出器的_every_节点尝试检查和创建所需的资源。"http"导出避免重新检查资源，除非某些东西触发它再次执行检查。这些触发因素包括：

* 生产群集的节点将重新启动。  * 与监控集群的连接失败。  * 生产群集上的许可证已更改。  * "http"导出器是动态更新的(因此会被替换)。

触发检查的最简单方法是禁用，然后重新启用导出器。

此资源管理行为可能会为删除监视资源的用户创建一个漏洞。由于"http"导出器不会重新检查其资源，除非发生其中一个触发器，这可能会导致格式错误的索引映射。

与"本地"导出器不同，"http"导出器本质上是集群外部的路由请求。这种情况意味着，当监控集群需要用户名和密码时，导出程序必须提供用户名和密码(或其他适当的安全配置，例如 TLS/SSL 设置)。

在讨论与"http"导出器相关的安全性时，请务必记住所有用户都在监控集群上进行管理。当您从开发环境迁移到生产环境时，记住这一点尤其重要，因为生产环境通常具有专用的监视群集。

有关"http"导出器的配置选项的详细信息，请参阅 HTTP 导出器设置。

[« Local exporters](local-exporter.md) [Pausing data collection »](pause-
export.md)
