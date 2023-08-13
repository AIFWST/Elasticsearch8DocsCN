

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« SQL CLI](sql-cli.md) [API usage »](_api_usage.md)

## SQLJDBC

Elasticsearch 的 SQL jdbc 驱动程序是一个功能丰富、功能齐全的 JDBC 驱动程序，用于 Elasticsearch。它是Type 4驱动程序，这意味着它是一个独立于平台的，独立的，直接到数据库的纯Java驱动程序，它将JDBC调用转换为Elasticsearch SQL。

###Installation

JDBC 驱动程序可从以下位置获取：

专用页面

     [elastic.co](/downloads/jdbc-client) provides links, typically for manual downloads. 
Maven dependency

     [Maven](https://maven.apache.org/)-compatible tools can retrieve it automatically as a dependency: 
    
    
    <dependency>
      <groupId>org.elasticsearch.plugin</groupId>
      <artifactId>x-pack-sql-jdbc</artifactId>
      <version>8.9.0</version>
    </dependency>

从Maven CentralRepository，或从"artifacts.elastic.co/maven"将其添加到存储库列表中：

    
    
    <repositories>
      <repository>
        <id>elastic.co</id>
        <url>https://artifacts.elastic.co/maven</url>
      </repository>
    </repositories>

### 版本兼容性

您的驱动程序必须与您的 Elasticsearch 服务器版本兼容。

驱动程序版本不能比 Elasticsearch 服务器版本更新。例如，7.10.0 服务器与 8.9.0 驱动程序不兼容。

弹性搜索服务器版本 |兼容的驱动程序版本 |示例 ---|---|--- 8.0.0–8.9.0

|

* 相同版本 * 任何早期的 8.x 版本 * 7.7.0 之后的任何 7.x 版本。

|

8.9.0 服务器与 8.9.0 及更早版本的 8.x 驱动程序兼容。8.9.0 服务器还与 7.7.0 及更高版本的 7.x 驱动程序兼容。   7.7.1-7.17

|

* 相同版本 * 早期的 7.x 版本，回到 7.7.0。

|

7.10.0 服务器与 7.7.0-7.10.0 驱动程序兼容。   7.7.0 及更早版本

|

* 版本相同。

|

7.6.1 服务器仅与 7.6.1 驱动程序兼容。   ###Setupedit

驱动程序主类是"org.elasticsearch.xpack.sql.jdbc.EsDriver"。请注意，驱动程序实现了 JDBC 4.0"服务提供程序"机制，这意味着只要它在类路径中可用，它就会自动注册。

注册后，驱动程序会将以下语法理解为 URL：

    
    
    jdbc:[es|elasticsearch]://[[http|https]://]?[host[:port]]?/[prefix]?[\?[option=value]&]*

`jdbc:[es|elasticsearch]://`

     Prefix. Mandatory. 
`[[http|https]://]`

     Type of HTTP connection to make. Possible values are `http` (default) or `https`. Optional. 
`[host[:port]]`

     Host (`localhost` by default) and port (`9200` by default). Optional. 
`[prefix]`

     Prefix (empty by default). Typically used when hosting Elasticsearch under a certain path. Optional. 
`[option=value]`

     Properties for the JDBC driver. Empty by default. Optional. 

驱动程序识别以下属性：

#####Essential

"时区"(默认 JVM 时区)

     Timezone used by the driver _per connection_ indicated by its `ID`. **Highly** recommended to set it (to, say, `UTC`) as the JVM timezone can vary, is global for the entire JVM and can't be changed easily when running under a security manager. 

#####Network

"连接超时"(默认为"30000")

     Connection timeout (in milliseconds). That is the maximum amount of time waiting to make a connection to the server. 
`network.timeout` (default `60000`)

     Network timeout (in milliseconds). That is the maximum amount of time waiting for the network. 
`page.size` (default `1000`)

     Page size (in entries). The number of results returned per page by the server. 
`page.timeout` (default `45000`)

     Page timeout (in milliseconds). Minimum retention period for the scroll cursor on the server. Queries that require a stateful scroll cursor on the server side might fail after this timeout. Hence, when scrolling through large result sets, processing `page.size` records should not take longer than `page.timeout` milliseconds. 
`query.timeout` (default `90000`)

     Query timeout (in milliseconds). That is the maximum amount of time waiting for a query to return. 

#### 基本身份验证

`user`

     Basic Authentication user name 
`password`

     Basic Authentication password 

####SSL

"SSL"(默认为"假")

     Enable SSL 
`ssl.keystore.location`

     key store (if used) location 
`ssl.keystore.pass`

     key store password 
`ssl.keystore.type` (default `JKS`)

     key store type. `PKCS12` is a common, alternative format 
`ssl.truststore.location`

     trust store location 
`ssl.truststore.pass`

     trust store password 
`ssl.truststore.type` (default `JKS`)

     trust store type. `PKCS12` is a common, alternative format 
`ssl.protocol`(default `TLS`)

     SSL protocol to be used 

####Proxy

`proxy.http`

     Http proxy host name 
`proxy.socks`

     SOCKS proxy host name 

####Mapping

'field.multi.value.leniency' (默认 'true')

     Whether to be lenient and return the first value (without any guarantees of what that will be - typically the first in natural ascending order) for fields with multiple values (true) or throw an exception. 

####Index

'index.include.frozen' (默认为'false')

     Whether to include frozen indices in the query execution or not (default). 

####Cluster

`catalog`

    

查询的默认目录(群集)。如果未指定，则查询仅对本地群集中的数据执行。

preview] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 请参阅 [跨集群搜索。

#### 错误处理

'allow.partial.search.results'(默认为'false')

     Whether to return partial results in case of shard failure or fail the query throwing the underlying exception (default). 

####Troubleshooting

"调试"(默认为"假")

     Setting it to `true` will enable the debug logging. 
`debug.output` (default `err`)

     The destination of the debug logs. By default, they are sent to standard error. Value `out` will redirect the logging to standard output. A file path can also be specified. 

####Additional

"验证属性"(默认为"true")

     If disabled, it will ignore any misspellings or unrecognizable properties. When enabled, an exception will be thrown if the provided property cannot be recognized. 

若要将所有这些放在一起，请使用以下 URL：

    
    
    jdbc:es://http://server:3456/?timezone=UTC&page.size=250

在端口"3456"上打开与"服务器"的 Elasticsearch SQL 连接，将 JDBC 连接时区设置为"UTC"，将其页面大小设置为"250"条目。

[« SQL CLI](sql-cli.md) [API usage »](_api_usage.md)
