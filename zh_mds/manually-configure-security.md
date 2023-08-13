

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Start the Elastic Stack with security enabled automatically](configuring-
stack-security.md) [Set up minimal security for Elasticsearch »](security-
minimal-setup.md)

## 手动配置安全性

安全需求因您是在笔记本电脑上进行本地开发还是保护生产环境中的所有通信而异。无论您在何处部署弹性堆栈("ELK")，运行安全集群对于保护您的数据都非常重要。这就是为什么在 Elasticsearch 8.0 及更高版本中默认启用和配置安全性的原因。

如果要在现有的不安全群集上启用安全性，请使用自己的证书颁发机构 (CA)，或者希望手动配置安全性，以下方案提供了在传输层上配置 TLS 的步骤，并在需要时保护 HTTPS 流量。

如果您在启动 Elasticsearch 节点之前手动配置安全性，则自动配置过程将遵循您的安全配置。您可以随时调整 TLS 配置，例如更新节点证书。

!弹性安全层

### 最低安全性 (ElasticsearchDevelopment)

如果您一直在使用 Elasticsearch，并希望在现有的不安全集群上启用安全性，请从这里开始。您将为内置用户设置密码以防止未经授权访问本地集群，并为 Kibana 配置密码身份验证。

最低安全方案不足以满足生产模式群集的需求。如果群集具有多个节点，则必须启用最低安全性，然后在节点之间配置传输层安全性 (TLS)。

设置最低安全性

### 基本安全性 (Elasticsearch +Kibana)

此方案为 TLS 配置节点之间的通信。此安全层要求节点验证安全证书，以防止未经授权的节点加入您的 Elasticsearch 集群。

Elasticsearch 和 Kibana 之间的外部 HTTP 流量不会被加密，但节点间通信将得到保护。

设置基本安全性

### 基本安全性加上安全的 HTTPS 流量 (ElasticStack)

此方案基于基本安全性构建，并使用 TLS 保护所有 HTTP流量。除了在 Elasticsearch 集群的传输接口上配置 TLS 之外，您还可以在 HTTP 接口上为 Elasticsearch 和 Kibana 配置 TLS。

如果需要在 HTTP 层上使用双向(双向)TLS，则需要配置相互身份验证的加密。

然后，您将 Kibana 和 Beats 配置为使用 TLS 与 Elasticsearch 通信，以便对所有通信进行加密。此安全级别很强，可确保进出群集的任何通信都是安全的。

设置基本安全性以及 HTTPS 流量

[« Start the Elastic Stack with security enabled automatically](configuring-
stack-security.md) [Set up minimal security for Elasticsearch »](security-
minimal-setup.md)
