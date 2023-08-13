

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Remote clusters](remote-clusters.md)

[« Remote clusters](remote-clusters.md) [Connect to remote clusters
»](remote-clusters-connect.md)

## 配置具有安全性的远程群集

要安全地对远程群集使用跨群集复制或跨群集搜索，请在所有连接的群集上启用安全性，并在每个节点上配置传输层安全性 (TLS)。远程群集至少需要在传输接口上配置 TLS 安全性。为了提高安全性，请在 HTTP 接口上配置 TLS。

所有连接的群集必须相互信任，并在传输接口上使用 TLS 相互进行身份验证。这意味着本地群集信任远程群集的证书颁发机构 (CA)，远程群集信任本地群集的 CA。建立连接时，所有节点都将验证来自另一端节点的证书。这种相互信任是安全连接远程集群所必需的，因为所有连接的节点实际上形成了一个安全域。

在本地群集上执行用户身份验证，并将用户和用户的角色名称传递到远程群集。远程群集根据其本地角色定义检查用户的角色名称，以确定允许用户访问哪些索引。

在对 securedElasticsearch 集群使用跨集群复制或跨集群搜索之前，请完成以下配置任务：

1. 在每个连接的集群中的每个节点上启用 Elasticsearch 安全功能，方法是在 'elasticsearch.yml' 中将 'xpack.security.enabled' 设置为 'true'。请参考 Elasticsearch 安全设置。  2. 在每个节点上配置传输层安全性 (TLS)，以加密节点间流量，并使用所有远程群集中的节点对本地群集中的节点进行身份验证。有关配置安全性所需的步骤，请参阅为 Elastic Stack 设置基本安全性。

此过程使用相同的 CA 为所有节点生成证书。或者，您可以将本地群集中的证书添加为每个远程群集中的受信任 CA。您还必须将来自远程群集的证书添加为本地群集上的受信任 CA。使用相同的 CA 为所有节点生成证书可简化此任务。

启用并配置安全性后，您可以从本地群集连接远程群集。

连接群集后，需要在本地和远程群集上配置用户和权限。

如果要为跨集群复制配置远程集群，则需要在本地集群上配置关注者索引，以在远程集群上复制领导索引。

[« Remote clusters](remote-clusters.md) [Connect to remote clusters
»](remote-clusters-connect.md)
