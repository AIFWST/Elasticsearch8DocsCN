

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Stopping Elasticsearch](stopping-elasticsearch.md) [Discovery
»](discovery-hosts-providers.md)

## 发现和集群形成

发现和集群形成过程负责发现节点、选择主节点、形成集群以及在每次更改时发布集群状态。

以下过程和设置是发现和群集形成的一部分：

发现

     Discovery is the process where nodes find each other when the master is unknown, such as when a node has just started up or when the previous master has failed. 
[Quorum-based decision making](modules-discovery-quorums.html "Quorum-based
decision making")

     How Elasticsearch uses a quorum-based voting mechanism to make decisions even if some nodes are unavailable. 
[Voting configurations](modules-discovery-voting.html "Voting configurations")

     How Elasticsearch automatically updates voting configurations as nodes leave and join a cluster. 
[Bootstrapping a cluster](modules-discovery-bootstrap-cluster.html
"Bootstrapping a cluster")

     Bootstrapping a cluster is required when an Elasticsearch cluster starts up for the very first time. In [development mode](bootstrap-checks.html#dev-vs-prod-mode "Development vs. production mode"), with no discovery settings configured, this is automatically performed by the nodes themselves. As this auto-bootstrapping is [inherently unsafe](modules-discovery-quorums.html "Quorum-based decision making"), running a node in [production mode](bootstrap-checks.html#dev-vs-prod-mode "Development vs. production mode") requires bootstrapping to be [explicitly configured](modules-discovery-bootstrap-cluster.html "Bootstrapping a cluster"). 
[Adding and removing master-eligible nodes](add-elasticsearch-nodes.html "Add
and remove nodes in your cluster")

     It is recommended to have a small and fixed number of master-eligible nodes in a cluster, and to scale the cluster up and down by adding and removing master-ineligible nodes only. However there are situations in which it may be desirable to add or remove some master-eligible nodes to or from a cluster. This section describes the process for adding or removing master-eligible nodes, including the extra steps that need to be performed when removing more than half of the master-eligible nodes at the same time. 
[Publishing the cluster state](cluster-state-publishing.html "Publishing the
cluster state")

     Cluster state publishing is the process by which the elected master node updates the cluster state on all the other nodes in the cluster. 
[Cluster fault detection](cluster-fault-detection.html "Cluster fault
detection")

     Elasticsearch performs health checks to detect and remove faulty nodes. 
[Settings](modules-discovery-settings.html "Discovery and cluster formation
settings")

     There are settings that enable users to influence the discovery, cluster formation, master election and fault detection processes. 

[« Stopping Elasticsearch](stopping-elasticsearch.md) [Discovery
»](discovery-hosts-providers.md)
