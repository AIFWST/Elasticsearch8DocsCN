

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« SQuirreL SQL](sql-client-apps-squirrel.md) [Tableau Desktop »](sql-
client-apps-tableau-desktop.md)

## SQLWorkbench/J

您可以使用 Elasticsearch JDBC 驱动程序从 SQL Workbench/J 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* SQL Workbench/J build 125 或更高版本 * Elasticsearch SQL JDBC 驱动程序

### 添加 Elasticsearch JDBCdriver

将 Elasticsearch JDBC 驱动程序通过 **ManageDrivers** 添加到 SQL Workbench/J 中，无论是从主窗口的 **File** 菜单还是从 **Connect** 窗口：

！工作台 1 管理驱动程序

从左侧选择**Elasticsearch**配置文件(如果缺少，请检查SQL Workbench/J版本或通过左上角的空白页按钮向列表中添加新条目)：

工作台 2 选择驱动程序

添加 JDBC jar(如果尚未选取驱动程序名称，请单击放大镜按钮)：

！工作台 3 添加罐子

### 创建新的连接配置文件

配置驱动程序后，通过 **文件** >**连接窗口**(或 Alt+C 快捷方式)创建新的连接配置文件：

！工作台 4 连接

选择以前配置的驱动程序，并使用 JDBC 语法设置集群的 URL。通过**测试**按钮验证连接 - 应出现确认窗口，表明所有内容均已正确配置。

设置完成。

### 执行 SQL 查询

SQL Workbench/J 已准备好通过 SQL 与 Elasticsearch 通信：单击创建的配置文件以执行语句或浏览数据：

工作台 5 数据

[« SQuirreL SQL](sql-client-apps-squirrel.md) [Tableau Desktop »](sql-
client-apps-tableau-desktop.md)
