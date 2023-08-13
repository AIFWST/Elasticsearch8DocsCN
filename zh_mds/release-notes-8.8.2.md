

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.9.0](release-notes-8.9.0.md) [Elasticsearch
version 8.8.1 »](release-notes-8.8.1.md)

## 弹性搜索版本8.8.2

另请参阅 8.8 中的重大更改。

### 错误修正

Aggregations

    

* 修复了空百分位数引发空指针异常的迭代 #96668(问题：#96626)

Health

    

* 在"运行状况元数据服务"中使用"群集设置"而不是节点"设置" #96843(问题：#96219)

采集节点

    

* 支持重新路由处理器中的虚线字段表示法 #96243

机器学习

    

* 确保 NLP 模型推理队列在关机或失败后始终被清除 #96738

SQL

    

* 修复了涉及版本值 #96540 的查询的翻译(问题：#96509)

Search

    

* 增加打开时间点的并发请求 #96782

TSDB

    

* 获取数据流 API 错误地打印已升级的 tsdb 数据流的警告日志 #96606

###Enhancements

TSDB

    

* 更改汇总线程池设置 #96821(问题：#96758)

Transform

    

* 添加空检查以修复潜在的 NPE #96785(问题：#96781)

[« Elasticsearch version 8.9.0](release-notes-8.9.0.md) [Elasticsearch
version 8.8.1 »](release-notes-8.8.1.md)
