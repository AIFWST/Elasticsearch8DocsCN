

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« Tableau Desktop](sql-client-apps-tableau-desktop.md) [SQL Language
»](sql-spec.md)

## 桌面服务器

使用 Elasticsearch JDBC 驱动程序和专用的 Elasticsearch TableauConnector 从 Tableau Server 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* Tableau Server 2019.4 或更高版本 * Elasticsearch SQL JDBC 驱动程序 * Elasticsearch Connector for Tableau

### 加载数据

首先，将 JDBC 驱动程序移动或下载到 Tableau Server 驱动程序目录：

* Windows： 'C：\Program Files\Tableau\Drivers' * Mac： '/Users/[user]/Library/Tableau/Drivers'

将适用于 Tableau 的 Elasticsearch Connector 移动到 Tableau Server 连接器目录。要查找此目录的位置，请参阅 Tableau 服务器文档或使用 TSM 命令行界面。

重新启动 Tableau Server。

若要将数据加载到工作簿中，请从"数据"菜单中添加"新建数据源"或使用图标。在"连接到数据"模式的"连接器"选项卡中，选择"通过 Elastic搜索"。

!选择 Elasticsearch 作为数据源

输入您的 Elasticsearch 实例的信息，然后单击 **登录**。

!登录

在主窗口中，选择您的 Elasticsearch 实例作为 **数据库**。然后选择要加载的表。

!选择要加载的表

最后，生成报告。

!生成报告

[« Tableau Desktop](sql-client-apps-tableau-desktop.md) [SQL Language
»](sql-spec.md)
