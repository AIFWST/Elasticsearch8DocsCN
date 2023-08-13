

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.2.3](release-notes-8.2.3.md) [Elasticsearch
version 8.2.1 »](release-notes-8.2.1.md)

## 弹性搜索版本8.2.2

另请参阅 8.2 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Audit

    

* 修复了审核日志记录以一致地在"origin.address"中包含端口号 #86732

CCR

    

* 修复了从属者上具有封闭索引的数据流之后的 CCR 损坏数据流 #87076(问题：#87048)

Geo

    

* 用于向矢量图块添加空值标签的防护 #87051

Infra/Core

    

* 调整突发 CPU 的 osprobe 断言 #86990

机器学习

    

* 修复群集生命周期早期的 ML 任务审核员异常 #87023(问题：#87002) * 分类中的邻接权重修复 #2277

###Enhancements

机器学习

    

* 使 ML 原生进程与 glibc 2.35 配合使用(Ubuntu 22.04 需要)#2272

[« Elasticsearch version 8.2.3](release-notes-8.2.3.md) [Elasticsearch
version 8.2.1 »](release-notes-8.2.1.md)
