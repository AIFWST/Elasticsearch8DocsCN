

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Enrich your data](ingest-enriching-data.md)

[« Enrich your data](ingest-enriching-data.md) [Example: Enrich your data
based on geolocation »](geo-match-enrich-policy-type.md)

## 设置扩充处理器

若要设置扩充处理器，请执行以下步骤：

1. 检查先决条件。  2. 添加丰富数据。  3. 创建扩充策略。  4. 执行扩充策略。  5. 将扩充处理器添加到引入管道。  6. 摄取和丰富文档。

设置扩充处理器后，可以更新扩充数据并更新扩充策略。

扩充处理器执行多个操作，可能会影响引入管道的速度。

我们强烈建议在将扩充处理器部署到生产环境之前对其进行测试和基准测试。

我们不建议使用扩充处理器来追加实时数据。扩充处理器最适合不经常更改的参考数据。

####Prerequisites

如果您使用 Elasticsearch 安全功能，则必须具备：

* 使用的任何索引的"读取"索引权限 * "enrich_user"内置角色

### 添加丰富数据

首先，将文档添加到一个或多个源索引。这些文档应包含最终要添加到传入文档的扩充数据。

您可以使用文档和索引 API 像管理常规 Elasticsearch 索引一样管理源索引。

您还可以设置 Beats(如 Filebeat)以自动将文档发送和索引到源索引。请参阅开始使用 Beats。

### 创建扩充策略

将扩充数据添加到源索引后，使用创建扩充策略 API 创建扩充策略。

创建后，无法更新或更改扩充策略。请参阅更新扩充策略。

### 执行扩充策略

创建扩充策略后，可以使用执行扩充策略 API 执行它以创建扩充索引。

！丰富策略索引

_enrich index_包含来自策略源索引的文档。扩充索引始终以".enrich-*"开头，是只读的，并且是强制合并的。

扩充索引应仅由扩充处理器使用。避免将扩充索引用于其他目的。

### 将扩充处理器添加到引入管道

拥有源索引、扩充策略和相关扩充索引后，可以设置包含策略扩充处理器的引入管道。

！丰富处理器

定义扩充处理器，并使用创建或更新管道 API 将其添加到引入管道。

定义扩充处理器时，必须至少包括以下内容：

* 要使用的扩充策略。  * 用于将传入文档与扩充索引中的文档进行匹配的字段。  * 要添加到传入文档的目标字段。此目标字段包含在丰富策略中指定的匹配和丰富字段。

您还可以使用"max_matches"选项来设置传入文档可以匹配的扩充文档数。如果设置为默认值"1"，则数据将作为 JSON 对象添加到传入文档的目标字段中。否则，数据将作为数组添加。

有关配置选项的完整列表，请参阅扩充。

您还可以将其他处理器添加到采集管道。

### 引入和扩充文档

现在，您可以使用采集管道来丰富文档并为其编制索引。

！丰富过程

在生产中实现管道之前，我们建议先索引一些测试文档，并使用 get API 验证是否正确添加了扩充数据。

### 更新扩充索引

创建后，无法将文档更新或索引到扩充索引。相反，请更新源索引并再次执行扩充策略。这会从更新的源索引创建新的扩充索引。以前的扩充索引将因维护作业延迟而被删除。默认情况下，每 15 分钟完成一次。

如果需要，您可以使用收录管道重新索引或更新任何已收录的文档。

### 更新扩充策略

创建后，无法更新或更改扩充策略。相反，您可以：

1. 创建并执行新的扩充策略。  2. 在任何正在使用的扩充处理器中，将以前的扩充策略替换为新的扩充策略。  3. 使用删除扩充策略 API 删除以前的扩充策略。

### 扩充组件

扩充协调器是一个组件，用于管理和执行在每个采集节点上扩充文档所需的搜索。它将来自所有管道中所有扩充处理器的搜索合并到批量多重搜索中。

扩充策略执行器是管理所有扩充策略执行的组件。执行扩充策略时，此组件会创建新的扩充索引并删除以前的扩充索引。扩充策略执行从选定的主节点进行管理。这些策略的执行发生在不同的节点上。

### 节点设置

"扩充"处理器具有用于扩充协调器和扩充策略执行器的节点设置。

扩充协调器支持以下节点设置：

`enrich.cache_size`

     Maximum number of searches to cache for enriching documents. Defaults to `1000`. There is a single cache for all enrich processors in the cluster. This setting determines the size of that cache. 
`enrich.coordinator_proxy.max_concurrent_requests`

     Maximum number of concurrent [multi-search requests](search-multi-search.html "Multi search API") to run when enriching documents. Defaults to `8`. 
`enrich.coordinator_proxy.max_lookups_per_request`

     Maximum number of searches to include in a [multi-search request](search-multi-search.html "Multi search API") when enriching documents. Defaults to `128`. 

扩充策略执行器支持以下节点设置：

`enrich.fetch_size`

     Maximum batch size when reindexing a source index into an enrich index. Defaults to `10000`. 
`enrich.max_force_merge_attempts`

     Maximum number of [force merge](indices-forcemerge.html "Force merge API") attempts allowed on an enrich index. Defaults to `3`. 
`enrich.cleanup_period`

     How often Elasticsearch checks whether unused enrich indices can be deleted. Defaults to `15m`. 
`enrich.max_concurrent_policy_executions`

     Maximum number of enrich policies to execute concurrently. Defaults to `50`. 

[« Enrich your data](ingest-enriching-data.md) [Example: Enrich your data
based on geolocation »](geo-match-enrich-policy-type.md)
