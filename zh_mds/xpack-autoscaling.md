

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Data tiers](data-tiers.md) [Autoscaling deciders »](autoscaling-
deciders.md)

#Autoscaling

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

自动缩放功能使操作员能够配置节点层，这些节点层可自行监视是否需要根据操作员定义的策略进行缩放。然后，通过自动扩展 API，Elasticsearch 集群可以报告它是否需要额外的资源来满足策略。例如，操作员可以定义一个策略，即暖层应根据可用磁盘空间进行缩放。Elasticsearch 将监控和预测暖层中的可用磁盘空间，如果预测使得集群很快由于磁盘空间而无法分配现有和未来的分片副本，则自动缩放 API 将报告集群由于磁盘空间而需要扩展。操作员仍有责任添加集群发出信号所需的额外资源。

策略由角色列表和决策程序列表组成。与角色匹配的节点由策略管理。决策程序提供所需容量的独立估计。有关决策程序的详细信息，请参阅自动缩放决策程序可用。

自动缩放支持专用机器学习节点的纵向扩展和缩减。自动缩放还支持基于存储纵向扩展数据节点。

自动缩放在 Debian 8 上不受支持。

[« Data tiers](data-tiers.md) [Autoscaling deciders »](autoscaling-
deciders.md)
