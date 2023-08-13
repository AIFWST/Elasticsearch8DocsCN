

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL JDBC](sql-jdbc.md)

[« SQL JDBC](sql-jdbc.md) [SQL ODBC »](sql-odbc.md)

## 接口用法

可以通过官方的"java.sql"和"javax.sql"包使用JDBC：

###'java.sql'

前者通过"java.sql.Driver"和"DriverManager"：

    
    
    String address = "jdbc:es://" + elasticsearchAddress;     __Properties connectionProperties = connectionProperties(); __Connection connection =
        DriverManager.getConnection(address, connectionProperties);

__

|

Elasticsearch 侦听 HTTP 流量的服务器和端口。端口默认为 9200。   ---|---    __

|

用于连接到 Elasticsearch 的属性。空的"属性"实例适用于不安全的 Elasticsearch。   ###'javax.sql'edit

可通过"javax.sql.DataSource"API 访问：

    
    
    EsDataSource dataSource = new EsDataSource();
    String address = "jdbc:es://" + elasticsearchAddress;     __dataSource.setUrl(address);
    Properties connectionProperties = connectionProperties(); __dataSource.setProperties(connectionProperties);
    Connection connection = dataSource.getConnection();

__

|

Elasticsearch 侦听 HTTP 流量的服务器和端口。默认为 9200。   ---|---    __

|

用于连接到 Elasticsearch 的属性。空的"属性"实例适用于不安全的 Elasticsearch。   使用哪一个？通常，在 URL 中提供大多数配置属性的客户端应用程序依赖于"DriverManager"样式，而"数据源"在_传递_时是首选，因为它可以在一个地方配置，使用者只需调用"getConnection"而不必担心任何其他属性。

要连接到安全的Elasticsearch服务器，"属性"应如下所示：

    
    
    Properties properties = new Properties();
    properties.put("user", "test_admin");
    properties.put("password", "x-pack-test-password");

建立连接后，您可以像使用任何其他 JDBC 连接一样使用它。例如：

    
    
    try (Statement statement = connection.createStatement();
            ResultSet results = statement.executeQuery(
                  " SELECT name, page_count"
                + "    FROM library"
                + " ORDER BY page_count DESC"
                + " LIMIT 1")) {
        assertTrue(results.next());
        assertEquals("Don Quixote", results.getString(1));
        assertEquals(1072, results.getInt(2));
        SQLException e = expectThrows(SQLException.class, () ->
            results.getInt(1));
        assertThat(e.getMessage(), containsString("Unable to convert "
                + "value [Don Quixote] of type [TEXT] to [Integer]"));
        assertFalse(results.next());
    }

Elasticsearch SQL 不提供连接池机制，因此 JDBC 驱动程序创建的连接不会被池化。为了实现池化连接，需要第三方连接池机制。配置和设置第三方提供程序超出了本文档的范围。

[« SQL JDBC](sql-jdbc.md) [SQL ODBC »](sql-odbc.md)
