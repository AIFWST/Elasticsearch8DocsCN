

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Payload transforms](transform.md)

[« Watcher search payload transform](transform-search.md) [Watcher chain
payload transform »](transform-chain.md)

## 观察程序脚本有效负载转换

一种有效负载转换，用于在监视执行上下文中的当前有效负载上执行脚本，并将其替换为新生成的有效负载。以下代码片段显示了如何在监视级别定义简单的脚本负载转换：

"脚本"有效负载转换与"搜索"有效负载转换结合使用时通常很有用，其中脚本只能从搜索结果中提取重要数据，从而保持有效负载最小。这可以通过"链"有效载荷转换来实现。

    
    
    {
      "transform" : {
        "script" : "return [ 'time' : ctx.trigger.scheduled_time ]" __}
    }

__

|

一个简单的"无痛"脚本，可创建一个新的有效负载，其中包含一个保存计划时间的"time"字段。   ---|--- 执行的脚本可以返回一个等效于 Java™ Map 或 JSON 对象的有效模型(您需要查阅特定脚本语言的文档以了解此构造是什么)。返回的任何其他值都将被赋值，并通过"_value"变量访问。

'script' 属性可以保存一个字符串值，在这种情况下，它将被视为内联脚本，并且将假定默认的 elasticsearch 脚本语言(如脚本中所述)。您可以使用 Elasticsearch 支持的其他脚本语言。为此，您需要将"脚本"字段设置为描述脚本及其语言的对象。下表列出了可以配置的可能设置：

**表 88.脚本有效负载转换设置**

姓名 |必填 |默认 |描述 ---|---|---|--- 'inline'

|

yes

|

-

|

使用内联脚本时，此字段保存脚本本身。   'id'

|

yes

|

-

|

引用存储的脚本时，此字段保存脚本的 ID。   "郎"

|

no

|

`painless`

|

脚本语言"参数"

|

no

|

-

|

脚本可访问的其他参数/变量 使用脚本的对象表示法时，必须定义一个(且仅一个)"内联"或"id"字段。

除了提供的"参数"之外，脚本还可以访问标准的监视执行上下文参数。

[« Watcher search payload transform](transform-search.md) [Watcher chain
payload transform »](transform-chain.md)
