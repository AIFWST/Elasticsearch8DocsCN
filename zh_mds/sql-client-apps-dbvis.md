

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« DBeaver](sql-client-apps-dbeaver.md) [Microsoft Excel »](sql-client-apps-
excel.md)

##DbVisualizer

您可以使用 Elasticsearch JDBC 驱动程序从 DbVisualizer 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序。

###Prerequisites

* DbVisualizer 13.0 或更高版本 * Elasticsearch SQL JDBC 驱动程序

Note

     Pre 13.0 versions of DbVisualizer can still connect to Elasticsearch by having the [JDBC driver](sql-jdbc.html "SQL JDBC") set up from the generic **Custom** template. 

### 设置 Elasticsearch JDBCdriver

通过 **工具** > **驱动程序管理器** 设置 Elasticsearch JDBC 驱动程序：

！dbvis 1 驱动程序管理器

从左侧边栏中选择**Elasticsearch**驱动程序模板以创建新的用户驱动程序：

！dbvis 2 driver manager elasticsearch

在本地下载驱动程序：

！dbvis 3 驱动程序管理器下载

并检查其可用性状态：

！dbvis 4 驱动程序管理器准备就绪

### 创建新连接

一旦 Elasticsearch 驱动程序就位，创建一个新连接：

！dbvis 5 new conn

双击可用驱动程序列表中的 Elasticsearch 条目：

！dbvis 6 new conn elasticsearch

输入连接详细信息，然后按**连接**，驱动程序版本(作为群集的版本)应显示在**连接消息**下。

！dbvis 7 new conn connect

### 执行 SQL 查询

设置完成。DbVisualizer 可用于对 stElasticsearch 运行查询并探索其内容：

！dbvis 8 data

[« DBeaver](sql-client-apps-dbeaver.md) [Microsoft Excel »](sql-client-apps-
excel.md)
