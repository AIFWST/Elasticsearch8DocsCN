

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Index lifecycle management settings in Elasticsearch](ilm-settings.md)
[Index recovery settings »](recovery.md)

## 索引管理设置

可以使用以下群集设置来启用或禁用索引管理功能。

"action.auto_create_index"！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) [Automatically create an index](docs-index_.html#index-creation "Automatically create data streams and indices") if it doesn't already exist and apply any configured index templates. Defaults to `true`. 

"action.destructive_requires_name"！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) When set to `true`, you must specify the index name to [delete an index](indices-delete-index.html "Delete index API"). It is not possible to delete all indices with `_all` or use wildcards. Defaults to `true`. 

'cluster.index.close.enable' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

(动态)在 Elasticsearch 中启用关闭 openindex。如果为"false"，则无法关闭打开的索引。默认为"真"。

关闭的索引仍会占用大量磁盘空间。

"重新索引.远程.白名单" ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting)) Specifies the hosts that can be [reindexed from remotely](docs-reindex.html#reindex-from-remote "Reindex from remote"). Expects a YAML array of `host:port` strings. Consists of a comma-delimited list of `host:port` entries. Defaults to `["\*.io:*", "\*.com:*"]`. 

`stack.templates.enabled`

    

(动态)如果为"true"，则启用内置索引和组件模板。弹性代理使用这些模板来创建数据流。如果为"false"，则 Elasticsearch 将禁用这些索引和组件模板。默认为"true"。

此设置会影响以下内置索引模板：

* "日志-*-*" * "指标-*-*" * "合成-*-*" * "分析-*"

此设置还会影响以下内置组件模板：

* "日志映射" * "日志设置" * "指标映射" * "指标设置" * "合成映射" * "合成设置"

[« Index lifecycle management settings in Elasticsearch](ilm-settings.md)
[Index recovery settings »](recovery.md)
