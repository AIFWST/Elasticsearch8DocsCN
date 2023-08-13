

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Enable audit logging](enable-audit-
logging.md)

[« Audit events](audit-event-types.md) [Logfile audit events ignore policies
»](audit-log-ignore-policy.md)

## 日志文件审计输出

"日志文件"审核输出是审核的唯一输出。它将数据写入<clustername>日志目录中的"_audit.json"文件。

如果覆盖"log4j2.properties"并且没有为任何审计跟踪指定追加器，则审计事件将转发到根追加器，默认情况下，根追加器指向"elasticsearch.log"文件。

### 日志条目格式

审核事件的格式为 JSON 文档，每个事件都打印在"<clustername>_audit.json"文件中的单独行上。条目本身不包含行尾分隔符。审核事件 JSON 格式有些特殊，因为 **大多数** 字段遵循点名称语法、按顺序排列并包含非空字符串值。此格式创建了一个类似于 CSV 的结构化列方面，可以更轻松地进行目视检查(与等效的嵌套 JSON 文档相比)。

但是，有一些属性是上述格式的例外。"放置"、"删除"、"更改"、"创建"和"无效"属性仅存在于具有"event.type："security_config_change"属性的事件中，其中包含安全更改效果的嵌套 JSON 表示形式。因此，安全配置更改的内容不会在审计事件文档中显示为顶级点命名字段。这是因为这些字段特定于特定类型的安全更改，并且不会显示在任何其他审核事件中。因此，列式格式的好处要有限得多;在这种情况下，嵌套结构节省空间的好处是首选的权衡。

当存在"request.body"属性时(请参阅审核搜索查询)，它包含一个包含完整 HTTP 请求正文的字符串值，根据 JSONRFC 4677 进行转义。

有一个审计事件类型列表为每个条目类型指定字段集和示例。

### 日志文件输出设置

可以使用"elasticsearch.yml"文件中的设置来控制事件和有关记录内容的其他一些信息。请参阅审核事件设置和本地节点信息设置。

请注意，在审核事件中包含请求正文时，可能会以纯文本形式审核**敏感数据，即使所有安全 API(例如更改用户密码的 API)在审核时都过滤掉了凭据。

您还可以配置日志文件在位于"ES_PATH_CONF"中的"log4j2.properties"文件中的写入方式(或查看源代码中 thelog4j2.properties 的相关部分)。默认情况下，审计信息会附加到<clustername>标准 Elasticsearch 'logs' 目录中的 '_audit.json' 文件(通常位于 '$ES_HOME/logs')。该文件也会每天轮换和存档，或者在达到 1GB 文件大小限制时进行存档。

[« Audit events](audit-event-types.md) [Logfile audit events ignore policies
»](audit-log-ignore-policy.md)
