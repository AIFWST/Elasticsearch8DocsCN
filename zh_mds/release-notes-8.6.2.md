

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.7.0](release-notes-8.7.0.md) [Elasticsearch
version 8.6.1 »](release-notes-8.6.1.md)

## 弹性搜索版本8.6.2

另请参阅 8.6 中的重大更改。

### 已知问题

* 分片重新平衡可能会暂时使集群失去平衡

从 8.6.0 开始，默认的分片重新平衡算法将计算最终的期望余额，然后进行分片移动以协调集群的当前状态与期望状态。但是，分片移动发生的顺序可能会偏向某些节点，从而导致集群在协调过程中暂时变得不平衡。与往常一样，一旦节点达到磁盘水印，它将不接受任何其他分片，但这种倾斜可能会导致节点在正常操作中比预期更频繁地到达其磁盘水印。对帐过程完成后，群集将再次平衡。

要避免此问题，请升级到 8.8.0 或更高版本。

* 使用采集附件处理器时，Tika 与 log4j 2.18.0 及更高版本(在 Elasticsearch 8.4.0 中引入)的交互会导致日志记录过多。此日志记录过多，可能导致群集不稳定，直至群集不可用且必须重新启动节点。(问题：#91964)。此问题已在 Elasticsearch 8.7.0 (#93878) 中修复

要解决此问题，请升级到 8.7.0 或更高版本。

### 错误修正

Allocation

    

* 仅模拟合法的所需动作 #93635(问题：#93271)

Health

    

* 修复了运行状况 API 中初始化分片的报告 #93502(问题：#90327)

Infra/Core

    

* 不要报告 7.x 指数的MIGRATION_NEEDED #93666

采集节点

    

* 修复处理 IP 阵列时地理 ip 数据库文件泄漏的问题 #93177

机器学习

    

* 在摄取时使用长推理超时 #93731

[« Elasticsearch version 8.7.0](release-notes-8.7.0.md) [Elasticsearch
version 8.6.1 »](release-notes-8.6.1.md)
