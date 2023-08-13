

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Resolve index API](indices-resolve-index-api.md) [Shrink index API
»](indices-shrink-index.md)

## 滚动更新接口

为数据流或索引别名创建新索引。

    
    
    response = client.indices.rollover(
      alias: 'my-data-stream'
    )
    puts response
    
    
    POST my-data-stream/_rollover

###Request

'发布 /<rollover-target>/_rollover/'

'发布 /<rollover-target>/_rollover<target-index>/'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须具有滚动更新目标的"管理"索引权限。

###Description

我们建议使用 ILM 的"滚动更新"操作来自动执行滚动更新。请参阅索引生命周期。

滚动更新 API 为数据流或索引别名创建新索引。API 的行为取决于滚动更新目标。

**滚动数据流**

如果滚动更新数据流，API 会为流创建新的写入索引。流以前的写入索引将成为常规支持索引。滚动更新还会增加数据流的生成。请参阅翻转。

**使用写入索引滚动更新索引别名**

在 Elasticsearch 7.9 之前，您通常使用带有 writeindex 的索引别名来管理时间序列数据。数据流取代了此功能，需要较少的维护，并自动与数据层集成。

请参阅将索引别名转换为数据流。

如果索引别名指向多个索引，则其中一个索引必须是写索引。滚动更新 API 为别名创建一个新的写入索引，并将"is_write_index"设置为"true"。API 还将上一个写入索引的"is_write_index"设置为"false"。

**使用一个索引滚动更新索引别名**

如果滚动更新仅指向一个索引的索引别名，API 将为该别名创建一个新索引，并从别名中删除原始索引。

#### 递增别名的索引名称

滚动更新索引别名时，可以为新索引指定名称。如果未指定名称，并且当前索引以"-"和数字结尾，例如"my-index-000001"或"my-index-3"，则新索引名称将递增该数字。例如，如果滚动更新当前索引为"my-index-000001"的别名，则滚动更新将创建一个名为"my-index-000002"的新索引。此数字始终为 6 个字符且以零填充，与前一个索引的名称无关。

**将日期数学与索引别名滚动更新一起使用**

如果对时序数据使用索引别名，则可以在索引名称中使用日期数学来跟踪翻转日期。例如，您可以创建一个别名，该别名指向名为"<my-index-{now/d}-000001>"的索引。如果在 2099 年 5 月 6 日创建索引，则索引的名称为"my-index-2099.05.06-000001"。如果在 2099 年 5 月 7 日滚动别名，则新索引的名称为"my-index-2099.05.07-000002"。有关示例，请参阅使用写入索引滚动更新索引别名。

#### 等待活动分片

滚动更新会创建一个新索引，并受"wait_for_active_shards"设置的约束。

### 路径参数

`<rollover-target>`

     (Required, string) Name of the data stream or index alias to roll over. 
`<target-index>`

    

(可选，字符串)要创建的索引的名称。支持日期数学。数据流不支持此参数。

如果别名的当前写入索引的名称不以"-"和数字结尾，例如"my-index-000001"或"my-index-3"，则此参数是必需的。

索引名称必须满足以下条件：

* 仅限小写 * 不能包含 '\'， '/'， '*'， '？''， '<'， '>'， '|'， ' ' (空格字符)， '，'， '#' * 7.0 之前的索引可能包含冒号 ('：')，但该冒号已被弃用，在 7.0+ 中不受支持 * 不能以 '-'、'_'、'+' 开头 * 不能是 '." 或 '..' * 不能超过 255 字节(注意是字节，因此多字节字符将更快地计入 255 限制) * 不推荐使用以 '." 开头的名称，隐藏索引和插件管理的内部索引除外

### 查询参数

`dry_run`

     (Optional, Boolean) If `true`, checks whether the current index satisfies the specified `conditions` but does not perform a rollover. Defaults to `false`. 
