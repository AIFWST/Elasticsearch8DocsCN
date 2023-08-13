

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Security limitations](security-limitations.md) [Getting started with
Watcher »](watcher-getting-started.md)

#Watcher

Kibana 警报提供了一组内置操作和警报，这些操作和警报与 APM、指标、安全性和正常运行时间等应用程序集成。您可以使用 Kibana 警报来检测不同 Kibanaapp 中的复杂情况，并在满足这些条件时触发操作。有关详细信息，请参阅警报和操作。

您可以使用观察程序监视数据中的更改或异常，并执行必要的操作作为响应。例如，您可能希望：

*监控社交媒体作为检测面向用户的自动化系统(如ATM或票务系统)故障的另一种方法。当某个区域中的推文和帖子数超过重要性阈值时，请通知服务技术人员。  * 监控您的基础架构，跟踪一段时间内的磁盘使用情况。当任何服务器可能在未来几天内用完可用空间时，请打开帮助台票证。  * 跟踪网络活动以检测恶意活动，并主动更改防火墙配置以拒绝恶意用户。  * 监控 Elasticsearch，当节点离开集群或查询吞吐量超出预期范围时，立即向系统管理员发送通知。  * 跟踪应用程序响应时间，如果页面加载时间超过 SLA 超过 5 分钟，请打开帮助台票证。如果超过SLA一小时，请呼叫值班管理员。

所有这些用例都具有一些关键属性：

* 相关数据或数据变化可以通过定期的 Elasticsearch 查询来识别。  * 可以根据条件检查查询结果。  * 如果条件为 true，则会执行一个或多个操作 - 发送电子邮件、通知第三方系统或存储查询结果。

### 手表的工作原理

警报功能提供用于创建、管理和testing_watches_的 API。监视描述单个警报，并且可以包含多个通知操作。

手表由四个简单的构建块构成：

Schedule

     A schedule for running a query and checking the condition. 
Query

     The query to run as input to the condition. Watches support the full Elasticsearch query language, including aggregations. 
Condition

     A condition that determines whether or not to execute the actions. You can use simple conditions (always true), or use scripting for more sophisticated scenarios. 
Actions

     One or more actions, such as sending email, pushing data to 3rd party systems through a webhook, or indexing the results of the query. 

所有手表的完整历史记录都保存在 Elasticsearch 索引中。此历史记录跟踪每次触发监视的时间，并记录查询结果、是否满足条件以及采取了哪些操作。

[« Security limitations](security-limitations.md) [Getting started with
Watcher »](watcher-getting-started.md)
