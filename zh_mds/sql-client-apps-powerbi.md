

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« Microsoft Excel](sql-client-apps-excel.md) [Microsoft PowerShell »](sql-
client-apps-ps1.md)

## Microsoft Power BIDesktop

您可以使用 Elasticsearch ODBC 驱动程序从 Microsoft Power BI Desktop 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* Microsoft Power BI Desktop 2.63 或更高版本 * Elasticsearch SQL ODBC 驱动程序 * 预配置的用户或系统 DSN(有关如何配置 DSN 的信息，请参阅"配置"部分)。

### 数据加载

首先，需要选择 ODBC 作为从中加载数据的源。启动后，单击_Get Data_按钮(在_Home_选项卡下)，然后单击列表底部的_More..._按钮：

**获取数据 / 更多 ...**！apps pbifromodbc1

在新打开的窗口中，滚动_All_列表底部并选择the_ODBC_条目，然后单击_Connect_按钮：

**ODBC / Connect**！apps pbifromodbc2

这会将当前窗口替换为新的_From ODBC_窗口，您必须在其中选择以前配置的 DSN：

**选择一个 DSN**！应用程序 pbi dsn

连接后，Power BI 将读取 Elasticsearch 的目录，并为用户提供要从中加载数据的表(索引)选择。单击其中一个表将加载以下数据中的预览：

**选择要加载的表**！应用程序 pbipickable

现在勾选所选表并单击_加载_按钮。Power BI 现在将加载和分析数据，并使用可用列填充列表。这些现在可用于构建所需的可视化：

**可视化数据**！应用程序 pbi 已加载

[« Microsoft Excel](sql-client-apps-excel.md) [Microsoft PowerShell »](sql-
client-apps-ps1.md)
