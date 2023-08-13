

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Clear cache API](indices-clearcache.md) [Close index API »](indices-
close.md)

## 克隆索引接口

克隆现有索引。

    
    
    POST /my-index-000001/_clone/cloned-my-index-000001

###Request

'发布 /<index>/_clone/<target-index>'

'把 /<index>/_clone/<target-index>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对要克隆的索引具有"管理"索引权限。  * 要克隆索引，该索引必须标记为只读，并且集群运行状况为"绿色"。

例如，以下请求阻止对"my_source_index"执行写入操作，以便可以克隆它。仍允许进行元数据更改，例如删除索引。

    
    
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
        "index.blocks.write": true
      }
    }

无法克隆数据流上的当前写入索引。为了克隆当前写入索引，必须首先滚动更新数据流，以便创建新的写入索引，然后可以克隆以前的写入索引。

###Description

使用克隆索引 API 将现有索引克隆到新索引中，其中每个原始主分片都会克隆到新索引中的新主分片中。

Elasticsearch 不会将索引模板应用于生成的索引。API 也不会从原始索引复制索引元数据。索引元数据包括别名、ILM 阶段定义和 CCR 追随者信息。例如，如果克隆 CCR 从属索引，则生成的克隆将不是跟随器索引。

克隆 API 会将大多数索引设置从源索引复制到生成的索引，但"index.number_of_replicas"和"index.auto_expand_replicas"除外。要在结果索引中设置副本数，请在克隆请求中配置这些设置。

#### 克隆的工作原理

克隆的工作原理如下：

* 首先，它创建一个与源索引具有相同定义的新目标索引。  * 然后，它将段从源索引硬链接到目标索引。(如果文件系统不支持硬链接，则所有段都将复制到新索引中，这是一个更加耗时的过程。  * 最后，它会恢复目标索引，就好像它是刚刚重新打开的已关闭索引一样。

#### 克隆索引

要将"my_source_index"克隆到名为"my_target_index"的新索引中，请发出以下请求：

    
    
    response = client.indices.clone(
      index: 'my_source_index',
      target: 'my_target_index'
    )
    puts response
    
    
    POST /my_source_index/_clone/my_target_index

一旦目标索引添加到集群状态，上述请求就会立即返回 - 它不会等待克隆操作开始。

只有满足以下要求，才能克隆索引：

* 目标索引不得存在。  * 源索引的主分片数必须与目标索引相同。  * 处理克隆进程的节点必须有足够的可用磁盘空间来容纳现有索引的第二个副本。

"_clone"API 类似于"创建索引"API，并接受目标索引的"设置"和"别名"参数：

    
    
    response = client.indices.clone(
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
    
    
    POST /my_source_index/_clone/my_target_index
    {
      "settings": {
        "index.number_of_shards": 5 __},
      "aliases": {
        "my_search_indices": {}
      }
    }

__

|

目标索引中的分片数。此值必须等于源索引中的分片数。   ---|--- 映射可能未在"_clone"请求中指定。源索引的映射将用于目标索引。

#### 监视克隆过程

克隆过程可以使用"_cat恢复"API 进行监控，或者通过将"wait_for_status"参数设置为"黄色"来等待所有主分片分配完毕。

一旦目标索引添加到集群状态，在分配任何分片之前，"_clone"API 就会返回。此时，所有分片处于"未分配"状态。如果由于任何原因无法分配目标索引，则其主分片将保持"未分配"状态，直到可以在该节点上分配为止。

分配主分片后，它将进入"正在初始化"状态，克隆过程开始。克隆操作完成后，分片将变为"活动"。此时，Elasticsearch 将尝试分配任何副本，并可能决定将主分片重新定位到另一个节点。

#### 等待活动分片

由于克隆操作会创建一个新索引以将分片克隆到，因此创建索引时的等待活动分片设置也适用于克隆索引操作。

### 路径参数

`<index>`

     (Required, string) Name of the source index to clone. 
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

[« Clear cache API](indices-clearcache.md) [Close index API »](indices-
close.md)
