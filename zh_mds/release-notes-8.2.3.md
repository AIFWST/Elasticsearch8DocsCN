

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.3.0](release-notes-8.3.0.md) [Elasticsearch
version 8.2.2 »](release-notes-8.2.2.md)

## 弹性搜索版本8.2.3

另请参阅 8.2 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Authorization

    

* 修复通配符应用程序权限的解析 #87293

CCR

    

* 删除 CcrRepository #87235 中的一些阻塞

索引接口

    

* 将解析索引 API 添加到索引 #87052 的"读取"权限(问题：#86977)

Infra/Core

    

* 清理异常 #87163 后的"放气压缩机"(问题：#87160)

Security

    

* 安全插件关闭可发布领域 #87429(问题：#86286)

Snapshot/Restore

    

* 从"存储恢复"#87254 调用"getRepositoryData"后分叉(问题：#87237)

###Enhancements

Infra/Core

    

* 强制扩展安全策略的属性 #87396

[« Elasticsearch version 8.3.0](release-notes-8.3.0.md) [Elasticsearch
version 8.2.2 »](release-notes-8.2.2.md)
