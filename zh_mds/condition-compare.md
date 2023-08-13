

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher conditions](condition.md)

[« Watcher never condition](condition-never.md) [Watcher array compare
condition »](condition-array-compare.md)

## 观察程序比较条件

使用"比较"条件与监视有效负载中的值执行简单比较。您可以使用"比较"条件，而无需启用动态脚本。

**表 81.支持的比较运算符**

姓名 |描述 ---|--- 'eq'

|

当解析的值等于给定的值(适用于数字、字符串、列表、对象和值)时返回 'true' 'not_eq'

|

当解析的值不等于给定的值时返回 'true' (适用于数字、字符串、列表、对象和空值) 'gt'

|

当解析的值大于给定的值时返回"true"(适用于数字和字符串值)"gte"

|

当解析值大于/等于/等于给定值时返回"true"(适用于数字和字符串值)"lt"

|

当解析的值小于给定值时返回"true"(适用于数字和字符串值)"lte"

|

当解析的值小于/等于/等于给定的值时返回 'true' (适用于数字和字符串值) ### 使用比较条件编辑

要使用"比较"条件，请在执行上下文中指定要计算的值、比较运算符以及要与之进行比较的值。例如，如果搜索结果中的总命中数大于或等于 5，则以下"比较"条件返回"true"：

    
    
    {
      "condition" : {
        "compare" : {
          "ctx.payload.hits.total" : { __"gte" : 5 __}
        }
      }
    }

__

|

使用点表示法引用执行上下文中的值。   ---|---    __

|

指定比较运算符和要比较的值。   比较日期和时间时，可以使用形式为"{expression}>"的日期数学表达式<。例如，如果手表在过去五分钟内执行，则以下表达式返回"true"：

    
    
    {
      "condition" : {
        "compare" : {
          "ctx.execution_time" : {
            "gte" : "<{now-5m}>"
          }
        }
      }
    }

您还可以通过将比较值指定为"{{path}}"形式的路径来比较执行上下文中的两个值。例如，以下条件将"ctx.payload.aggregations.status.buckets.error.doc_count"与"ctx.payload.aggregations.handled.buckets.true.doc_count"进行比较：

    
    
    {
      "condition" : {
        "compare" : {
          "ctx.payload.aggregations.status.buckets.error.doc_count" : {
            "not_eq" : "{{ctx.payload.aggregations.handled.buckets.true.doc_count}}"
          }
        }
      }
    }

### 在执行上下文中访问值

您可以使用"点表示法"来访问执行上下文中的值。输入加载到执行上下文中的值以"ctx.payload"为前缀。

您可以使用数组中的条目从零开始的数组索引来引用数组中的条目。例如，要访问"ctx.payload.hits.hits"数组的第三个元素，请使用"ctx.payload.hits.hits.2"。

姓名 |描述 ---|--- 'ctx.watch_id'

|

当前正在执行的监视的 ID。   "ctx.execution_time"

|

此表的时间执行开始。   "ctx.trigger.triggered_time"

|

触发此手表的时间。   "ctx.trigger.scheduled_time"

|

这只手表应该被触发的时间。   'ctx.metadata.*'

|

与监视关联的任何元数据。   'ctx.payload.*'

|

手表输入加载的有效负载数据。   « 观察程序从不条件观察程序数组比较条件 »