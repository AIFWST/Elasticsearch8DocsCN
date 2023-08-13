

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« SQL Translate API](sql-translate.md) [SQL JDBC »](sql-jdbc.md)

## SQLCLI

Elasticsearch 附带了一个脚本，用于在其"bin"目录中运行 SQL CLI：

    
    
    $ ./bin/elasticsearch-sql-cli

您可以将要连接的 Elasticsearch 实例的 URL 作为第一个参数传递：

    
    
    $ ./bin/elasticsearch-sql-cli https://some.server:9200

如果在群集上启用了安全性，则可以将用户名和密码以"用户名：password@host_name：端口"的形式传递给 SQL CLI：

    
    
    $ ./bin/elasticsearch-sql-cli https://sql_user:strongpassword@some.server:9200

一旦 CLI 运行，您就可以使用 Elasticsearch 支持的任何查询：

    
    
    sql> SELECT * FROM library WHERE page_count > 500 ORDER BY page_count DESC;
         author      |        name        |  page_count   | release_date
    -----------------+--------------------+---------------+---------------
    Peter F. Hamilton|Pandora's Star      |768            |1078185600000
    Vernor Vinge     |A Fire Upon the Deep|613            |707356800000
    Frank Herbert    |Dune                |604            |-144720000000
    Alastair Reynolds|Revelation Space    |585            |953078400000
    James S.A. Corey |Leviathan Wakes     |561            |1306972800000

包含 SQL CLI 的 jar 是一个独立的 Java 应用程序，脚本只是启动它。你可以把它移到其他机器上，而不必在上面安装 Elasticsearch。如果没有已提供的脚本文件，则可以使用类似于以下内容的命令来启动 SQL CLI：

    
    
    $ ./java -jar [PATH_TO_CLI_JAR]/elasticsearch-sql-cli-[VERSION].jar https://some.server:9200

or

    
    
    $ ./java -cp [PATH_TO_CLI_JAR]/elasticsearch-sql-cli-[VERSION].jar org.elasticsearch.xpack.sql.cli.Cli https://some.server:9200

每个 Elasticsearch 版本的 jar 名称都会不同(例如 'elasticsearch-sql-cli-7.3.2.jar')，因此在上面的例子中指定的通用 'VERSION'。此外，如果不从 SQL CLI jar 所在的文件夹运行命令，则还必须提供完整路径。

### CLI命令

除了SQL查询，CLI还可以执行一些特定的命令：

'allow_partial_search_results = '<boolean>(默认为'假')

     If `true`, returns partial results if there are shard request timeouts or [shard failures](docs-replication.html#shard-failures "Shard failures"). If `false`, returns an error with no partial results. 
    
    
    sql> allow_partial_search_results = true;
    allow_partial_search_results set to true

"fetch_size = <number>"(默认值"1000")

     Allows to change the size of fetches for query execution. Each fetch is delimited by fetch separator (if explicitly set). 
    
    
    sql> fetch_size = 2000;
    fetch size set to 2000

'fetch_separator = <string>'(默认为空字符串)

     Allows to change the separator string between fetches. 
    
    
    sql> fetch_separator = "---------------------";
    fetch separator set to "---------------------"

"宽松 = <boolean>"(默认为"假")

     If `false`, Elasticsearch SQL returns an error for fields containing [array values](array.html "Arrays"). If `true`, Elasticsearch SQL returns the first value from the array with no guarantee of consistent results. 
    
    
    sql> lenient = true;
    lenient set to true

`info`

     Returns server information. 
    
    
    sql> info;
    Node:mynode Cluster:elasticsearch Version:8.3

`exit`

     Closes the CLI. 
    
    
    sql> exit;
    Bye!

`cls`

     Clears the screen. 
    
    
    sql> cls;

`logo`

     Prints Elastic logo. 
    
    
    sql> logo;
    
                           asticElasticE
                         ElasticE  sticEla
              sticEl  ticEl            Elast
            lasti Elasti                   tic
          cEl       ast                     icE
         icE        as                       cEl
         icE        as                       cEl
         icEla     las                        El
       sticElasticElast                     icElas
     las           last                    ticElast
    El              asti                 asti    stic
    El              asticEla           Elas        icE
    El            Elas  cElasticE   ticEl           cE
    Ela        ticEl         ticElasti              cE
     las     astic               last              icE
       sticElas                   asti           stic
         icEl                      sticElasticElast
         icE                       sticE   ticEla
         icE                       sti       cEla
         icEl                      sti        Ela
          cEl                      sti       cEl
           Ela                    astic    ticE
             asti               ElasticElasti
               ticElasti  lasticElas
                  ElasticElast
    
                           SQL
                          8.3.0

[« SQL Translate API](sql-translate.md) [SQL JDBC »](sql-jdbc.md)
