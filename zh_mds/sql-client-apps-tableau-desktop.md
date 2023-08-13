

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« SQL Workbench/J](sql-client-apps-workbench.md) [Tableau Server »](sql-
client-apps-tableau-server.md)

## 桌面

使用 Elasticsearch JDBC 驱动程序和专用的 Elasticsearch TableauConnector 从 Tableau Desktop 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* Tableau Desktop 2019.4 或更高版本 * Elasticsearch SQL JDBC 驱动程序 * Elasticsearch Connector for Tableau

### 加载数据

首先，将 JDBC 驱动程序移动或下载到 Tableau Desktop 驱动程序目录：

* Windows： 'C：\Program Files\Tableau\Drivers' * Mac： '/Users/[user]/Library/Tableau/Drivers'

将适用于 Tableau 的 Elasticsearch Connector 移动到 Tableau Desktop 连接器目录：

* Windows： 'C：\Users\[Windows User]\Documents\My Tableau Repository\Connectors' * Mac： '/Users/[user]/Documents/My Tableau Repository/Connectors'

启动 Tableau Desktop。在菜单中，单击"**更多...**"，然后选择"由 Elastic** 进行的 Elasticsearch"作为数据源。

!选择 Elasticsearch by Elastic 作为数据源

在"新建连接**"模式中，输入 Elasticsearchinstance 的信息，然后单击"登录"。

!登录

在主窗口中，选择您的 Elasticsearch 实例作为 **数据库**。然后选择要加载的表。

!选择要加载的表

最后，生成报告。

!生成报告

[« SQL Workbench/J](sql-client-apps-workbench.md) [Tableau Server »](sql-
client-apps-tableau-server.md)
