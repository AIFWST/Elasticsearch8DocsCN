

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Data management](data-management.md) [Tutorial: Customize built-in ILM
policies »](example-using-index-lifecycle-policy.md)

## ILM：管理索引生命周期

您可以将索引生命周期管理 (ILM) 策略配置为根据您的性能、弹性和保留要求自动管理索引。例如，您可以使用 ILM 执行以下操作：

* 当索引达到一定大小或文档数量时启动新索引 * 每天、每周或每月创建一个新索引，并存档以前的索引 * 删除过时的索引以强制实施数据保留标准

您可以通过 Kibana Management 或 ILM API 创建和管理索引生命周期策略。当您使用 Elastic Agent、Beats 或 Logstash Elasticsearchoutput 插件将数据发送到 Elastic Stack 时，会自动创建默认的索引生命周期管理策略。

！索引生命周期策略

要自动备份索引和管理快照，请使用快照生命周期策略。

* _Tutorial：自定义内置policies_ * _Tutorial：自动化rollover_ * _概述_ * _概念_ * _Configure生命周期policy_ * _Migrate索引分配筛选器到节点roles_ * _Troubleshooting索引生命周期管理errors_ * _Start和停止索引生命周期management_ * _Manage现有indices_ * _Skip rollover_ * _Restore托管数据流或index_ * _Index生命周期管理APIs_ * _Index生命周期actions_

[« Data management](data-management.md) [Tutorial: Customize built-in ILM
policies »](example-using-index-lifecycle-policy.md)
