

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Snapshot and restore settings](snapshot-settings.md) [Thread pools
»](modules-threadpool.md)

## 在弹性搜索中转换设置

无需配置任何设置即可使用转换。默认情况下，它处于启用状态。

#### 常规转换设置

'node.roles： [ transform ]'

    

(静态)将"node.roles"设置为包含"transform"，以将节点标识为_transform node_。如果要运行转换，群集中必须至少有一个转换节点。

如果设置"node.roles"，则必须显式指定节点所需的所有角色。要了解更多信息，请参阅 Node。

强烈建议专用转换节点也具有"remote_cluster_client"角色;否则，在转换中使用时，跨集群搜索将失败。请参阅符合远程条件的节点。

`xpack.transform.enabled`

     [7.8.0]  Deprecated in 7.8.0. Basic License features should always be enabled  ([Static](settings.html#static-cluster-setting)) This deprecated setting no longer has any effect. 
`xpack.transform.num_transform_failure_retries`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The number of times that a transform retries when it experiences a non-fatal error. Once the number of retries is exhausted, the transform task is marked as `failed`. The default value is `10` with a valid minimum of `0` and maximum of `100`. If a transform is already running, it has to be restarted to use the changed setting. The `num_failure_retries` setting can also be specified on an individual transform level. Specifying this setting for each transform individually is recommended. 

[« Snapshot and restore settings](snapshot-settings.md) [Thread pools
»](modules-threadpool.md)
