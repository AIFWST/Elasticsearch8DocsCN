

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Local gateway settings](modules-gateway.md) [Machine learning settings in
Elasticsearch »](ml-settings.md)

##Logging

您可以使用 Elasticsearch 的应用程序日志来监控集群并诊断问题。如果您将 Elasticsearch 作为服务运行，则日志的默认位置因您的平台和安装方法而异：

Docker Debian (APT) RPM macOS Linux Windows .zip

在 Docker 上，日志消息转到控制台，并由配置的 Docker 日志记录驱动程序处理。要访问日志，请运行"码头工人日志"。

对于 Debian 安装，Elasticsearch 将日志写入 '/var/log/elasticsearch'。

对于 RPM 安装，Elasticsearch 将日志写入 '/var/log/elasticsearch'。

对于macOS".tar.gz"安装，Elasticsearch会将日志写入"$ES_HOME/logs"。

升级过程中，"$ES_HOME"中的文件存在删除风险。在生产环境中，我们强烈建议您将"path.logs"设置为"$ES_HOME"之外的位置。请参阅路径设置。

对于 Linux '.tar.gz' 安装，Elasticsearch 会将日志写入 '$ES_HOME/logs' 中。

升级过程中，"$ES_HOME"中的文件存在删除风险。在生产环境中，我们强烈建议您将"path.logs"设置为"$ES_HOME"之外的位置。请参阅路径设置。

对于 Windows'.zip' 安装，Elasticsearch 会将日志写入 '%ES_HOME%\logs'。

"%ES_HOME%"中的文件在升级过程中存在删除风险。在生产环境中，我们强烈建议您将"path.logs"设置为"%ES_HOME%"之外的位置。请参阅路径设置。

如果从命令行运行 Elasticsearch，Elasticsearch 会将日志打印到标准输出("stdout")。

### 日志记录配置

Elastic 强烈建议使用默认提供的 Log4j 2 配置。

Elasticsearch 使用 Log4j 2 进行日志记录。可以使用 log4j2.properties 文件配置 Log4j 2。Elasticsearch 公开了三个属性，'${sys：es.logs.base_path}'、'${sys：es.logs.cluster_name}' 和 '${sys：es.logs.node_name}'，可以在配置文件中引用它们来确定日志文件的位置。属性"${sys：es.logs.base_path}"将解析为 logdirectory，"${sys：es.logs.cluster_name}"将解析为群集名称(在默认配置中用作日志文件名的前缀)，而"${sys：es.logs.node_name}"将解析为节点名称(如果显式设置了节点名称)。

例如，如果您的日志目录('path.logs')是'/var/log/elasticsearch'，而你的集群名为'production'，那么'${sys：es.logs.base_path}'将解析为'/var/log/elasticsearch'和'${sys：es.logs.base_path}${sys：file.separator}${sys：es.logs.cluster_name}.log'将解析为'/var/log/elasticsearch/production.log'。

    
    
    ######## Server JSON ############################
    appender.rolling.type = RollingFile __appender.rolling.name = rolling
    appender.rolling.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}_server.json __appender.rolling.layout.type = ECSJsonLayout __appender.rolling.layout.dataset = elasticsearch.server __appender.rolling.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}-%d{yyyy-MM-dd}-%i.json.gz __appender.rolling.policies.type = Policies
    appender.rolling.policies.time.type = TimeBasedTriggeringPolicy __appender.rolling.policies.time.interval = 1 __appender.rolling.policies.time.modulate = true __appender.rolling.policies.size.type = SizeBasedTriggeringPolicy __appender.rolling.policies.size.size = 256MB __appender.rolling.strategy.type = DefaultRolloverStrategy
    appender.rolling.strategy.fileIndex = nomax
    appender.rolling.strategy.action.type = Delete __appender.rolling.strategy.action.basepath = ${sys:es.logs.base_path}
    appender.rolling.strategy.action.condition.type = IfFileName __appender.rolling.strategy.action.condition.glob = ${sys:es.logs.cluster_name}-* __appender.rolling.strategy.action.condition.nested_condition.type = IfAccumulatedFileSize __appender.rolling.strategy.action.condition.nested_condition.exceeds = 2GB __################################################

__

|

配置"滚动文件"追加程序---|--- __

|

登录至 '/var/log/elasticsearch/production_server.json' __

|

使用 JSON 布局。   __

|

