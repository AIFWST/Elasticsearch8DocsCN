

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher conditions](condition.md)

[« Watcher compare condition](condition-compare.md) [Watcher script
condition »](condition-script.md)

## 观察程序数组比较条件

使用"array_compare"将执行上下文中的值数组与给定值进行比较。有关可以使用的运算符，请参阅表 81。

### 使用数组比较条件

要使用"array_compare"条件，请在执行上下文中指定要评估的数组、比较运算符以及要比较的值。(可选)可以在要计算的每个数组元素中指定字段的路径。

例如，如果聚合中至少有一个存储桶的"doc_count"大于等于 25，则以下"array_compare"条件返回"true"：

    
    
    {
      "condition": {
        "array_compare": {
          "ctx.payload.aggregations.top_tweeters.buckets" : { __"path": "doc_count", __"gte": { __"value": 25 __}
          }
        }
      }
    }

__

|

要计算的执行上下文中数组的路径，以点表示法指定。   ---|---    __

|

要计算的每个数组元素中的字段的路径。   __

|

要使用的比较运算符。   __

|

比较值。支持日期数学，如比较条件。   使用包含点的字段名称时，此条件将不起作用，请改用 ascript 条件。

### 数组比较条件属性

姓名 |说明 ---|--- '<数组路径>'

|

执行上下文中数组的路径，以点表示法指定。例如，"ctx.payload.aggregations.top_tweeters.buckets"。   "<数组路径>.路径"

|

要计算的每个数组元素中的字段的路径。例如，"doc_count"。默认为空字符串。   "<阵列路径>。<operator>.量词'

|

比较需要多少匹配项才能评估为"true"："部分"或"全部"。默认为"一些"\-必须至少有一个匹配项。如果数组为空，则如果量词设置为"all"，则比较结果为"true";如果量词设置为"some"，则计算结果为"false"。   "<阵列路径>。<operator>.值'

|

要比较的值。   « 观察程序比较条件 观察程序脚本条件 »