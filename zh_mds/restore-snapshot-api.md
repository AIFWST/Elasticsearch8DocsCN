

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Get snapshot status API](get-snapshot-status-api.md) [Delete snapshot API
»](delete-snapshot-api.md)

## 恢复快照接口

还原集群或指定数据流和索引的快照。

    
    
    response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'my_snapshot'
    )
    puts response
    
    
    POST /_snapshot/my_repository/my_snapshot/_restore

###Request

"发布/_snapshot/<repository>/<snapshot>/_restore"

###Prerequisites

* 如果您使用 Elasticsearch 安全功能，则必须具有"管理"或"cluster：admin/snapshot/*"集群权限才能使用此 API。

* 您只能将快照还原到具有选定主节点的正在运行的集群。快照的存储库必须已注册并可供群集使用。  * 快照和集群版本必须兼容。请参阅快照兼容性。  * 要还原快照，集群的全局元数据必须是可写的。确保没有任何阻止写入的群集块。还原操作将忽略索引块。  * 在恢复数据流之前，请确保集群包含启用了数据流的匹配索引模板。要进行检查，请使用 Kibana 的 **索引管理** 功能或获取索引模板 API： 响应 = client.indices.get_index_template( 名称： '*'， filter_path： 'index_templates.name，index_templates.index_template.index_patterns，index_templates.index_template.data_stream' ) 将响应 GET _index_template/*？filter_path=index_templates.name，index_templates.index_template.index_patterns，index_templates.index_template.data_stream

如果不存在此类模板，则可以创建一个模板或还原包含该模板的群集状态。如果没有匹配的索引模板，则 adata 流无法滚动更新或创建后备索引。

* 如果您的快照包含来自 App Search 或 Workplace 搜索的数据，请确保在还原快照之前已还原企业级搜索加密密钥。

### 路径参数

`<repository>`

     (Required, string) Name of the repository to restore a snapshot from. 
`<snapshot>`

     (Required, string) Name of the snapshot to restore. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`wait_for_completion`

    

(可选，布尔值)如果为"true"，则请求在还原操作完成时返回响应。当它完成所有尝试恢复已还原索引的主分片时，该操作即告完成。即使一个或多个恢复尝试失败，这也适用。

如果为"false"，则请求在还原操作初始化时返回响应。默认为"假"。

### 请求正文

`ignore_unavailable`

     (Optional, Boolean) If `true`, the request ignores any index or data stream in `indices` that's missing from the snapshot. If `false`, the request returns an error for any missing index or data stream. Defaults to `false`. 
`ignore_index_settings`

    

(可选，字符串或字符串数组)不从快照还原的索引设置。不能使用此选项忽略"index.number_of_shards"。

对于数据流，此选项仅适用于还原的支持索引。新后备索引是使用数据流的匹配索引模板配置的。

`include_aliases`

     (Optional, Boolean) If `true`, the request restores aliases for any restored data streams and indices. If `false`, the request doesn't restore aliases. Defaults to `true`. 

`include_global_state`

    

(可选，布尔值)如果为"true"，则还原群集状态。默认为"假"。

群集状态包括：

* 持久群集设置 * 索引模板 * 旧索引模板 * 引入管道 * ILM 策略 * 对于 7.12.0 之后拍摄的快照，功能状态

如果"include_global_state"为"true"，则还原操作会将集群中的旧索引模板与快照中包含的模板合并，替换名称与快照中名称匹配的任何现有模板。它会完全删除集群中存在的所有持久设置、非旧版索引模板、摄取管道和 ILM 生命周期策略，并将其替换为快照中的相应项目。

使用"feature_states"参数配置要素状态的恢复方式。

如果"include_global_state"为"true"，并且创建的快照没有全局状态，则还原请求将失败。

`feature_states`

    

(可选，字符串数组)要还原的功能状态。

如果"include_global_state"为"true"，则默认情况下，请求将还原快照中的所有功能状态。如果"include_global_state"为"false"，则默认情况下，请求不会恢复任何功能状态。请注意，指定空数组将导致默认行为。要恢复任何功能状态，无论"include_global_state"值如何，请指定仅包含值"none"("["none"]")的数组。

`index_settings`

    

(可选，对象)用于添加或更改还原索引(包括后备索引)的索引设置。不能使用此选项更改"index.number_of_shards"。

对于数据流，此选项仅适用于还原的支持索引。新后备索引是使用数据流的匹配索引模板配置的。

`indices`

    

(可选，字符串或字符串数组)要还原的索引和数据流的逗号分隔列表。支持多目标语法。默认为快照中的所有常规索引和常规数据流。

不能使用此参数还原系统索引或系统数据流。请改用"feature_states"。

`partial`

    

(可选，布尔值)如果为"false"，则当快照中包含的一个或多个索引没有所有可用的主分片时，整个还原操作将失败。默认为"假"。

如果为"true"，则允许恢复具有不可用分片的索引的部分快照。只有成功包含在快照中的分片才会被还原。所有缺失的分片都将重新创建为空。

`rename_pattern`

    

(可选，字符串)定义要应用于还原的数据流和索引的重命名模式。与重命名模式匹配的数据流和索引将根据"rename_replacement"重命名。

重命名模式根据"appendReplacement"逻辑应用，该正则表达式支持引用原始文本。

`rename_replacement`

     (Optional, string) Defines the rename replacement string. See [`rename_pattern`](restore-snapshot-api.html#restore-snapshot-api-rename-pattern) for more information. 

###Examples

以下请求从"snapshot_2"恢复"index_1"和"index_2"。"rename_pattern"和"rename_replacement"参数表示与正则表达式"index_(.+)"匹配的任何索引将在恢复时使用模式"restored_index_$1"重命名。

例如，"index_1"将重命名为"restored_index_1"。"index_2"将重命名为"restored_index_2"。

    
    
    response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'snapshot_2',
      wait_for_completion: true,
      body: {
        indices: 'index_1,index_2',
        ignore_unavailable: true,
        include_global_state: false,
        rename_pattern: 'index_(.+)',
        rename_replacement: 'restored_index_$1',
        include_aliases: false
      }
    )
    puts response
    
    
    POST /_snapshot/my_repository/snapshot_2/_restore?wait_for_completion=true
    {
      "indices": "index_1,index_2",
      "ignore_unavailable": true,
      "include_global_state": false,
      "rename_pattern": "index_(.+)",
      "rename_replacement": "restored_index_$1",
      "include_aliases": false
    }

如果请求成功，API 将返回确认。如果请求遇到错误，响应会指示发现的任何问题，例如阻止还原操作完成的 openindex。

[« Get snapshot status API](get-snapshot-status-api.md) [Delete snapshot API
»](delete-snapshot-api.md)
