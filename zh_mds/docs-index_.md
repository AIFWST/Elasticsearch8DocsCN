

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Reading and Writing documents](docs-replication.md) [Get API »](docs-
get.md)

## 索引接口

请参阅映射types__Removal。

将 JSON 文档添加到指定的数据流或索引，并使其可搜索。如果目标是索引并且文档已存在，则请求将更新文档并递增其版本。

不能使用索引 API 将现有文档的更新请求发送到数据流。请参阅通过查询更新数据流中的文档和更新或删除后备索引中的文档。

###Request

"放 /<target>/_doc/<_id>"

'发布 /<target>/_doc/'

"放 /<target>/_create/<_id>"

'发布 /<target>/_create/<_id>"

您无法使用"PUT//<target>_doc/<_id>"请求格式向数据流添加新文档。要指定文档 ID，请改用"PUT//<target>_create/<_id>"格式。请参阅将文档添加到数据流。

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或索引别名具有以下索引权限：

    * To add or overwrite a document using the `PUT /<target>/_doc/<_id>` request format, you must have the `create`, `index`, or `write` index privilege. 
    * To add a document using the `POST /<target>/_doc/`, `PUT /<target>/_create/<_id>`, or `POST /<target>/_create/<_id>` request formats, you must have the `create_doc`, `create`, `index`, or `write` index privilege. 
    * To automatically create a data stream or index with an index API request, you must have the `auto_configure`, `create_index`, or `manage` index privilege. 

* 自动数据流创建需要启用数据流的匹配索引模板。请参阅_Set数据stream_。

### 路径参数

`<target>`

    

(必需，字符串)目标数据流或索引的名称。

如果目标不存在，并且与具有"data_stream"定义的索引模板的名称或通配符 ("*") 模式匹配，则此请求将创建数据流。请参阅_Set数据stream_。

如果目标不存在且与数据流模板不匹配，则此请求会创建索引。

您可以使用解析索引 API 检查现有目标。

`<_id>`

    

(可选，字符串)文档的唯一标识符。

以下请求格式需要此参数：

* 'PUT //_doc/<_id>' * 'PUT //_create/<_id>' * 'POST //<target><target><target>_create/<_id>'

要自动生成文档 ID，请使用"POST //<target>_doc/"请求格式并省略此参数。

### 查询参数

`if_seq_no`

     (Optional, integer) Only perform the operation if the document has this sequence number. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`if_primary_term`

     (Optional, integer) Only perform the operation if the document has this primary term. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 

`op_type`

    

(可选，枚举)设置为"create"以仅在文档不存在时才为文档编制索引(如果absent_，则_put)。如果具有指定"_id"的文档已存在，则索引操作将失败。与使用"<index>/_create"端点相同。有效值："索引"、"创建"。如果指定了文档 ID，则默认为"索引"。否则，它默认为"创建"。

如果请求以数据流为目标，则需要"创建"的"op_type"。请参阅将文档添加到数据流。

`pipeline`

     (Optional, string) ID of the pipeline to use to preprocess incoming documents. If the index has a default ingest pipeline specified, then setting the value to `_none` disables the default ingest pipeline for this request. If a final pipeline is configured it will always run, regardless of the value of this parameter. 
`refresh`

     (Optional, enum) If `true`, Elasticsearch refreshes the affected shards to make this operation visible to search, if `wait_for` then wait for a refresh to make this operation visible to search, if `false` do nothing with refreshes. Valid values: `true`, `false`, `wait_for`. Default: `false`. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`timeout`

    

(可选，时间单位)周期请求等待以下操作：

* 自动创建索引 * 动态映射更新 * 等待活动分片

默认为"1m"(一分钟)。这保证了 Elasticsearch 在失败之前至少等待超时。实际等待时间可能会更长，尤其是在发生多次等待时。

`version`

     (Optional, integer) Explicit version number for concurrency control. The specified version must match the current version of the document for the request to succeed. 
`version_type`

     (Optional, enum) Specific version type: `external`, `external_gte`. 
