

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Searchable snapshots](searchable-snapshots.md) [Elasticsearch security
principles »](es-security-principles.md)

# 保护弹性堆栈

弹性堆栈由许多活动部件组成。有构成集群的 Elasticsearch 节点，以及 Logstash 实例、Kibanainstances、Beats 代理和客户端都与集群通信。为了确保集群安全，请遵循 Elasticsearch 安全原则。

第一个原则是在启用安全性的情况下运行 Elasticsearch。配置安全性可能很复杂，因此我们可以轻松启动启用了并配置安全性的 Elastic Stack。对于任何新集群，只需启动 Elasticsearch 即可自动启用密码保护、使用传输层安全性 (TLS) 进行安全节点间通信，以及加密 Elasticsearch 和 Kibana 之间的连接。

如果您有一个现有的不安全集群(或者希望自己管理安全性)，您可以手动启用和配置安全性以保护 Elasticsearchcluster 和与您的集群通信的任何客户端。您还可以实施其他安全措施，例如基于角色的访问控制、IP 筛选和审核。

启用安全性通过以下方式保护 Elasticsearch 集群：

* 通过密码保护、基于角色的访问控制和 IP 过滤防止未经授权的访问。  * 通过 SSL/TLS 加密保持数据的完整性。  * 维护审计跟踪，以便您知道谁在对您的集群及其存储的数据执行什么操作。

如果您计划在启用了联邦信息处理标准 (FIPS) 140-2 的 JVM 中运行 Elasticsearch，请参阅 FIPS 140-2。

## 防止未经授权的访问

为了防止对 Elasticsearch 集群的未授权访问，您需要一种方法来_验证_用户，以验证用户是否是他们声称的身份。例如，确保只有名为_Kelsey Andorra_的人才能以用户"kandorra"身份登录。Elasticsearch 安全功能提供独立的身份验证机制，使您能够快速使用密码保护集群。

如果您已经在使用 LDAP、Active Directory 或 PKI 来管理组织中的用户，则安全功能将与这些系统集成以执行用户身份验证。

在许多情况下，对用户进行身份验证是不够的。您还需要一种方法来控制用户可以访问哪些数据以及他们可以执行哪些任务。通过启用 Elasticsearch 安全功能，您可以通过为角色分配访问权限并将这些角色分配给用户来_授权_用户。使用此基于角色的访问控制机制 (RBAC)，您可以将用户"kandorra"限制为仅对"事件"索引执行读取操作，从而限制对所有其他索引的访问。

安全功能还使您能够根据 IP 筛选器限制可以连接到群集的节点和客户端。您可以阻止和允许特定 IP 地址、子网或 DNS 域来控制对集群的网络级访问。

请参阅用户身份验证和用户授权。

## 保持数据完整性和机密性

安全性的一个关键部分是确保机密数据的安全。Elasticsearch 具有针对意外数据丢失和损坏的内置保护功能。但是，没有什么可以阻止故意篡改或数据拦截。Elastic Stack 安全功能使用 TLS 来保护the_integrity_数据不被篡改，同时还通过加密与集群之间的通信以及集群内的通信来providing_confidentiality_。为了获得更好的保护，您可以提高加密强度。

请参见配置弹性堆栈的安全性。

## 维护审计跟踪

保持系统安全需要保持警惕。通过使用 Elastic Stack 安全功能来维护审计跟踪，您可以轻松查看谁在访问您的集群以及他们在做什么。您可以配置审核级别，该级别考虑记录的事件类型。这些事件包括身份验证尝试失败、用户访问被拒绝、节点连接被拒绝等。通过分析访问模式和访问集群的失败尝试，您可以深入了解尝试的攻击和数据泄露。保留群集中活动的可审核日志也有助于诊断操作问题。

请参阅启用审核日志记录。

[« Searchable snapshots](searchable-snapshots.md) [Elasticsearch security
principles »](es-security-principles.md)
