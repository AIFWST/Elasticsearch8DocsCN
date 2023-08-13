

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Full-cluster restart and rolling restart](restart-cluster.md) [Configure
remote clusters with security »](remote-clusters-security.md)

## 远程集群

您可以将本地集群连接到其他 Elasticsearch 集群(已知as_remote clusters_)。远程群集可以位于不同的数据中心或地理区域，并且包含可通过跨群集复制进行复制或由本地群集使用跨群集搜索进行搜索的索引或数据流。

通过跨集群复制，您可以将数据引入到远程集群上的索引。此 _leader_ 索引将复制到本地集群上的一个或多个只读 _follower_ 索引。通过创建具有跨群集复制的多群集体系结构，您可以配置灾难恢复、使数据更接近用户或建立集中式报表群集以在本地处理报表。

跨集群搜索使您能够针对一个或多个远程集群运行搜索请求。此功能为每个区域提供所有集群的全局视图，允许您从本地集群发送搜索请求，并从所有连接的远程集群返回结果。对于完整的跨群集搜索功能，本地群集和远程群集必须位于同一订阅级别。

在本地和远程群集上启用和配置安全性都很重要。将本地集群连接到远程集群时，本地集群上的 Elasticsearchsuper用户(例如"弹性"用户)可以获得对远程集群的完全读取访问权限。要安全地使用跨集群复制和跨集群搜索，请在所有连接的集群上启用安全性，并至少在每个节点的传输级别上配置传输层安全性 (TLS)。

此外，操作系统级别的本地管理员对 Elasticsearch 配置文件和私钥具有足够的访问权限，可能会接管远程集群。确保您的安全策略包括在操作系统级别保护本地 _and_ 远程群集。

要注册远程群集，请使用嗅探模式(默认)或代理模式将本地群集连接到远程群集中的节点。注册远程集群后，配置跨集群复制和跨集群搜索的权限。

### 嗅探模式

在嗅探模式下，使用名称和种子节点列表创建集群。注册远程群集时，将从其中一个种子节点检索其群集状态，并且最多选择三个_gateway nodes_作为远程群集请求的一部分。此模式要求本地群集可以访问网关节点的发布地址。

嗅探模式是默认的连接模式。

_gateway nodes_选择取决于以下条件：

* **版本**：远程节点必须与它们注册到的群集兼容：

    * Any node can communicate with another node on the same major version. For example, 7.0 can talk to any 7.x node. 
    * Only nodes on the last minor version of a certain major version can communicate with nodes on the following major version. In the 6.x series, 6.8 can communicate with any 7.x node, while 6.7 can only communicate with 7.0. 
    * Version compatibility is symmetric, meaning that if 6.7 can communicate with 7.0, 7.0 can also communicate with 6.7. The following table depicts version compatibility between local and remote nodes.

版本兼容性表

|

本地群集 ---|--- 远程群集

|

5.0–5.5

|

5.6

|

6.0–6.6

|

6.7

|

6.8

|

7.0

|

7.1–7.16

|

7.17

|

8.0–8.9    5.0–5.5

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 5.6

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.0–6.6

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.7

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.8

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.0

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.1–7.16

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.17

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.0–8.9

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是的   

Elastic 仅支持对这些配置的子集进行跨集群搜索。请参阅支持的跨集群搜索配置。

* **角色**：默认情况下，任何不符合主节点条件的节点都可以充当网关节点。专用主节点永远不会被选为网关节点。  * **属性**：您可以通过将"cluster.remote.node.attr.gateway"设置为"true"来定义集群的网关节点。但是，此类节点仍然必须满足上述两个要求。

### 代理模式

在代理模式下，使用名称和单个代理地址创建群集。注册远程群集时，将打开到代理地址的可配置数量的套接字连接。需要代理才能将这些连接路由到远程群集。代理模式不要求远程群集节点具有可访问的发布地址。

代理模式不是默认连接模式，必须进行配置。代理模式与嗅探模式具有相同的版本兼容性要求。

版本兼容性矩阵

|

本地群集 ---|--- 远程群集

|

5.0–5.5

|

5.6

|

6.0–6.6

|

6.7

|

6.8

|

7.0

|

7.1–7.16

|

7.17

|

8.0–8.9    5.0–5.5

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 5.6

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.0–6.6

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.7

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.8

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.0

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.1–7.16

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.17

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.0–8.9

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是的，Elastic 仅支持对这些配置的子集进行跨集群搜索。请参阅支持的跨集群搜索配置。

[« Full-cluster restart and rolling restart](restart-cluster.md) [Configure
remote clusters with security »](remote-clusters-security.md)
