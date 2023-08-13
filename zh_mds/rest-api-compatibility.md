

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Common options](common-options.md) [Autoscaling APIs »](autoscaling-
apis.md)

## REST API 兼容性

为了帮助 REST 客户端减轻不兼容(中断性)API 更改的影响，Elasticsearch 提供了按请求选择加入的 API 兼容模式。

Elasticsearch REST API 在不同版本中通常是稳定的。但是，某些改进需要与以前版本不兼容的更改。例如，Elasticsearch 7.x 在许多 URL 路径中支持自定义映射类型，但 Elasticsearch 8.0+ 不支持(请参阅 mappingtypes_ _Removal)。在发送到 Elasticsearch 8.0+ 的请求中指定自定义类型会返回错误。但是，如果您请求 REST API 兼容性，Elasticsearch 会接受该请求，即使不再支持映射类型也是如此。

当 API 以删除为目标或将以不兼容的方式进行更改时，一个或多个版本将弃用原始 API。使用原始 API 会在日志中触发弃用警告。这使您能够在升级之前查看弃用日志并采取适当的操作。但是，在某些情况下，很难确定使用已弃用 API 的所有位置。这就是 REST API 兼容性可以提供帮助的地方。

当您请求 REST API 兼容性时，Elasticsearch 会尝试遵循以前的 REST API 版本。Elasticsearch 尝试应用最兼容的 URL、请求正文、响应正文和 HTTP 参数。

对于兼容的 API，这不起作用 - 它只会影响对与以前版本有重大更改的 API 的调用。如果 Elasticsearch 无法自动解决不兼容问题，则在兼容模式下仍会返回错误。

REST API 兼容性不保证与先前版本相同的行为。它指示 Elasticsearch 自动解决任何不兼容问题，以便可以处理请求而不是返回错误。

REST API 兼容性应该是平滑升级过程的桥梁，而不是长期策略。REST API 兼容性仅在一个主要版本中得到支持：支持 8.x 的 7.x 请求/响应。

当您使用 REST API 兼容性提交请求并且 Elasticsearch 解决了不兼容性时，会将一条消息写入弃用日志，类别为"compatible_api"。查看弃用日志以确定使用情况和完全支持的功能中的任何差距。

有关特定中断性更改和请求兼容模式的影响的信息，请参阅迁移指南中的 REST API 更改。

### 请求 REST API 兼容性

REST API 兼容性是通过 Accept 和/或 Content-Type 标头为每个请求实现的。

例如：

    
    
    Accept: "application/vnd.elasticsearch+json;compatible-with=7"
    Content-Type: "application/vnd.elasticsearch+json;compatible-with=7"

始终需要 Accept 标头，并且仅当随请求一起发送正文时才需要 Content-Type 标头。以下值在与 7.x 或 8.x Elasticsearch 服务器通信时有效：

    
    
    "application/vnd.elasticsearch+json;compatible-with=7"
    "application/vnd.elasticsearch+yaml;compatible-with=7"
    "application/vnd.elasticsearch+smile;compatible-with=7"
    "application/vnd.elasticsearch+cbor;compatible-with=7"

官方支持的 Elasticsearchclient 可以为所有请求启用 REST API 兼容性。

要为 Elasticsearch 收到的所有请求启用 REST API 兼容性，请将环境变量"ELASTIC_CLIENT_APIVERSIONING"设置为 true。

### REST API 兼容性工作流

要在从 7.17 升级到 8.9.0 期间利用 REST API 兼容性，请执行以下操作：

1. 将您的 Elasticsearch 客户端升级到最新的 7.x 版本，并启用 REST API 兼容性。  2. 使用升级助手查看所有关键问题并浏览弃用日志。一些关键问题可能会通过 REST API 兼容性得到缓解。  3. 在继续升级之前解决所有关键问题。  4. 将弹性搜索升级到 8.9.0。  5. 查看弃用日志中是否有类别为"compatible_api"的条目。查看与依赖于兼容模式的请求关联的工作流。  6. 将您的 Elasticsearch 客户端升级到 8.x，并在需要时手动解决兼容性问题。

[« Common options](common-options.md) [Autoscaling APIs »](autoscaling-
apis.md)
