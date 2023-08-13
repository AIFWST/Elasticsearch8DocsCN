

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.4.0](release-notes-8.4.0.md) [Elasticsearch
version 8.3.2 »](release-notes-8.3.2.md)

## 弹性搜索版本8.3.3

另请参阅 8.3 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Infra/Core

    

* 将"build_flavor"添加回信息 API REST 响应 #88336(问题：#88318)

Mapping

    

* 仅在运行脚本时强制实施最大值限制 #88295

Monitoring

    

* 将 cgroup 内存字段切换到关键字 #88260

Packaging

    

* 修复 Docker 位置参数传递 #88584

Security

    

* 确保"CreateApiKey"始终创建一个新文档 #88413

###Enhancements

Security

    

* 关闭 OIDC 反向通道中的空闲连接的新设置 #87773

###Upgrades

Packaging

    

* 升级到 OpenJDK 18.0.2+9 #88675(问题：#88673)

[« Elasticsearch version 8.4.0](release-notes-8.4.0.md) [Elasticsearch
version 8.3.2 »](release-notes-8.3.2.md)
