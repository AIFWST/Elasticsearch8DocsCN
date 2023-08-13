

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« Qlik Sense Desktop](sql-client-apps-qlik.md) [SQL Workbench/J »](sql-
client-apps-workbench.md)

## SQuirreLSQL

您可以使用 Elasticsearch JDBC 驱动程序从 SQuirreL SQL 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* SQuirreL SQL 版本 4.0.0 或更高版本 * Elasticsearch SQL JDBC 驱动程序

### 添加 Elasticsearch JDBCDriver

要添加 Elasticsearch JDBC 驱动程序，请使用 **Windows** > **View Drivers** 菜单(或 Ctrl+Shift+D 快捷方式)：

！松鼠 1 查看驱动程序

从左侧的"驱动程序"面板中选择**Elasticsearch**配置文件(如果缺少，请检查SQuirreL SQL版本或通过左上角的"+"按钮向列表中添加新条目)：

松鼠 2 选择驱动程序

选择"额外类路径"选项卡，然后选择"添加"JDBC jar。命名连接和**列出驱动程序**以填充"类名"(如果尚未填写)：

松鼠 3 添加驱动程序

驱动程序现在应出现在列表中，其名称旁边有一个蓝色复选标记：

松鼠4司机列表

### 为弹性搜索添加别名

添加新连接或使用新驱动程序在 SQuirreL 术语中添加一个 _alias_。为此，请选择左侧的"别名"面板，然后单击"+"号：

松鼠 5 添加别名

命名新别名并选择之前添加的"Elasticsearch"驱动程序：

松鼠6别名道具

设置完成。通过单击**测试连接**仔细检查它。

### 执行 SQL 查询

连接应自动打开(如果在只需单击"别名"面板中的"连接"之前已创建连接)。SQuirreL SQL 现在可以向 Elasticsearch 发出 SQL命令：

松鼠 7 数据

[« Qlik Sense Desktop](sql-client-apps-qlik.md) [SQL Workbench/J »](sql-
client-apps-workbench.md)
