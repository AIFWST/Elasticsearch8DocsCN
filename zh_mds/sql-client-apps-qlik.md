

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« MicroStrategy Desktop](sql-client-apps-microstrat.md) [SQuirreL SQL
»](sql-client-apps-squirrel.md)

## Qlik SenseDesktop

您可以使用 Elasticsearch ODBC 驱动程序从 Qlik Sense Desktop 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* Qlik Sense Desktop 2018 年 11 月或更高版本 * Elasticsearch SQL ODBC 驱动程序 * 预配置的用户或系统 DSN(有关如何配置 DSN 的信息，请参阅配置部分)。

### 数据加载

要使用 Elasticsearch SQL ODBC 驱动程序将数据加载到 Qlik Sense 桌面，请按顺序执行以下步骤。

1. 创建新应用

应用程序启动后，您首先需要单击_Createnew app_按钮：

！Apps Qlik newapp

2. 命名应用

...​然后给它起个名字，

！Apps Qlik Create

3. 打开应用程序

...​然后打开它：

！应用程序 Qlik 打开

4. 向应用添加数据

开始配置源以从新创建的应用程序中加载数据：

！apps qlik adddata

5. 从 ODBC 加载

您可以选择要选择的来源。单击 _ODBC_ 图标：

！Apps Qlik ODBC

6. 选择DSN

在"_Create新连接 (ODBC)_"对话框中，单击之前为 Elasticsearch 实例配置的 DSN 名称：

！Apps Qlik DSN

如果您的实例上启用了身份验证，并且这些用户名和密码尚未成为 DSN 的一部分，请在相应的字段中提供用户名和密码。按 _创建_ 按钮。

7. 选择源表

应用程序现在将连接到 Elasticsearch 实例并查询目录信息，并为您提供可从中加载数据的表列表：

！Apps Qlik Selecttable

8. 可视化数据

按下_Add data_按钮并自定义数据可视化：

！Apps Qlik Visualize

[« MicroStrategy Desktop](sql-client-apps-microstrat.md) [SQuirreL SQL
»](sql-client-apps-squirrel.md)
