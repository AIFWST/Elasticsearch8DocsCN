

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« DbVisualizer](sql-client-apps-dbvis.md) [Microsoft Power BI Desktop
»](sql-client-apps-powerbi.md)

## 微软Excel

您可以使用 Elasticsearch ODBC 驱动程序从 Microsoft Excel 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* Microsoft Office 2016 或更高版本 * Elasticsearch SQL ODBC 驱动程序 预配置的用户或系统 DSN(有关如何配置 DSN 的信息，请参阅"配置"部分)。

### 将数据加载到电子表格中

首先，需要选择 ODBC 作为从中加载数据的源。为此，请单击 _Data_ 选项卡，然后单击下拉菜单中的_New Query_按钮 expand_From 其他Sources_ ，然后选择_From ODBC_：

**ODBC 作为数据源**！apps excelfromodbc

这将打开一个新窗口，其中包含一个下拉菜单，其中填充了Excel在系统上找到的DSN。选择配置为连接到弹性搜索实例的 DSN，然后按 _OK_ 按钮：

**选择一个 DSN**！应用程序 excel dsn

这将导致一个新窗口，允许用户输入连接凭据。

即使 Elasticsearch 实例未启用安全性，Excel 也可能需要用户名。在这种情况下，提供没有密码的虚假用户名不会妨碍连接。但请注意，Excel 将缓存这些凭据(因此，如果您启用了安全性，则不会再次提示您输入凭据)。

填写用户名和密码，然后按 _Connect_。

**提供连接凭据**！应用程序已出色

连接后，Excel 将读取 Elasticsearch 的目录，并为用户提供从中加载数据的表(索引)选择。单击其中一个表将加载以下数据中的预览：

**选择要加载的表**！应用程序Excelpickable

现在单击 _Load_ 按钮，这将使 Excel 将表中的所有数据加载到电子表格中：

**数据加载到电子表格中**！应用程序出色加载

[« DbVisualizer](sql-client-apps-dbvis.md) [Microsoft Power BI Desktop
»](sql-client-apps-powerbi.md)
