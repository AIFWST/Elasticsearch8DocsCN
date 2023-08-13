

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Encrypting sensitive data in Watcher](encrypting-data.md) [Watcher simple
input »](input-simple.md)

## 观察器输入

触发监视时，其 _input_ 将数据加载到执行上下文中。此有效负载可在后续监视执行阶段访问。例如，您可以根据其输入加载的数据来计算手表的状况。

观察程序支持四种输入类型：

* "简单"：将静态数据加载到执行上下文中。  * "搜索"：将搜索结果加载到执行上下文中。  * 'http'：将 HTTP 请求的结果加载到执行上下文中。  * "链"：使用一系列输入将数据加载到执行上下文中。

如果未为监视定义输入，则会将空有效负载加载到执行上下文中。

[« Encrypting sensitive data in Watcher](encrypting-data.md) [Watcher simple
input »](input-simple.md)
