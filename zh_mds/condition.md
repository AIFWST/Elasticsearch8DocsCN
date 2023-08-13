

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Watcher schedule trigger](trigger-schedule.md) [Watcher always condition
»](condition-always.md)

## 观察程序条件

触发监视时，其条件确定是否执行监视操作。观察程序支持以下条件类型：

* "always"：条件的计算结果始终为"true"，因此始终执行监视操作。  * "从不"：条件的计算结果始终为"false"，因此永远不会执行监视操作。  * "比较"：与监视有效负载中的值执行简单比较，以确定是否执行监视操作。  * "array_compare"：将监视有效负载中的值数组与给定值进行比较，以确定是否执行监视操作。  * "脚本"：使用脚本确定是否执行监视操作。

如果从监视中省略条件定义，则条件默认为"始终"。

评估条件时，它具有对监视执行上下文的完全访问权限，包括监视有效负载 ('ctx.payload.*')。脚本，比较andarray_compare条件可以使用有效载荷数据来确定是否满足必要条件。

除了监视范围条件之外，您还可以配置每个条件。

[« Watcher schedule trigger](trigger-schedule.md) [Watcher always condition
»](condition-always.md)
