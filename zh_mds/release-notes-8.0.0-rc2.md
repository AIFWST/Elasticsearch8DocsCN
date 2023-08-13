

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.0.0](release-notes-8.0.0.md) [Elasticsearch
version 8.0.0-rc1 »](release-notes-8.0.0-rc1.md)

## 弹性搜索版本8.0.0-rc2

另请参阅 8.0 中的重大更改。

### 已知问题

* **不要将生产集群升级到 Elasticsearch 8.0.0-rc2.** Elasticsearch 8.0.0-rc2 是 Elasticsearch 8.0 的预发行版，仅用于测试目的。

不支持从预发布版本升级，这可能会导致错误或数据丢失。如果从已发布版本(如 7.16)升级到预发布版本进行测试，请在完成后放弃群集的内容。请勿尝试升级到最终的 8.0 版本。

* 如果您在 aarch64 平台(如 Linux ARM 或 macOS M1)上的存档中安装了 Elasticsearch，则在首次启动节点时不会自动生成"弹性"用户密码和 Kibana 注册令牌。

节点启动后，使用"bin/elasticsearch-reset-password"工具生成"弹性"密码：

    
        bin/elasticsearch-reset-password -u elastic

然后，使用 'bin/elasticsearch-create-enrollment-token' 工具为 Kibana 创建一个注册令牌：

    
        bin/elasticsearch-create-enrollment-token -s kibana

###Deprecations

Engine

* 弃用设置"max_merge_at_once_explicit"#80574

Search

* 根据节点特征配置 'IndexSearcher.maxClauseCount()' #81525 (问题： #46433)

### 新功能

Snapshot/Restore

    

* 支持 Kubernetes 服务账户的 IAM 角色 #81255(问题：#52625)

Watcher

    

* 对观察程序历史记录模板名称使用"startsWith"而不是完全匹配 #82396

###Enhancements

集群协调

    

* 减少"任务批处理器"的锁重 #82227(问题：#77466)

ILM+SLM

    

* 避免不必要的"生命周期执行状态"重新计算 #81558(问题：#77466、#79692) * 将未更改的 ILM 策略更新转换为无操作 #82240(问题：#82065)

Infra/Core

    

* 阻止升级到 8.0，而无需先升级到最后一个 7.x 版本 #82321(问题：#81865)

机器学习

    

* 将"deployment_stats"添加到训练模型统计信息 #80531 * 设置"use_auto_machine_memory_percent"现在默认为"max_model_memory_limit" #80532(问题：#80415)

Network

    

* 改进慢速入站处理以包括响应类型 #80425

Packaging

    

* 将存储库插件转换为模块 #81870(问题：#81652)

Search

    

* 在 kNN 搜索 #80516 中检查前面的嵌套字段(问题：#78473)

### 错误修正

Autoscaling

    

* 使用调整后的总内存而不是总内存 #80528(问题：#78750)

Infra/Scripting

    

* 修复脚本引擎创建时重复的允许列表 #82820(问题：#82778)

Ingest

    

* 将默认 geoip 日志记录调整为不那么详细 #81404(问题：#81356)

机器学习

    

* 在开始部署之前检查"total_definition_length"是否一致 #80553 * 在某些错误类型上更一致地使推理处理器失败 #81475 * 优化作业统计信息调用以减少搜索 #82362(问题：#82255)

Recovery

    

* 使分片启动的响应处理仅在群集状态更新完成后返回 #82790(问题：#81628)

Search

    

* 使用余弦相似性时拒绝零长度向量 #82241(问题：#81167)

Security

    

* 固定配置路径下自动生成的 TLS 文件 #81547 (问题： #81057) * 在某些情况下绑定到非本地主机进行传输 #82973 * 节点重新配置时更正文件所有权 #82789(问题：#80990) * 使用花哨的 unicode 显示安全自动配置 #82740(问题：#82364)

Snapshot/Restore

    

* 如果没有要还原的内容，请删除自定义元数据 #81373(问题：#81247、#82019)

###Upgrades

Infra/Logging

    

* 升级 ECS 日志记录布局至最新版本 #80500

Search

    

* 升级到已发布的 lucene 9.0.0 #81426

[« Elasticsearch version 8.0.0](release-notes-8.0.0.md) [Elasticsearch
version 8.0.0-rc1 »](release-notes-8.0.0-rc1.md)