"dataset"是填充"ECSJsonLayout"中"event.dataset"字段的标志。在解析不同类型的日志时，它可用于更轻松地区分不同类型的日志。   __

|

将日志滚动到 '/var/log/elasticsearch/production-yyyy-MM-dd-i.json';日志将在每卷上压缩，"i"将递增__

|

使用基于时间的滚动策略 __

|

每天滚动日志 __

|

在日边界上对齐滚动(而不是每 24 小时滚动一次)__

|

使用基于尺寸的滚动策略 __

|

256 MB __ 后滚动日志

|

滚动日志时使用删除操作 __

|

仅删除与文件模式匹配的日志 __

|

模式是仅删除主日志 __

|

仅当我们积累了太多压缩日志时才删除 __

|

压缩日志的大小条件为 2 GB ######## 服务器 - 旧样式模式 ### appender.rolling_old.type = RollingFile appender.rolling_old.name = rolling_old appender.rolling_old.fileName = ${sys：es.logs.base_path}${sys：file.separator}${sys：es.logs.cluster_name}_server.log __appender.rolling_old.layout.type = PatternLayout appender.rolling_old.layout.pattern = [%d{ISO8601}][%-5p][%-25c{1.}][%node_name]%marker %m%n appender.rolling_old.filePattern = ${sys：es.logs.base_path}${sys：file.separator}${sys：es.logs.cluster_name}-%d{yyyy-MM-dd}-%i.old_log.gz

__

|

"旧式"模式追加器的配置。这些日志将保存在"*.log"文件中，如果存档，则将保存在"* .log.gz"文件中。请注意，这些应被视为已弃用，并将在将来删除。   ---|--- Log4j 的配置解析会被任何无关的空格混淆;如果在此页面上复制并粘贴任何 Log4j 设置，或输入任何常规 Log4j配置，请务必修剪任何前导和尾随空格。

请注意，您可以在"appender.rolling.filePattern"中将".gz"替换为".zip"，以使用 zip 格式压缩滚动的日志。如果删除".gz"扩展名，则日志在滚动时不会被压缩。

如果要将日志文件保留指定的时间段，可以将滚动更新策略与删除操作一起使用。

    
    
    appender.rolling.strategy.type = DefaultRolloverStrategy __appender.rolling.strategy.action.type = Delete __appender.rolling.strategy.action.basepath = ${sys:es.logs.base_path} __appender.rolling.strategy.action.condition.type = IfFileName __appender.rolling.strategy.action.condition.glob = ${sys:es.logs.cluster_name}-* __appender.rolling.strategy.action.condition.nested_condition.type = IfLastModified __appender.rolling.strategy.action.condition.nested_condition.age = 7D __

__

|

配置"默认滚动更新策略"---|---__

|

配置"删除"操作以处理翻转 __

|

Elasticsearch 日志的基本路径 __

|

处理展期时适用的条件 __

|

从与 glob'${sys：es.logs.cluster_name}-*' 匹配的基本路径中删除文件;这是日志文件滚动到的 glob;这需要只删除滚动的 Elasticsearch 日志，而不是删除弃用和慢日志 __

|

要应用于与 glob __ 匹配的文件的嵌套条件

|

将日志保留七天 可以加载多个配置文件(在这种情况下，它们将被合并)，只要它们被命名为"log4j2.properties"并且具有Elasticsearch配置目录作为祖先;这对于公开其他记录器的插件很有用。记录器部分包含 java 包及其相应的日志级别。追加器部分包含日志的目标。有关如何自定义日志记录和所有支持的追加程序的大量信息，请参见 Log4j文档。

### 配置日志记录级别

Elasticsearch 源代码中的每个 Java 包都有一个相关的记录器。例如，"org.elasticsearch.discovery"包包含与发现过程相关的日志的"logger.org.elasticsearch.discovery"。

若要获取或多或少的详细日志，请使用群集更新设置 API 更改相关记录器的日志级别。每个记录器都接受 Log4j 2 的内置日志级别，从最不详细到最详细："关闭"、"致命"、"错误"、"警告"、"信息"、"调试"和"跟踪"。默认日志级别为"INFO"。以较高详细级别("调试"和"跟踪")记录的消息仅供专家使用。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.discovery": 'DEBUG'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.discovery": "DEBUG"
      }
    }

