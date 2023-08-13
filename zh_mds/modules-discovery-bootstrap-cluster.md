

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Discovery and cluster formation](modules-
discovery.md)

[« Voting configurations](modules-discovery-voting.md) [Publishing the
cluster state »](cluster-state-publishing.md)

## 引导集群

首次启动 Elasticsearch 集群需要在集群中的一个或多个符合主节点条件的节点上显式定义符合主节点条件的初始节点集。这称为_cluster bootstrapping_。这仅在群集首次启动时是必需的。加入正在运行的群集的新启动节点从群集的选定主节点获取此信息。

初始主节点集在"cluster.initial_master_nodes"设置中定义。对于每个符合主节点条件的节点，应将其设置为包含以下项之一的列表：

* 节点的节点名称。  * 如果未设置"node.name"，则为节点的主机名，因为"node.name"默认为节点的主机名。您必须使用完全限定主机名或裸主机名，具体取决于您的系统配置。  * 节点传输发布地址的 IP 地址(如果无法使用节点的"node.name"。这通常是"network.host"解析到的IP地址，但可以覆盖。  * 节点发布地址的 IP 地址和端口，格式为"IP：PORT"，如果无法使用节点的"node.name"并且有多个节点共享一个 IP 地址。

群集形成后，从每个节点的配置中删除"cluster.initial_master_nodes"设置。不应为不符合主节点条件的节点、加入现有群集的符合主节点条件的节点或正在重新启动的节点设置它。

如果在集群形成后保留"cluster.initial_master_nodes"，则存在将来的错误配置可能导致在现有集群旁边引导新集群的风险。可能无法在不丢失数据的情况下从这种情况中恢复。

创建新集群的最简单方法是选择一个符合主节点条件的节点，该节点将引导自身进入单节点集群，然后所有其他节点将加入该集群。在其他符合主节点条件的节点加入群集之前，这种简单的方法对故障没有弹性。例如，如果您有一个节点名称为"master-a"的符合主节点条件的节点，则按如下方式对其进行配置(从所有其他节点的配置中省略"cluster.initial_master_nodes")：

    
    
    cluster.initial_master_nodes: master-a

对于容错群集引导，请使用所有符合主节点条件的节点。例如，如果您的集群有 3 个符合主节点条件的节点，节点名称为"master-a"、"master-b"和"master-c"，则按如下方式配置它们：

    
    
    cluster.initial_master_nodes:
      - master-a
      - master-b
      - master-c

您必须将"cluster.initial_master_nodes"设置为设置它的每个节点上的相同节点列表，以确保在引导过程中仅形成单个集群。如果"cluster.initial_master_nodes"在设置它的节点之间有所不同，则可以引导多个集群。通常不可能在不丢失数据的情况下从这种情况中恢复。

**节点名称格式必须匹配**

"cluster.initial_master_nodes"列表中使用的节点名称必须与节点的"node.name"属性完全匹配。默认情况下，节点名称设置为计算机的主机名，根据您的系统配置，该主机名可能是完全限定的，也可能不是完全限定的。如果每个节点名称都是完全限定域名(例如"master-a.example.com")，那么您也必须在"cluster.initial_master_nodes"列表中使用完全限定域名;相反，如果您的节点名称是裸主机名(不带".example.com"后缀)，则必须在"cluster.initial_master_nodes"列表中使用裸主机名。如果您混合使用完全限定主机名和裸主机名，或者"node.name"和"cluster.initial_master_nodes"之间存在其他不匹配，则集群将无法成功形成，您将看到如下所示的日志消息。

    
    
    [master-a.example.com] master not discovered yet, this node has
    not previously joined a bootstrapped (v7+) cluster, and this
    node must discover master-eligible nodes [master-a, master-b] to
    bootstrap a cluster: have discovered [{master-b.example.com}{...

此消息显示节点名称"master-a.example.com"和"主 b.example.com"以及"cluster.initial_master_nodes"条目"主-a"和"主-b"，从此消息中可以清楚地看出它们不完全匹配。

### 选择群集名称

"cluster.name"设置使您能够创建多个彼此分离的集群。节点在首次相互连接时验证它们是否同意其集群名称，而 Elasticsearch 只会从具有相同集群名称的节点形成集群。集群名称的默认值为"elasticsearch"，但建议更改此值以反映集群的逻辑名称。

### 开发模式下的自动引导

默认情况下，每个节点将在首次启动时自动引导自身进入单节点群集。如果配置了以下任何设置，则不会进行自动引导：

* "discovery.seed_providers" * "discovery.seed_hosts" * "cluster.initial_master_nodes"

要将新节点添加到现有群集中，请配置"discovery.seed_hosts"或其他相关发现设置，以便新节点可以发现群集中现有的符合主节点条件的节点。要引导新的多节点群集，请按照群集引导部分中所述配置"cluster.initial_master_nodes"以及"discovery.seed_hosts"或其他相关发现设置。

**形成单个集群**

一旦 Elasticsearch 节点加入了现有集群，或者引导了一个新的集群，它就不会加入不同的集群。Elasticsearch 不会在单独的集群形成后将它们合并在一起，即使您随后尝试将所有节点配置到单个集群中也是如此。这是因为没有办法将这些单独的集群合并在一起而不会有数据丢失的风险。您可以通过检查每个节点上"GET /"报告的集群 UUID 来判断您已经形成了单独的集群。

如果您打算将节点添加到现有集群中，但改为引导单独的单节点集群，则必须重新启动：

1. 关闭节点。  2. 通过删除节点数据文件夹中的内容来完全擦除节点。  3. 配置"discovery.seed_hosts"或"discovery.seed_providers"以及其他相关发现设置。  4. 重新启动节点并验证它是否加入现有集群，而不是形成自己的单节点集群。

如果您打算形成一个新的多节点集群，但改为引导单节点集群集合，则必须重新开始：

1. 关闭所有节点。  2.通过删除每个节点的数据文件夹的内容来完全擦除每个节点。  3. 如上所述配置"cluster.initial_master_nodes"。  4. 配置"discovery.seed_hosts"或"discovery.seed_providers"以及其他相关发现设置。  5. 重新启动所有节点并验证它们是否已形成单个集群。

[« Voting configurations](modules-discovery-voting.md) [Publishing the
cluster state »](cluster-state-publishing.md)
