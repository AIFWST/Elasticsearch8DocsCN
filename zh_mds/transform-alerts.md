

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Transforming
data](transforms.md)

[« When to use transforms](transform-usage.md) [Working with transforms at
scale »](transform-scale.md)

## 为转换生成警报

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

Kibana 警报功能包括对转换规则的支持，这些规则在特定条件下检查连续转换的运行状况。如果满足规则的条件，则会创建警报并触发关联的操作。例如，您可以创建一个规则来检查连续转换是否已启动，如果未启动，则通过电子邮件通知您。要了解有关 Kibanaalerting 功能的更多信息，请参阅警报。

以下转换规则可用：

转变健康

     Monitors transforms health and alerts if an operational issue occurred. 

### 创建规则

您可以在**堆栈管理>规则**下创建转换规则。

在"**创建规则**"窗口中，为规则命名并选择性地提供标记。选择转换运行状况规则类型：

!创建转换运行状况规则

#### 转换运行状况

选择要包括的一个或多个转换。还可以使用特殊字符 ("*") 将规则应用于所有转换。将自动包括在规则之后创建的转换。

默认情况下，以下运行状况检查可用并处于启用状态：

_Transform不是started_

     Notifies if the corresponding transforms is not started or it does not index any data. The notification message recommends the necessary actions to solve the error. 
_Errors in transform messages_

     Notifies if transform messages contain errors. 

!选择运行状况检查

作为规则创建过程的最后一步，定义其操作。

### 定义操作

您可以向规则添加一个或多个操作，以便在满足条件和不再满足条件时生成通知。

每个操作都使用一个连接器，该连接器存储 Kibanaservice 或受支持的第三方集成的连接信息，具体取决于您要将通知发送到的位置。例如，可以使用 Slack 连接器向频道发送消息。或者，您可以使用将 JSONobject 写入特定索引的索引连接器。有关创建连接器的详细信息，请参阅连接器。

必须设置操作频率，这涉及选择运行操作的频率(例如，在每个检查间隔、仅在警报状态更改时或自定义操作间隔)。每种规则类型还具有有效操作组的列表，您必须选择其中一个组(例如，在检测到问题或恢复问题时运行操作)。

如果选择自定义操作间隔，则它不能短于规则的检查间隔。

还可以自定义每个操作的通知消息。变量列表可用于包含在消息中，例如转换 ID、说明、转换状态等。

!选择连接器类型

保存配置后，规则将显示在"**规则**"列表中，您可以在其中检查其状态并查看其配置信息的概述。

警报的名称始终与触发警报的关联转换的转换 ID 相同。您可以在列出各个警报的规则页面上将特定转换的通知静音。您可以通过选择规则名称通过**规则**打开它。

[« When to use transforms](transform-usage.md) [Working with transforms at
scale »](transform-scale.md)