`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`aliases`

    

(可选，对象的对象)目标索引的别名。数据流不支持此参数。

"别名"对象的属性

`<alias>`

    

(必填，对象)键是别名。索引别名支持日期数学。

对象正文包含别名的选项。支持空对象。

""的属性<alias>

`filter`

     (Optional, [Query DSL object](query-dsl.html "Query DSL")) Query used to limit documents the alias can access. 
`index_routing`

     (Optional, string) Value used to route indexing operations to a specific shard. If specified, this overwrites the `routing` value for indexing operations. 
`is_hidden`

     (Optional, Boolean) If `true`, the alias is [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices"). Defaults to `false`. All indices for the alias must have the same `is_hidden` value. 
`is_write_index`

     (Optional, Boolean) If `true`, the index is the [write index](aliases.html#write-index "Write index") for the alias. Defaults to `false`. 
`routing`

     (Optional, string) Value used to route indexing and search operations to a specific shard. 
`search_routing`

     (Optional, string) Value used to route search operations to a specific shard. If specified, this overwrites the `routing` value for search operations. 

`conditions`

    

(可选，对象)展期条件。如果指定，Elasticsearch 仅在当前索引满足这些条件时才执行滚动更新。如果未指定此参数，Elasticsearch 将无条件执行滚动更新。

如果指定了条件，则其中至少有一个必须是 max_* 条件。如果满足任何max_*条件并且满足所有min_*条件，则指数将展期。

若要触发滚动更新，当前索引必须在请求时满足这些条件。Elasticsearch 不会在 API 响应后监控索引。要自动滚动更新，请改用 ILM 的"滚动更新"。

"条件"的属性

`max_age`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Triggers rollover after the maximum elapsed time from index creation is reached. The elapsed time is always calculated since the index creation time, even if the index origination date is configured to a custom date, such as when using the [index.lifecycle.parse_origination_date](ilm-settings.html#index-lifecycle-parse-origination-date) or [index.lifecycle.origination_date](ilm-settings.html#index-lifecycle-origination-date) settings. 
`max_docs`

     (Optional, integer) Triggers rollover after the specified maximum number of documents is reached. Documents added since the last refresh are not included in the document count. The document count does **not** include documents in replica shards. 
`max_size`

    

(可选，字节单位)当索引达到特定大小时触发滚动更新。这是索引中所有主分片的总大小。副本不计入最大索引大小。

若要查看当前索引大小，请使用_cat索引 API。"pri.store.size"值显示所有主分片的组合大小。

`max_primary_shard_size`

    

(可选，字节单位)当索引中最大的主分片达到特定大小时触发滚动更新。这是索引中主分片的最大大小。与"max_size"一样，副本将被忽略。

要查看当前分片大小，请使用_cat分片 API。"store"值显示每个分片的大小，"prirep"表示分片是主分片("p")还是副本("r")。

`max_primary_shard_docs`

    

(可选，整数)当索引中最大的主分片达到一定数量的文档时触发滚动更新。这是索引中主分片的最大文档数。与"max_docs"一样，副本将被忽略。

要查看当前的分片文档，请使用_cat分片 API。"docs"值显示每个分片的文档数量。

`min_age`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Prevents rollover until after the minimum elapsed time from index creation is reached. See notes on `max_age`. 
`min_docs`

     (Optional, integer) Prevents rollover until after the specified minimum number of documents is reached. See notes on `max_docs`. 
`min_size`

     (Optional, [byte units](api-conventions.html#byte-units "Byte size units")) Prevents rollover until the index reaches a certain size. See notes on `max_size`. 
`min_primary_shard_size`

     (Optional, [byte units](api-conventions.html#byte-units "Byte size units")) Prevents rollover until the largest primary shard in the index reaches a certain size. See notes on `max_primary_shard_size`. 
`min_primary_shard_docs`

     (Optional, integer) Prevents rollover until the largest primary shard in the index reaches a certain number of documents. See notes on `max_primary_shard_docs`. 

`mappings`

    

(可选，映射对象)索引中字段的映射。如果指定，此映射可以包括：

* 字段名称 * 字段数据类型 * 映射参数

请参阅映射。

数据流不支持此参数。

`settings`

    

(可选，索引设置对象)索引的配置选项。请参阅索引设置。

数据流不支持此参数。

### 响应正文

`acknowledged`

     (Boolean) If `true`, the request received a response from the master node within the `timeout` period. 
`shards_acknowledged`

     (Boolean) If `true`, the request received a response from [active shards](docs-index_.html#index-wait-for-active-shards "Active shards") within the `master_timeout` period. 
`old_index`

     (string) Previous index for the data stream or index alias. For data streams and index aliases with a write index, this is the previous write index. 
`new_index`

     (string) Index created by the rollover. For data streams and index aliases with a write index, this is the current write index. 
`rolled_over`

     (Boolean) If `true`, the data stream or index alias rolled over. 
`dry_run`

     (Boolean) If `true`, Elasticsearch did not perform the rollover. 
`condition`

    

(对象)请求的"条件"中指定的每个条件的结果。如果未指定任何条件，则这是一个空对象。

"条件"的属性

`<condition>`

     (Boolean) The key is each condition. The value is its result. If `true`, the index met the condition. 

###Examples

#### 滚动数据流

以下请求无条件滚动访问数据流。

    
    
    response = client.indices.rollover(
      alias: 'my-data-stream'
    )
    puts response
    
    
    POST my-data-stream/_rollover

仅当当前 writeindex 满足以下一个或多个条件时，以下请求才会滚动流：

* 索引是在 7 天或更长时间前创建的。  * 索引包含 1，000 个或更多文档。  * 索引的最大主分片为 50GB 或更大。

    
    
    response = client.indices.rollover(
      alias: 'my-data-stream',
      body: {
        conditions: {
          max_age: '7d',
          max_docs: 1000,
          max_primary_shard_size: '50gb',
          max_primary_shard_docs: '2000'
        }
      }
    )
    puts response
    
    
    POST my-data-stream/_rollover
    {
      "conditions": {
        "max_age": "7d",
        "max_docs": 1000,
        "max_primary_shard_size": "50gb",
        "max_primary_shard_docs": "2000"
      }
    }

该 API 返回：

    
    
    {
      "acknowledged": true,
      "shards_acknowledged": true,
      "old_index": ".ds-my-data-stream-2099.05.06-000001",
      "new_index": ".ds-my-data-stream-2099.05.07-000002",
      "rolled_over": true,
      "dry_run": false,
      "conditions": {
        "[max_age: 7d]": false,
        "[max_docs: 1000]": true,
        "[max_primary_shard_size: 50gb]": false,
        "[max_primary_shard_docs: 2000]": false
      }
    }

#### 使用写索引滚动更新索引别名

以下请求创建"<my-index-{now/d}-000001>"并将其设置为"my-alias"的写入索引。

    
    
    response = client.indices.create(
      index: '<my-index-{now/d}-000001>',
      body: {
        aliases: {
          "my-alias": {
            is_write_index: true
          }
        }
      }
    )
    puts response
    
    
    # PUT <my-index-{now/d}-000001>
    PUT %3Cmy-index-%7Bnow%2Fd%7D-000001%3E
    {
      "aliases": {
        "my-alias": {
          "is_write_index": true
        }
      }
    }

仅当当前写入索引满足以下一个或多个条件时，以下请求才会滚动更新别名：

* 索引是在 7 天或更长时间前创建的。  * 索引包含 1，000 个或更多文档。  * 索引的最大主分片为 50GB 或更大。

    
    
    response = client.indices.rollover(
      alias: 'my-alias',
      body: {
        conditions: {
          max_age: '7d',
          max_docs: 1000,
          max_primary_shard_size: '50gb',
          max_primary_shard_docs: '2000'
        }
      }
    )
    puts response
    
    
    POST my-alias/_rollover
    {
      "conditions": {
        "max_age": "7d",
        "max_docs": 1000,
        "max_primary_shard_size": "50gb",
        "max_primary_shard_docs": "2000"
      }
    }

该 API 返回：

    
    
    {
      "acknowledged": true,
      "shards_acknowledged": true,
      "old_index": "my-index-2099.05.06-000001",
      "new_index": "my-index-2099.05.07-000002",
      "rolled_over": true,
      "dry_run": false,
      "conditions": {
        "[max_age: 7d]": false,
        "[max_docs: 1000]": true,
        "[max_primary_shard_size: 50gb]": false,
        "[max_primary_shard_docs: 2000]": false
      }
    }

如果别名的索引名称使用日期数学，并且您定期滚动更新索引，则可以使用日期数学来缩小搜索范围。例如，以下搜索以过去三天创建的索引为目标。

    
    
    response = client.search(
      index: '<my-index-{now/d}-*>,<my-index-{now/d-1d}-*>,<my-index-{now/d-2d}-*>'
    )
    puts response
    
    
    # GET /<my-index-{now/d}-*>,<my-index-{now/d-1d}-*>,<my-index-{now/d-2d}-*>/_search
    GET /%3Cmy-index-%7Bnow%2Fd%7D-*%3E%2C%3Cmy-index-%7Bnow%2Fd-1d%7D-*%3E%2C%3Cmy-index-%7Bnow%2Fd-2d%7D-*%3E/_search

#### 使用 oneindex 滚动更新索引别名

以下请求创建"<my-index-{now/d}-000001>"及其别名"my-write-alias"。

    
    
    response = client.indices.create(
      index: '<my-index-{now/d}-000001>',
      body: {
        aliases: {
          "my-write-alias": {}
        }
      }
    )
    puts response
    
    
    # PUT <my-index-{now/d}-000001>
    PUT %3Cmy-index-%7Bnow%2Fd%7D-000001%3E
    {
      "aliases": {
        "my-write-alias": { }
      }
    }

仅当当前索引满足以下一个或多个条件时，以下请求才会滚动更新别名：

* 索引是在 7 天或更长时间前创建的。  * 索引包含 1，000 个或更多文档。  * 索引的最大主分片为 50GB 或更大。

    
    
    response = client.indices.rollover(
      alias: 'my-write-alias',
      body: {
        conditions: {
          max_age: '7d',
          max_docs: 1000,
          max_primary_shard_size: '50gb',
          max_primary_shard_docs: '2000'
        }
      }
    )
    puts response
    
    
    POST my-write-alias/_rollover
    {
      "conditions": {
        "max_age": "7d",
        "max_docs": 1000,
        "max_primary_shard_size": "50gb",
        "max_primary_shard_docs": "2000"
      }
    }

该 API 返回：

    
    
    {
      "acknowledged": true,
      "shards_acknowledged": true,
      "old_index": "my-index-2099.05.06-000001",
      "new_index": "my-index-2099.05.07-000002",
      "rolled_over": true,
      "dry_run": false,
      "conditions": {
        "[max_age: 7d]": false,
        "[max_docs: 1000]": true,
        "[max_primary_shard_size: 50gb]": false,
        "[max_primary_shard_docs: 2000]": false
      }
    }

#### 在翻转期间指定设置

通常，使用索引模板自动配置在滚动更新期间创建的索引。如果滚动更新索引别名，则可以使用滚动更新 API 在模板中添加其他索引设置或覆盖设置。数据流不支持"设置"参数。

    
    
    response = client.indices.rollover(
      alias: 'my-alias',
      body: {
        settings: {
          "index.number_of_shards": 2
        }
      }
    )
    puts response
    
    
    POST my-alias/_rollover
    {
      "settings": {
        "index.number_of_shards": 2
      }
    }

[« Resolve index API](indices-resolve-index-api.md) [Shrink index API
»](indices-shrink-index.md)