`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

`require_alias`

     (Optional, Boolean) If `true`, the destination must be an [index alias](aliases.html "Aliases"). Defaults to `false`. 

### 请求正文

`<field>`

     (Required, string) Request body contains the JSON source for the document data. 

### 响应正文

`_shards`

     Provides information about the replication process of the index operation. 
`_shards.total`

     Indicates how many shard copies (primary and replica shards) the index operation should be executed on. 
`_shards.successful`

    

指示索引操作成功处理的分片副本数。当索引操作成功时，"成功"至少为 1。

当索引操作成功返回时，副本分片可能不会全部启动 - 默认情况下，只需要主分片。设置"wait_for_active_shards"以更改此默认行为。请参阅活动分片。

`_shards.failed`

     An array that contains replication-related errors in the case an index operation failed on a replica shard. 0 indicates there were no failures. 
`_index`

     The name of the index the document was added to. 
`_type`

     The document type. Elasticsearch indices now support a single document type, `_doc`. 
`_id`

     The unique identifier for the added document. 
`_version`

     The document version. Incremented each time the document is updated. 
`_seq_no`

     The sequence number assigned to the document for the indexing operation. Sequence numbers are used to ensure an older version of a document doesn’t overwrite a newer version. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`_primary_term`

     The primary term assigned to the document for the indexing operation. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`result`

     The result of the indexing operation, `created` or `updated`. 

###Description

您可以使用"_doc"或"_create"资源为新的 JSON 文档编制索引。使用"_create"可以保证仅当文档不存在时才对其进行索引。要更新现有文档，您必须使用"_doc"资源。

#### 自动创建数据流和索引

如果请求的目标不存在，并且与具有"data_stream"定义的索引模板匹配，则索引操作会自动创建数据流。请参阅_Set数据stream_。

如果目标不存在且与数据流模板不匹配，则该操作会自动创建索引并应用任何匹配的索引模板。

Elasticsearch 包含多个内置索引模板。若要避免与这些模板发生命名冲突，请参阅避免索引模式冲突。

如果不存在映射，索引操作将创建动态映射。默认情况下，如果需要，新字段和对象会自动添加到映射中。有关字段映射的详细信息，请参阅映射和更新映射 API。

自动索引创建由"action.auto_create_index"设置控制。此设置默认为"true"，这允许自动创建任何索引。您可以修改此设置以显式允许或阻止自动创建与指定模式匹配的索引，或将其设置为"false"以完全禁用自动索引创建。指定要允许的模式的逗号分隔列表，或在每个模式前面加上"+"或"-"，以指示是允许还是阻止。指定列表时，默认行为是不允许。

"action.auto_create_index"设置仅影响索引的自动创建。它不会影响数据流的创建。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "action.auto_create_index": 'my-index-000001,index10,-index1*,+ind*'
        }
      }
    )
    puts response
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "action.auto_create_index": 'false'
        }
      }
    )
    puts response
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "action.auto_create_index": 'true'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "action.auto_create_index": "my-index-000001,index10,-index1*,+ind*" __}
    }
    
    PUT _cluster/settings
    {
      "persistent": {
        "action.auto_create_index": "false" __}
    }
    
    PUT _cluster/settings
    {
      "persistent": {
        "action.auto_create_index": "true" __}
    }

__

|

允许自动创建名为"my-index-000001"或"index10"的索引，阻止创建与模式"index1*"匹配的索引，并允许创建与"ind*"模式匹配的任何其他索引。模式按指定的顺序匹配。   ---|---    __

|

完全禁用自动索引创建。   __

|

允许自动创建任何索引。这是默认值。   ##### 如果缺席编辑，则放置

可以通过使用"_create"资源或将"op_type"参数设置为 _create_ 来强制创建操作。在这种情况下，如果索引中已存在具有指定 ID 的文档，则索引操作将失败。

##### 自动创建文档 ID

使用"POST //<target>_doc/"请求格式时，"op_type"会自动设置为"创建"，索引操作会为文档生成唯一 ID。

    
    
    response = client.index(
      index: 'my-index-000001',
      body: {
        "@timestamp": '2099-11-15T13:12:00',
        message: 'GET /search HTTP/1.1 200 1070000',
        user: {
          id: 'kimchy'
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_doc/
    {
      "@timestamp": "2099-11-15T13:12:00",
      "message": "GET /search HTTP/1.1 200 1070000",
      "user": {
        "id": "kimchy"
      }
    }

API 返回以下结果：

    
    
    {
      "_shards": {
        "total": 2,
        "failed": 0,
        "successful": 2
      },
      "_index": "my-index-000001",
      "_id": "W0tpsmIBdwcYyG50zbta",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "result": "created"
    }

##### 乐观并发控制

索引操作可以设置为有条件的，并且仅在为文档的最后修改分配了由"if_seq_no"和"if_primary_term"参数指定的序列号和主要术语时才执行。如果检测到不匹配，该操作将导致"版本冲突异常"和状态代码 409。有关更多详细信息，请参阅乐观并发控制。

#####Routing

默认情况下，分片放置(或"路由")通过使用文档 id 值的哈希值进行控制。为了进行更明确的控制，可以使用"路由"参数直接在每个操作的基础上指定路由器使用的哈希函数的值。例如：

    
    
    response = client.index(
      index: 'my-index-000001',
      routing: 'kimchy',
      body: {
        "@timestamp": '2099-11-15T13:12:00',
        message: 'GET /search HTTP/1.1 200 1070000',
        user: {
          id: 'kimchy'
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_doc?routing=kimchy
    {
      "@timestamp": "2099-11-15T13:12:00",
      "message": "GET /search HTTP/1.1 200 1070000",
      "user": {
        "id": "kimchy"
      }
    }

在此示例中，文档根据提供的"路由"参数"kimchy"路由到分片。

设置显式映射时，您还可以使用"_routing"字段来定向索引操作，以从文档本身提取路由值。这确实是以额外的文档解析传递的(非常低的)成本为代价的。如果定义"_routing"映射并将其设置为"必需"，则在未提供或提取路由值的情况下，索引操作将失败。

数据流不支持自定义路由，除非它们是在模板中启用"allow_custom_routing"设置的情况下创建的。

#####Distributed

索引操作根据其路由定向到主分片(请参阅上面的路由部分)，并在包含此分片的实际节点上执行。主分片完成操作后，如果需要，更新将分发到适用的副本。

##### 活动分片

为了提高写入系统的复原能力，可以将索引操作配置为等待一定数量的活动分片副本，然后再继续操作。如果所需数量的活动分片副本不可用，则写入操作必须等待并重试，直到必要的分片副本已启动或发生超时。默认情况下，写入操作仅等待主分片处于活动状态后再继续(即"wait_for_active_shards=1")。可以通过设置"index.write.wait_for_active_shards"在索引设置中动态覆盖此默认值。若要更改每个操作的此行为，可以使用"wait_for_active_shards"请求参数。

有效值为"all"或任何正整数，最多为索引中每个分片的配置副本总数(即"number_of_replicas+1")。指定负值或大于分片副本数的数字将引发错误。

例如，假设我们有一个由三个节点组成的集群，"A"、"B"和"C"，我们创建一个索引"索引"，副本数设置为 3(结果有 4 个分片副本，比节点多一个副本)。如果我们尝试索引操作，默认情况下，该操作将仅确保每个分片的主副本在继续之前可用。这意味着，即使"B"和"C"下降，并且"A"托管了主分片副本，索引操作仍将仅使用数据的一个副本进行。如果请求上的"wait_for_active_shards"设置为"3"(并且所有 3 个节点都已启动)，则索引操作将需要 3 个活动分片副本才能继续，这一要求应该满足，因为集群中有 3 个活动节点，每个节点都保存分片的副本。但是，如果我们将"wait_for_active_shards"设置为"all"(或设置为"4"，这是相同的)，索引操作将不会继续，因为我们没有索引中每个分片的所有 4 个副本都处于活动状态。除非在集群中启动一个新节点来托管分片的第四个副本，否则操作将超时。

请务必注意，此设置大大降低了写入操作未写入所需分片副本数的可能性，但并不能完全消除这种可能性，因为此检查发生在写入操作开始之前。写入操作开始后，复制仍有可能在任意数量的分片副本上失败，但在主副本上仍会成功。写入操作响应的"_shards"部分显示复制成功/失败的分片副本数。

    
    
    {
      "_shards": {
        "total": 2,
        "failed": 0,
        "successful": 2
      }
    }

#####Refresh

控制此请求所做的更改何时可供搜索。见提神。

##### Noopupdates

使用索引 API 更新文档时，即使文档未更改，也始终会创建文档的新版本。如果这不可接受，请使用将"detect_noop"设置为 true 的"_update"API。此选项在索引 API 上不可用，因为索引 API 不会提取旧源，也无法将其与新源进行比较。

对于何时不接受noop更新，没有硬性规定。这是许多因素的组合，例如数据源发送更新的频率，以及每秒有多少查询Elasticsearch在接收更新的分片上运行。

#####Timeout

执行索引操作时，分配用于执行索引操作的主分片可能不可用。造成这种情况的一些原因可能是主分片当前正在从网关恢复或正在进行重定位。默认情况下，索引操作将在主分片上等待最多 1 分钟，然后失败并响应错误。"timeout"参数可用于显式指定它等待的时间。下面是将其设置为 5 分钟的示例：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      timeout: '5m',
      body: {
        "@timestamp": '2099-11-15T13:12:00',
        message: 'GET /search HTTP/1.1 200 1070000',
        user: {
          id: 'kimchy'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?timeout=5m
    {
      "@timestamp": "2099-11-15T13:12:00",
      "message": "GET /search HTTP/1.1 200 1070000",
      "user": {
        "id": "kimchy"
      }
    }

#####Versioning

每个索引文档都有一个版本号。默认情况下，使用从 1 开始并随着每次更新递增的内部版本控制，包括删除。(可选)可以将版本号设置为外部值(例如，如果在数据库中维护)。要启用此功能，应将"version_type"设置为"外部"。提供的值必须是枚举，长整型值大于或等于 0，并且小于 9.2e+18 左右。

使用外部版本类型时，系统会检查传递给索引请求的版本号是否大于当前存储的文档的版本号。如果为 true，则将为文档编制索引并使用新版本号。如果提供的值小于或等于存储文档的版本号，则会发生版本冲突，索引操作将失败。例如：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      version: 2,
      version_type: 'external',
      body: {
        user: {
          id: 'elkbee'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?version=2&version_type=external
    {
      "user": {
        "id": "elkbee"
      }
    }

版本控制是完全实时的，不受搜索操作的近实时方面的影响。如果未提供版本，则执行操作时不进行任何版本检查。

在前面的示例中，操作将成功，因为提供的 2 版本高于当前文档版本 1。如果文档已更新，并且其版本设置为 2 或更高版本，则索引命令将失败并导致冲突(409 http 状态代码)。

一个很好的副作用是，只要使用源数据库中的版本号，就不需要维护由于对源数据库的更改而执行的严格顺序异步索引操作。如果使用外部版本控制，甚至使用数据库中的数据更新 Elasticsearch 索引的简单情况也会得到简化，因为如果索引操作由于某种原因顺序不正常，则只会使用最新版本。

##### 版本类型

除了"外部"版本类型之外，Elasticsearch 还支持针对特定用例的其他类型：

"外部"或"external_gt"

     Only index the document if the given version is strictly higher than the version of the stored document **or** if there is no existing document. The given version will be used as the new version and will be stored with the new document. The supplied version must be a non-negative long number. 
`external_gte`

     Only index the document if the given version is **equal** or higher than the version of the stored document. If there is no existing document the operation will succeed as well. The given version will be used as the new version and will be stored with the new document. The supplied version must be a non-negative long number. 

"external_gte"版本类型适用于特殊用例，应谨慎使用。如果使用不当，可能会导致数据丢失。还有另一个选项"force"，它已被弃用，因为它可能导致主分片和副本分片分化。

###Examples

将 JSON 文档插入到"my-index-000001"索引中，"_id"为 1：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        "@timestamp": '2099-11-15T13:12:00',
        message: 'GET /search HTTP/1.1 200 1070000',
        user: {
          id: 'kimchy'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "@timestamp": "2099-11-15T13:12:00",
      "message": "GET /search HTTP/1.1 200 1070000",
      "user": {
        "id": "kimchy"
      }
    }

API 返回以下结果：

    
    
    {
      "_shards": {
        "total": 2,
        "failed": 0,
        "successful": 2
      },
      "_index": "my-index-000001",
      "_id": "1",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "result": "created"
    }

如果不存在具有该 ID 的文档，则使用"_create"资源将文档索引到"my-index-000001"索引中：

    
    
    response = client.create(
      index: 'my-index-000001',
      id: 1,
      body: {
        "@timestamp": '2099-11-15T13:12:00',
        message: 'GET /search HTTP/1.1 200 1070000',
        user: {
          id: 'kimchy'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_create/1
    {
      "@timestamp": "2099-11-15T13:12:00",
      "message": "GET /search HTTP/1.1 200 1070000",
      "user": {
        "id": "kimchy"
      }
    }

将"op_type"参数设置为 _create_，以便在不存在具有该 ID 的文档时将文档索引到"my-index-000001"索引中：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      op_type: 'create',
      body: {
        "@timestamp": '2099-11-15T13:12:00',
        message: 'GET /search HTTP/1.1 200 1070000',
        user: {
          id: 'kimchy'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?op_type=create
    {
      "@timestamp": "2099-11-15T13:12:00",
      "message": "GET /search HTTP/1.1 200 1070000",
      "user": {
        "id": "kimchy"
      }
    }

[« Reading and Writing documents](docs-replication.md) [Get API »](docs-
get.md)
