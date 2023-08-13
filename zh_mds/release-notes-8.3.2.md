

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.3.3](release-notes-8.3.3.md) [Elasticsearch
version 8.3.1 »](release-notes-8.3.1.md)

## 弹性搜索版本8.3.2

另请参阅 8.3 中的重大更改。

Elasticsearch 8.3.2 是 Elastic Stack 的版本兼容版本。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Geo

    

* 修复"内部地质网格"#88273 上的潜在断路器泄漏(问题：#88261)

### 新功能

Heath

    

* 为"instance_has_master"指示器 #87963 添加用户操作

[« Elasticsearch version 8.3.3](release-notes-8.3.3.md) [Elasticsearch
version 8.3.1 »](release-notes-8.3.1.md)
