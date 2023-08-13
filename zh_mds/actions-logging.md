

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Watcher index action](actions-index.md) [Watcher Slack Action »](actions-
slack.md)

## 观察程序日志记录操作

使用"日志记录"操作将文本记录到标准 Elasticsearch 日志中。有关支持的属性，请参阅日志记录操作属性。

此操作主要用于开发期间和调试目的。

### 配置日志记录操作

您可以在"操作"数组中配置日志记录操作。特定于操作的属性是使用"日志记录"关键字指定的。

以下代码片段显示了一个简单的日志记录操作定义：

    
    
    "actions" : {
      "log" : { __"transform" : { ... }, __"logging" : {
          "text" : "executed at {{ctx.execution_time}}" __}
      }
    }

__

|

操作的 ID。   ---|---    __

|

一个可选的转换，用于在执行"日志记录"操作之前转换有效负载。   __

|

要记录的文本。   ### 日志记录操作属性编辑

姓名 |必填 |默认 |描述 ---|---|---|--- 'text'

|

yes

|

-

|

应记录的文本。可以是静态文本或包含胡子模板。   "类别"

|

no

|

xpack.watcher.actions.logging

|

将记录文本的类别。   "水平"

|

no

|

info

|

日志记录级别。有效值为："错误"、"警告"、"信息"、"调试"和"跟踪"。   « 观察者索引操作 观察者松弛动作 »