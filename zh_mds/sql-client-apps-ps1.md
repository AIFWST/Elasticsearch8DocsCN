

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Client Applications](sql-client-apps.md)

[« Microsoft Power BI Desktop](sql-client-apps-powerbi.md) [MicroStrategy
Desktop »](sql-client-apps-microstrat.md)

## 微软PowerShell

您可以使用 Elasticsearch ODBC 驱动程序从 Microsoft PowerShell 访问 Elasticsearch 数据。

Elastic 不认可、推广或支持此应用程序;对于本产品中的原生 Elasticsearch 集成，请联系其供应商。

###Prerequisites

* Microsoft PowerShell * Elasticsearch SQL ODBC 驱动程序 * 预配置的用户或系统 DSN(有关如何配置 DSN 的信息，请参阅"配置"部分)。

### 编写脚本

虽然将以下说明放入脚本文件不是绝对要求，但这样做将使其更易于扩展和重用。以下说明举例说明了如何使用预先配置的 DSN 从 Elasticsearch 实例中的现有索引执行简单的 SELECT 查询。打开一个新文件"select.ps1"，并在其中放置以下说明：

    
    
    $connectstring = "DSN=Local Elasticsearch;"
    $sql = "SELECT * FROM library"
    
    $conn = New-Object System.Data.Odbc.OdbcConnection($connectstring)
    $conn.open()
    $cmd = New-Object system.Data.Odbc.OdbcCommand($sql,$conn)
    $da = New-Object system.Data.Odbc.OdbcDataAdapter($cmd)
    $dt = New-Object system.Data.datatable
    $null = $da.fill($dt)
    $conn.close()
    $dt

现在打开一个PowerShell shell并简单地执行脚本：

**在PowerShell中运行SQL**！apps ps exed

[« Microsoft Power BI Desktop](sql-client-apps-powerbi.md) [MicroStrategy
Desktop »](sql-client-apps-microstrat.md)
