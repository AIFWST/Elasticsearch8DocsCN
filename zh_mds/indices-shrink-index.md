

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Rollover API](indices-rollover-index.md) [Simulate index API »](indices-
simulate-index.md)

## 收缩索引API

将现有索引收缩为主分片较少的新索引。

    
    
    response = client.indices.shrink(
      index: 'my-index-000001',
      target: 'shrunk-my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_shrink/shrunk-my-index-000001

###Request

'发布 /<index>/_shrink/<target-index>'

'把 /<index>/_shrink/<target-index>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有索引的"管理"索引权限。  * 在缩小索引之前：

    * The index must be read-only. 
    * A copy of every shard in the index must reside on the same node. 
    * The index must have a `green` [health status](cluster-health.html "Cluster health API"). 

为了简化分片分配，我们建议您同时删除索引的副本分片。稍后，您可以在收缩操作过程中重新添加副本分片。

您可以使用以下更新索引设置 API 请求删除索引的副本分片，将索引的剩余分片重新定位到同一节点，并将索引设为只读。

    
    
    response = client.indices.put_settings(
      index: 'my_source_index',
      body: {
        settings: {
          "index.number_of_replicas": 0,
          "index.routing.allocation.require._name": 'shrink_node_name',
          "index.blocks.write": true
        }
      }
    )
    puts response
    
    
    PUT /my_source_index/_settings
    {
      "settings": {
        "index.number_of_replicas": 0,                                __"index.routing.allocation.require._name": "shrink_node_name", __"index.blocks.write": true __}
    }

__

|

删除索引的副本分片。   ---|---    __

|

将索引的分片重新定位到"shrink_node_name"节点。请参阅索引级别硬分配筛选。   __

|

防止对此索引执行写入操作。仍允许元数据更改，例如删除索引。   重新定位源索引可能需要一段时间。可以使用"_cat恢复"API 跟踪进度，也可以使用"集群运行状况"API 等待所有分片都使用"wait_for_no_relocating_shards"参数重新定位。

###Description

收缩索引 API 允许您将现有索引收缩为主分片较少的新索引。目标索引中请求的主分片数必须是源索引中分片数的一个因子。例如，具有"8"个主分片的索引可以收缩为"4"、"2"或"1"主分片，或者具有"15"个主分片的索引可以收缩为"5"、"3"或"1"。如果索引中的分片数是质数，则只能将其缩小为单个主分片。在收缩之前，索引中每个分片的(主副本)副本必须存在于同一节点上。

数据流上的当前写入索引无法收缩。为了收缩当前写入索引，必须首先滚动更新数据流，以便创建新的写入索引，然后可以收缩以前的写入索引。

#### 收缩的工作原理

收缩操作：

1. 创建一个与源索引定义相同但主分片数量较少的新目标索引。  2. 将段从源索引硬链接到目标索引。(如果文件系统不支持硬链接，则所有段都将复制到新索引中，这是一个更加耗时的过程。此外，如果使用多个数据路径，则不同数据路径上的分片需要段文件的完整副本(如果它们不在同一磁盘上)，因为硬链接无法跨磁盘工作) 3.恢复目标索引，就好像它是刚刚重新打开的已关闭索引一样。

#### 收缩索引

要将"my_source_index"收缩为名为"my_target_index"的新索引，请发出以下请求：

    
    
    response = client.indices.shrink(
      index: 'my_source_index',
      target: 'my_target_index',
      body: {
        settings: {
          "index.routing.allocation.require._name": nil,
          "index.blocks.write": nil
        }
      }
    )
    puts response
    
    
    POST /my_source_index/_shrink/my_target_index
    {
      "settings": {
        "index.routing.allocation.require._name": null, __"index.blocks.write": null __}
    }

__

|

清除从源索引复制的分配要求。   ---|---    __

|

清除从源索引复制的索引写入块。   一旦目标索引添加到集群状态，上述请求就会立即返回 - 它不会等待收缩操作开始。

指数只有在满足以下要求时才能收缩：

* 目标索引不得存在。  * 源索引的主分片必须多于目标索引。  * 目标索引中的主分片数必须是源索引中主分片数的因子。源索引的主分片必须多于目标索引。  * 索引在所有分片中总共包含的文档不得超过"2，147，483，519"，这些分片将在目标索引上收缩为单个分片，因为这是单个分片可以容纳的最大文档数。  * 处理收缩过程的节点必须有足够的可用磁盘空间来容纳现有索引的第二个副本。

"_shrink"API 类似于"创建索引"API，并接受目标索引的"设置"和"别名"参数：

    
    
    response = client.indices.shrink(
      index: 'my_source_index',
      target: 'my_target_index',
      body: {
        settings: {
          "index.number_of_replicas": 1,
          "index.number_of_shards": 1,
          "index.codec": 'best_compression'
        },
        aliases: {
          my_search_indices: {}
        }
      }
    )
    puts response
    
    
    POST /my_source_index/_shrink/my_target_index
    {
      "settings": {
        "index.number_of_replicas": 1,
        "index.number_of_shards": 1, __"index.codec": "best_compression" __},
      "aliases": {
        "my_search_indices": {}
      }
    }

__

|

目标索引中的分片数。这必须是源索引中分片数的一个因素。   ---|---    __

|

最佳压缩仅在对索引进行新写入时生效，例如将分片强制合并到单个段时。   映射可能未在"_shrink"请求中指定。

#### 监控收缩过程

可以使用"_cat恢复"API 监控收缩过程，或者通过将"wait_for_status"参数设置为"黄色"，可以使用"集群运行状况"API 来等待所有主分片的分配。

一旦目标索引添加到集群状态，在分配任何分片之前，"_shrink"API 就会返回。此时，所有分片处于"未分配"状态。如果由于任何原因无法在收缩节点上分配目标索引，则其主分片将保持"未分配"状态，直到可以在该节点上分配为止。

一旦主分片被分配，它就会进入状态"正在初始化"，收缩过程开始。收缩操作完成后，分片将变为"活动"。此时，Elasticsearch 将尝试分配任何副本，并可能决定将主分片重新定位到另一个节点。

#### 等待活动分片

由于收缩操作会创建一个新索引以将分片收缩到，因此创建索引时的等待活动分片设置也适用于收缩索引操作。

### 路径参数

`<index>`

     (Required, string) Name of the source index to shrink. 
`<target-index>`

    

(必需，字符串)要创建的目标索引的名称。

索引名称必须满足以下条件：

* 仅限小写 * 不能包含 '\'， '/'， '*'， '？''， '<'， '>'， '|'， ' ' (空格字符)， '，'， '#' * 7.0 之前的索引可能包含冒号 ('：')，但该冒号已被弃用，在 7.0+ 中不受支持 * 不能以 '-'、'_'、'+' 开头 * 不能是 '." 或 '..' * 不能超过 255 字节(注意是字节，因此多字节字符将更快地计入 255 限制) * 不推荐使用以 '." 开头的名称，隐藏索引和插件管理的内部索引除外

### 查询参数

`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`aliases`

    

(可选，对象的对象)生成的索引的别名。

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

`settings`

     (Optional, [index setting object](index-modules.html#index-modules-settings "Index Settings")) Configuration options for the target index. See [Index Settings](index-modules.html#index-modules-settings "Index Settings"). 
`max_primary_shard_size`

     (Optional, [byte units](api-conventions.html#byte-units "Byte size units")) The max primary shard size for the target index. Used to find the optimum number of shards for the target index. When this parameter is set, each shard's storage in the target index will not be greater than the parameter. The shards count of the target index will still be a factor of the source index's shards count, but if the parameter is less than the single shard size in the source index, the shards count for the target index will be equal to the source index's shards count. For example, when this parameter is set to 50gb, if the source index has 60 primary shards with totaling 100gb, then the target index will have 2 primary shards, with each shard size of 50gb; if the source index has 60 primary shards with totaling 1000gb, then the target index will have 20 primary shards; if the source index has 60 primary shards with totaling 4000gb, then the target index will still have 60 primary shards. This parameter conflicts with `number_of_shards` in the `settings`, only one of them may be set. 

[« Rollover API](indices-rollover-index.md) [Simulate index API »](indices-
simulate-index.md)
