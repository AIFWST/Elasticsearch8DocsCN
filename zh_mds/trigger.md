

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Watcher chain input](input-chain.md) [Watcher schedule trigger
»](trigger-schedule.md)

## 观察程序触发器

每个监视都必须有一个"触发器"，用于定义监视执行过程应何时启动。创建监视时，其触发器将注册到相应的_Trigger Engine_。触发引擎负责评估触发器并在需要时触发手表。

观察程序旨在支持不同类型的触发器，但目前只有基于时间的"计划"触发器可用。

[« Watcher chain input](input-chain.md) [Watcher schedule trigger
»](trigger-schedule.md)
