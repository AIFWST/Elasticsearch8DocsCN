

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« SQL Client Applications](sql-client-apps.md) [DbVisualizer »](sql-client-
apps-dbvis.md)

##DBeaver

您可以使用 Elasticsearch JDBC 驱动程序从 DBeaver 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* DBeaver 版本 6.0.0 或更高版本 * Elasticsearch SQL JDBC 驱动程序

### 新建连接

通过菜单"文件">"新建">"数据库连接"菜单或直接通过"数据库连接"面板创建新连接。

！dbeaver 1 new conn

### 选择弹性搜索类型

从可用的连接类型中选择 Elasticsearch 类型：

！dbeaver 2 conn es

### 指定 Elasticsearch 集群信息

适当地配置 Elasticsearch SQL 连接：

！海狸 3 康恩道具

### 验证驱动程序版本

通过使用"编辑驱动程序设置"按钮，确保使用正确的 JDBC 驱动程序版本：

！dbeaver 4 驱动程序版本

DBeaver 知道 Elasticsearch JDBC maven 存储库，所以只需**下载/更新**工件或添加新工件即可。作为替代方案，如果Elasticsearch Maven存储库不是一个选项，则可以添加本地文件。

更改驱动程序时，请确保单击底部的"查找类"按钮 - 应自动选择驱动程序类，但这提供了正确找到驱动程序jar并且未损坏的健全性检查。

### 测试连接性

驱动程序版本和设置就绪后，使用**测试连接**检查一切是否正常。如果一切正常，应该得到一个确认窗口，其中包含驱动程序版本和ElasticsearchSQL的版本：

！dbeaver 5 Test Conn

单击"完成"，新的 Elasticsearch 连接将显示在"数据库连接"面板中。

DBeaver 现在配置为与 Elasticsearch 通信。

### 连接到弹性搜索

只需单击 Elasticsearch 连接，即可开始查询和探索 Elasticsearch：

！dbeaver 6 data

[« SQL Client Applications](sql-client-apps.md) [DbVisualizer »](sql-client-
apps-dbvis.md)
