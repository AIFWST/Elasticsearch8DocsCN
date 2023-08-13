

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Simulate index template API](indices-simulate-template.md) [Unfreeze
index API »](unfreeze-index-api.md)

## 拆分索引接口

将现有索引拆分为具有更多主分片的新索引。

    
    
    response = client.indices.split(
      index: 'my-index-000001',
      target: 'split-my-index-000001',
      body: {
        settings: {
          "index.number_of_shards": 2
        }
      }
    )
    puts response
    
    
    POST /my-index-000001/_split/split-my-index-000001
    {
      "settings": {
        "index.number_of_shards": 2
      }
    }

###Request

'发布 /<index>/_split<target-index>/'

"放 /<index>/_split<target-index>/"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有索引的"管理"索引权限。  * 在拆分索引之前：

    * The index must be read-only. 
    * The [cluster health](cluster-health.html "Cluster health API") status must be green. 

您可以使用以下请求将索引设为只读：

    
    
    response = client.indices.put_settings(
      index: 'my_source_index',
      body: {
        settings: {
          "index.blocks.write": true
        }
      }
    )
    puts response
    
    
    PUT /my_source_index/_settings
    {
      "settings": {
        "index.blocks.write": true __}
    }

__

|

防止对此索引执行写入操作，同时仍允许元数据更改(如删除索引)。   ---|--- 数据流上的当前写入索引无法拆分。为了拆分当前写入索引，必须首先滚动更新数据流，以便创建新的写入索引，然后可以拆分以前的写入索引。

###Description

拆分索引 API 允许您将现有索引拆分为新索引，其中每个原始主分片在新索引中拆分为两个或多个主分片。

索引可以拆分的次数(以及每个原始分片可以拆分为的分片数)由"index.number_of_routing_shards"设置决定。路由分片的数量指定内部用于在具有一致哈希的分片之间分发文档的哈希空间。例如，将"number_of_routing_shards"设置为"30"("5 x 2 x 3")的 5 分片索引可以按因子"2"或"3"进行拆分。换句话说，它可以拆分如下：

* "5" -> "10" -> "30"(除以 2，然后除以 3) * "5" -> "15" -> "30"(除以 3，然后除以 2) * "5" -> "30"(除以 6)

"index.number_of_routing_shards"是静态索引设置。只能在创建索引时或在闭合索引上设置"index.number_of_routing_shards"。

**索引创建示例**

以下创建索引 API 创建"my-index-000001"索引，index.number_of_routing_shards"设置为"30"。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          index: {
            number_of_routing_shards: 30
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "index": {
          "number_of_routing_shards": 30
        }
      }
    }

"index.number_of_routing_shards"设置的默认值取决于原始索引中的主分片数量。默认值旨在允许您按 2 倍拆分，最多 1024 个分片。但是，必须考虑原始主分片的数量。例如，由 5 个主分片创建的索引可以拆分为 10、20、40、80，160、320 或最多 640 个分片(具有单个拆分操作或多个拆分操作)。

如果原始索引包含一个主分片(或者多分片索引已缩小为单个主分片)，则索引可能会拆分为任意数量的分片大于 1。然后，默认数量的路由分片的属性将应用于新拆分的索引。

#### 拆分的工作原理

拆分操作：

1. 创建一个与源索引定义相同但主分片数量更多的新目标索引。  2. 将段从源索引硬链接到目标索引。(如果文件系统不支持硬链接，则所有段都将复制到新索引中，这是一个更加耗时的过程。  3. 创建低级文件后，再次对所有文档进行哈希处理，以删除属于不同分片的文档。  4. 恢复目标索引，就好像它是刚刚重新打开的已关闭索引一样。

#### 为什么 Elasticsearch 不支持增量重新分片？

从"N"个分片到"N+1"个分片，也就是。增量重新分片确实是许多键值存储支持的功能。添加新分片并将新数据推送到这个新分片不是一种选择：这可能会成为索引瓶颈，并且根据其"_id"来确定文档属于哪个分片，这是获取、删除和更新请求所必需的，将变得非常复杂。这意味着我们需要使用不同的哈希方案重新平衡现有数据。

键值存储高效执行此操作的最常见方法是使用一致性哈希。一致哈希只需要在将分片数量从"N"增加到"N+1"时重新定位"1/N"的键。然而，Elasticsearch的存储单位分片是Lucene索引。由于面向搜索的数据结构，占用Luceneindex的很大一部分，无论是仅5%的文档，删除它们并在另一个分片上索引它们通常比键值存储的成本要高得多。如上一节所述，当通过乘法因子增加分片数量时，此成本是合理的：这允许 Elasticsearch 在本地执行拆分，这反过来又允许在索引级别执行拆分，而不是重新索引需要移动的文档，以及使用硬链接进行高效的文件复制。

对于仅追加数据，可以通过创建新索引并向其中推送新数据，同时添加涵盖旧索引和新索引的别名以进行读取操作，从而获得更大的灵活性。假设新旧索引分别具有"M"和"N"分片，与搜索具有"M+N"分片的索引相比，这没有开销。

#### 拆分索引

要将"my_source_index"拆分为名为"my_target_index"的新索引，请发出以下请求：

    
    
    response = client.indices.split(
      index: 'my_source_index',
      target: 'my_target_index',
      body: {
        settings: {
          "index.number_of_shards": 2
        }
      }
    )
    puts response
    
    
    POST /my_source_index/_split/my_target_index
    {
      "settings": {
        "index.number_of_shards": 2
      }
    }

一旦目标索引添加到集群状态，上述请求就会立即返回 - 它不会等待拆分操作开始。

仅当索引满足以下要求时，才能拆分索引：

* 目标索引不得存在 * 源索引的主分片必须少于目标索引。  * 目标索引中的主分片数必须是源索引中主分片数的倍数。  * 处理拆分过程的节点必须有足够的可用磁盘空间来容纳现有索引的第二个副本。

"_split"API 类似于"创建索引"API，并接受目标索引的"设置"和"别名"参数：

    
    
    response = client.indices.split(
      index: 'my_source_index',
      target: 'my_target_index',
      body: {
        settings: {
          "index.number_of_shards": 5
        },
        aliases: {
          my_search_indices: {}
        }
      }
    )
    puts response
    
    
    POST /my_source_index/_split/my_target_index
    {
      "settings": {
        "index.number_of_shards": 5 __},
      "aliases": {
        "my_search_indices": {}
      }
    }

__

|

目标索引中的分片数。这必须是源索引中分片数的倍数。   ---|--- 映射可能未在"_split"请求中指定。

#### 监视拆分过程

可以使用"_cat恢复"API 监控拆分过程，或者通过将"wait_for_status"参数设置为"黄色"，可以使用"集群运行状况"API 来等待所有主分片的分配。

一旦目标索引添加到集群状态，在分配任何分片之前，"_split"API 就会返回。此时，所有分片处于"未分配"状态。如果由于任何原因无法分配目标索引，则其主分片将保持"未分配"状态，直到可以在该节点上分配为止。

分配主分片后，它将进入状态"正在初始化"，拆分过程开始。拆分操作完成后，分片将变为"活动"。此时，Elasticsearch 将尝试分配任何副本，并可能决定将主分片重新定位到另一个节点。

#### 等待活动分片

由于拆分操作会创建一个新索引以将分片拆分到，因此创建索引时的等待活动分片设置也适用于拆分索引操作。

### 路径参数

`<index>`

     (Required, string) Name of the source index to split. 
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

[« Simulate index template API](indices-simulate-template.md) [Unfreeze
index API »](unfreeze-index-api.md)