要将记录器的详细程度重置为其默认级别，请将记录器设置设置为"null"：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.discovery": nil
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.discovery": null
      }
    }

更改日志级别的其他方法包括：

1. 'elasticsearch.yml'： logger.org.elasticsearch.discovery： DEBUG

这在调试单个节点上的问题时最合适。

2. 'log4j2.properties'： logger.discovery.name = org.elasticsearch.discovery logger.discovery.level = debug

当您已经出于其他原因需要更改 Log4j 2 配置时，这是最合适的。例如，您可能希望将特定记录器的日志发送到另一个文件。但是，这些用例很少见。

### 弃用日志记录

Elasticsearch 还将弃用日志写入日志目录。这些日志记录您使用已弃用的 Elasticsearch 功能时的消息。在将 Elasticsearch 升级到新的主要版本之前，您可以使用弃用日志来更新应用程序。

默认情况下，Elasticsearch 会以 1GB 的速度滚动和压缩弃用日志。默认配置最多保留五个日志文件：四个滚动日志和一个活动日志。

Elasticsearch 在"关键"级别发出弃用日志消息。这些消息指示已使用的弃用功能将在下一个主要版本中删除。"WARN"级别的弃用日志消息表明使用了不太重要的功能，它不会在下一个主要版本中删除，但将来可能会被删除。

要停止写入弃用日志消息，请在"log4j2.properties"中将"logger.deprecation.level"设置为"OFF"：

    
    
    logger.deprecation.level = OFF

或者，您可以动态更改日志记录级别：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.deprecation": 'OFF'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.deprecation": "OFF"
      }
    }

请参阅配置日志记录级别。

如果将"X-Opaque-Id"用作 HTTP 标头，则可以确定触发已弃用功能的原因。用户 ID 包含在弃用 JSON 日志中的"X-Opaque-ID"字段中。

    
    
    {
      "type": "deprecation",
      "timestamp": "2019-08-30T12:07:07,126+02:00",
      "level": "WARN",
      "component": "o.e.d.r.a.a.i.RestCreateIndexAction",
      "cluster.name": "distribution_run",
      "node.name": "node-0",
      "message": "[types removal] Using include_type_name in create index requests is deprecated. The parameter will be removed in the next major version.",
      "x-opaque-id": "MY_USER_ID",
      "cluster.uuid": "Aq-c-PAeQiK3tfBYtig9Bw",
      "node.id": "D7fUYfnfTLa2D7y-xw6tZg"
    }

弃用日志可以索引到".logs-deprecation.elasticsearch-default"数据流"cluster.deprecation_indexing.enabled"设置设置为 true。

### 弃用日志限制

弃用日志根据已弃用的功能密钥和 x-opaque-id 进行重复数据删除，以便在重复使用某项功能时，它不会过载弃用日志。这适用于索引弃用日志和日志修复日志文件。您可以通过将"cluster.deprecation_indexing.x_opaque_id_used.enabled"更改为false来禁用在限制中使用"x-opaque-id"，有关更多详细信息，请参阅此类javadoc。

### JSON 日志格式

为了更容易解析 Elasticsearch 日志，日志现在以 JSON 格式打印。这是由 Log4J 布局属性'appender.rolling.layout.type = ECSJsonLayout'配置的。此布局需要设置"数据集"属性，该属性用于在解析时区分日志流。

    
    
    appender.rolling.layout.type = ECSJsonLayout
    appender.rolling.layout.dataset = elasticsearch.server

每行包含一个 JSON 文档，其中包含在"ECSJsonLayout"中配置的属性。有关更多详细信息，请参阅此类javadoc。但是，如果 JSON 文档包含异常，它将跨多行打印。第一行将包含常规属性，后续行将包含格式化为 JSON 数组的堆栈跟踪。

您仍然可以使用自己的自定义布局。为此，将"appender.rolling.layout.type"行替换为不同的布局。请参阅下面的示例：

    
    
    appender.rolling.type = RollingFile
    appender.rolling.name = rolling
    appender.rolling.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}_server.log
    appender.rolling.layout.type = PatternLayout
    appender.rolling.layout.pattern = [%d{ISO8601}][%-5p][%-25c{1.}] [%node_name]%marker %.-10000m%n
    appender.rolling.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}-%d{yyyy-MM-dd}-%i.log.gz

[« Local gateway settings](modules-gateway.md) [Machine learning settings in
Elasticsearch »](ml-settings.md)
