

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Secure the Elastic Stack](secure-cluster.md) [Start the Elastic Stack
with security enabled automatically »](configuring-stack-security.md)

## 弹性搜索安全原则

保护您的 Elasticsearch 集群及其包含的数据至关重要。实施纵深防御策略可提供多层安全性，以帮助保护您的系统。以下原则为以安全的方式运行 Elasticsearch 奠定了基础，有助于在多个级别缓解对系统的攻击。

### 在启用安全性的情况下运行 Elasticsearch

切勿在未启用安全性的情况下运行 Elasticsearch 集群。这一原则怎么强调都不为过。在没有安全性的情况下运行 Elasticsearch 会使您的集群暴露给任何可以向 Elasticsearch 发送网络流量的人，从而允许这些人下载、修改或删除您的集群中的任何数据。在启用安全性的情况下启动 Elastic Stack，或手动配置安全性以防止未经授权访问您的集群并确保节点间通信安全。

### 使用专用的非 root 用户运行 Elasticsearch

切勿尝试以"根"用户身份运行 Elasticsearch，这将使任何防御策略无效，并允许恶意用户在您的服务器上执行任何操作。您必须创建一个专用的非特权用户才能运行 Elasticsearch.By 默认值，Elasticsearch 的 'rpm'、'deb'、'docker 和 Windows 软件包包含具有此范围的 'elasticsearch' 用户。

### 保护 Elasticsearch 免受公共互联网流量的影响

即使启用了安全性，也不要将 Elasticsearch 暴露给公共互联网流量。使用应用程序清理对 Elasticsearch 的请求仍然存在风险，例如恶意用户编写"_search"请求，这可能会使 Elasticsearch 集群不堪重负并使其瘫痪。保持Elasticsearch尽可能隔离，最好是在防火墙和VPN后面。任何面向 Internet 的应用程序都应运行预封装聚合，或者根本不运行聚合。

虽然你绝对不应该直接向互联网公开Elasticsearch，但你也不应该直接向用户公开Elasticsearch。相反，请使用中介应用程序代表用户发出请求。此实现允许您跟踪用户行为，例如可以提交请求，以及集群中的哪些特定节点。例如，您可以实现一个应用程序，该应用程序接受来自用户的搜索词并通过"simple_query_string"查询将其汇集。

### 实现基于角色的访问控制

为用户定义角色并分配适当的权限，以确保用户只能访问所需的资源。此过程确定是否允许传入请求背后的用户运行该请求。

[« Secure the Elastic Stack](secure-cluster.md) [Start the Elastic Stack
with security enabled automatically »](configuring-stack-security.md)
