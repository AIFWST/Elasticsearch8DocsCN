

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md)

[« Scripting and security](modules-scripting-security.md) [Advanced scripts
using script engines »](modules-scripting-engine.md)

## Lucene 表达式语言

Lucene的表达式将"javascript"表达式编译为字节码。它们专为高性能自定义排名和排序功能而设计，默认情况下启用"内联"和"存储"脚本。

###Performance

表达式旨在与自定义 Lucenecode 具有竞争性能。与其他脚本引擎相比，此性能是由于每个文档的开销较低：表达式执行更多"前期"操作。

这允许非常快速的执行，甚至比编写"本机"脚本还要快。

###Syntax

表达式支持 JavaScript 语法的子集：单个表达式。

有关可用的运算符和函数的详细信息，请参阅表达式模块文档。

"表达式"脚本中的变量可供访问：

* 文档字段，例如 'doc['myfield'].value' * 该字段支持的变量和方法，例如 'doc['myfield'].empty' * 传递到脚本中的参数，例如 'mymodifier' * 当前文档的分数，'_score'(仅在"script_score"中使用时可用)

您可以将表达式脚本用于"script_score"、"script_fields"、排序脚本和数字聚合脚本，只需将"lang"参数设置为"表达式"。

### 数值字段API

表达式 |描述 ---|--- 'doc['field_name'].value'

|

字段的值，作为"双精度""doc[field_name"].空"

|

一个布尔值，指示该字段在文档中是否没有值。   'doc['field_name'].length'

|

本文档中的值数。   'doc['field_name'].min()'

|

本文档中字段的最小值。   'doc['field_name'].max()'

|

本文档中字段的最大值。   'doc['field_name'].median()'

|

本文档中字段的中值。   'doc['field_name'].avg()'

|

本文档中值的平均值。   'doc['field_name'].sum()'

|

本文档中值的总和。   当文档完全缺少该字段时，默认情况下该值将被视为"0"。您可以将其视为另一个值，例如'doc['myfield'].empty ？100 ： doc['myfield'].value'

当文档具有多个字段值时，默认情况下返回最小值。您可以选择不同的值，例如'doc['myfield'].sum()'。

当文档完全缺少该字段时，默认情况下该值将被视为"0"。

布尔字段以数字形式公开，其中"true"映射到"1"，"false"映射到"0"。例如： 'doc['on_sale'].value ？doc['price'].value * 0.5 :d oc['price'].value'

### 日期字段API

日期字段被视为自 1970 年 1 月 1 日以来的毫秒数，并支持上述数值字段 API，以及对某些特定于日期的字段的访问：

表达式 |描述 ---|--- 'doc['field_name'].date.centuryOfEra'

|

世纪 (1-2920000) 'doc['field_name'].date.dayOfMonth'

|

第 (1-31 天)，例如"1"表示每月的第一天。   'doc['field_name'].date.dayOfWeek'

|

星期几 (1-7)，例如"1"表示星期一。   'doc['field_name'].date.dayOfYear'

|

一年中的某一天，例如"1"表示 1 月 1 日。   'doc['field_name'].date.era'

|

时代："0"代表公元前，"1"代表公元。   'doc['field_name'].date.hourOfDay'

|

小时 (0-23)。   'doc['field_name'].date.millisOfDay'

|

一天内的毫秒数 (0-86399999)。   'doc['field_name'].date.millisOfSecond'

|

秒内的毫秒 (0-999)。   'doc['field_name'].date.minuteOfDay'

|

一天中的分钟 (0-1439)。   'doc['field_name'].date.minuteOfHour'

|

一小时内的分钟数 (0-59)。   'doc['field_name'].date.monthOfYear'

|

一年中的月份 (1-12)，例如"1"表示 1 月。   'doc['field_name'].date.secondOfDay'

|

日内秒 (0-86399)。   'doc['field_name'].date.secondOfMinute'

|

秒内(0-59)。   'doc['field_name'].date.year'

|

年份 (-292000000 - 292000000)。   'doc['field_name'].date.yearOfCentury'

|

世纪内的年份(1-100)。   'doc['field_name'].date.yearOfEra'

|

时代内的年份(1-292000000)。   以下示例显示了"date"字段date0 和 date1 之间的年份差异：

'doc['date1'].date.year - doc['date0'].date.year'

### 'geo_point' 字段API

表达式 |描述 ---|--- 'doc['field_name'].empty'

|

一个布尔值，指示该字段在文档中是否没有值。   'doc['field_name'].lat'

|

地理点的纬度。   'doc['field_name'].lon'

|

地理点的经度。   以下示例计算距华盛顿特区的距离(以公里为单位)：

'haversin(38.9072， 77.0369， doc['field_name'].lat， doc['field_name'].lon)'

在此示例中，坐标可以作为参数传递给脚本，例如基于用户的地理位置。

###Limitations

相对于其他脚本语言，有一些限制：

* 只能访问数字、"布尔"、"日期"和"geo_point"字段 * 存储的字段不可用

[« Scripting and security](modules-scripting-security.md) [Advanced scripts
using script engines »](modules-scripting-engine.md)
