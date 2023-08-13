

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Logging](logging.md) [Monitoring settings in Elasticsearch »](monitoring-
settings.md)

## 弹性搜索中的机器学习设置

无需配置任何设置即可使用机器学习。默认情况下，它处于启用状态。

机器学习使用 SSE4.2 指令，因此它仅适用于 CPU 支持 SSE4.2 的计算机。如果在较旧的硬件上运行 Elasticsearch，则必须禁用机器学习(通过将"xpack.ml.enabled"设置为"false")。

#### 常规机器学习设置

'node.roles： [ ml ]'

    

(静态)将"node.roles"设置为包含"ml"，以将节点标识为_machine学习node_。如果要运行机器学习作业，群集中必须至少有一个机器学习节点。

如果设置"node.roles"，则必须显式指定节点所需的所有角色。要了解更多信息，请参阅 Node。

* 在专用协调节点或专用主节点上，请勿设置"ml"角色。  * 强烈建议专用机器学习节点也具有"remote_cluster_client"角色;否则，在机器学习作业或数据馈送中使用跨集群搜索时会失败。请参阅符合远程条件的节点。

`xpack.ml.enabled`

    

(静态)默认值 ('true') 在节点上启用机器学习 API。

如果要在群集中使用机器学习功能，建议在所有节点上使用此设置的默认值。

如果设置为"false"，则会在节点上禁用机器学习 API。例如，节点无法打开作业、启动数据馈送、接收传输(内部)通信请求或来自客户端(包括 Kibana)的与机器学习 API 相关的请求。

`xpack.ml.inference_model.cache_size`

     ([Static](settings.html#static-cluster-setting)) The maximum inference cache size allowed. The inference cache exists in the JVM heap on each ingest node. The cache affords faster processing times for the `inference` processor. The value can be a static byte sized value (such as `2gb`) or a percentage of total allocated heap. Defaults to `40%`. See also [Machine learning circuit breaker settings](ml-settings.html#model-inference-circuit-breaker "Machine learning circuit breaker settings"). 

"xpack.ml.inference_model.时间到现场"！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting)) The time to live (TTL) for trained models in the inference model cache. The TTL is calculated from last access. Users of the cache (such as the inference processor or inference aggregator) cache a model on its first use and reset the TTL on every use. If a cached model is not accessed for the duration of the TTL, it is flagged for eviction from the cache. If a document is processed later, the model is again loaded into the cache. To update this setting in Elasticsearch Service, see [Add Elasticsearch user settings](/guide/en/cloud/current/ec-add-user-settings.html). Defaults to `5m`. 
`xpack.ml.max_inference_processors`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The total number of `inference` type processors allowed across all ingest pipelines. Once the limit is reached, adding an `inference` processor to a pipeline is disallowed. Defaults to `50`. 
`xpack.ml.max_machine_memory_percent`

    

(动态)机器学习可用于运行分析进程的计算机内存的最大百分比。这些进程与 ElasticsearchJVM 是分开的。限制基于计算机的总内存，而不是当前可用内存。如果将作业分配给节点会导致机器学习作业的估计内存使用量超过限制，则不会将作业分配给节点。启用操作员权限功能后，此设置只能由操作员用户更新。最小值为"5";最大值为"200"。默认为"30"。

不要将此设置配置为高于运行 Elasticsearch JVM 后剩余内存量的值，除非您有足够的交换空间来容纳它，并且已确定这是专业用例的合适配置。最大设置值适用于已确定对机器学习作业使用交换空间是可接受的特殊情况。一般的最佳实践是不在 Elasticsearchnode 上使用 swap。

`xpack.ml.max_model_memory_limit`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The maximum `model_memory_limit` property value that can be set for any machine learning jobs in this cluster. If you try to create a job with a `model_memory_limit` property value that is greater than this setting value, an error occurs. Existing jobs are not affected when you update this setting. If this setting is `0` or unset, there is no maximum `model_memory_limit` value. If there are no nodes that meet the memory requirements for a job, this lack of a maximum memory limit means it's possible to create jobs that cannot be assigned to any available nodes. For more information about the `model_memory_limit` property, see [Create anomaly detection jobs](ml-put-job.html "Create anomaly detection jobs API") or [Create data frame analytics jobs](put-dfanalytics.html "Create data frame analytics jobs API"). Defaults to `0` if `xpack.ml.use_auto_machine_memory_percent` is `false`. If `xpack.ml.use_auto_machine_memory_percent` is `true` and `xpack.ml.max_model_memory_limit` is not explicitly set then it will default to the largest `model_memory_limit` that could be assigned in the cluster. 

`xpack.ml.max_open_jobs`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The maximum number of jobs that can run simultaneously on a node. In this context, jobs include both anomaly detection jobs and data frame analytics jobs. The maximum number of jobs is also constrained by memory usage. Thus if the estimated memory usage of the jobs would be higher than allowed, fewer jobs will run on a node. Prior to version 7.1, this setting was a per-node non-dynamic setting. It became a cluster-wide dynamic setting in version 7.1. As a result, changes to its value after node startup are used only after every node in the cluster is running version 7.1 or higher. The minimum value is `1`; the maximum value is `512`. Defaults to `512`. 
`xpack.ml.nightly_maintenance_requests_per_second`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The rate at which the nightly maintenance task deletes expired model snapshots and results. The setting is a proxy to the [`requests_per_second`](docs-delete-by-query.html#docs-delete-by-query-throttle "Throttling delete requests") parameter used in the delete by query requests and controls throttling. When the operator privileges feature is enabled, this setting can be updated only by operator users. Valid values must be greater than `0.0` or equal to `-1.0`, where `-1.0` means a default value is used. Defaults to `-1.0`
`xpack.ml.node_concurrent_job_allocations`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The maximum number of jobs that can concurrently be in the `opening` state on each node. Typically, jobs spend a small amount of time in this state before they move to `open` state. Jobs that must restore large models when they are opening spend more time in the `opening` state. When the operator privileges feature is enabled, this setting can be updated only by operator users. Defaults to `2`. 

#### 高级机器学习设置

这些设置适用于高级用例;默认值通常就足够了：

`xpack.ml.enable_config_migration`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) Reserved. When the operator privileges feature is enabled, this setting can be updated only by operator users. 
`xpack.ml.max_anomaly_records`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The maximum number of records that are output per bucket. Defaults to `500`. 
`xpack.ml.max_lazy_ml_nodes`

    

(动态)懒惰启动的机器学习节点的数量。在第一个机器学习作业打开之前不需要机器学习节点的情况下很有用。如果当前机器学习节点数大于或等于此设置，则假定没有更多的惰性节点可用，因为已预配所需的节点数。如果作业已打开，并且此设置的值大于零，并且没有节点可以接受作业，则作业将保持"OPEN"状态，直到将新的机器学习节点添加到群集并将作业分配给在该节点上运行。启用操作员权限功能后，此设置只能由操作员用户更新。默认为"0"。

此设置假定某些外部进程能够将机器学习节点添加到群集。此设置仅在与此类外部进程结合使用时才有用。

`xpack.ml.max_ml_node_size`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The maximum node size for machine learning nodes in a deployment that supports automatic cluster scaling. If you set it to the maximum possible size of future machine learning nodes, when a machine learning job is assigned to a lazy node it can check (and fail quickly) when scaling cannot support the size of the job. When the operator privileges feature is enabled, this setting can be updated only by operator users. Defaults to `0b`, which means it will be assumed that automatic cluster scaling can add arbitrarily large nodes to the cluster. 

`xpack.ml.model_repository`

    

(动态)机器学习模型存储库的位置，在受限或封闭网络中安装模型时，模型工件文件可用。"xpack.ml.model_repository"可以是文件位置或HTTP / HTTPS服务器的字符串。示例值包括：

    
    
    xpack.ml.model_repository: file://${path.home}/config/models/

or

    
    
    xpack.ml.model_repository: https://my-custom-backend

如果 'xpack.ml.model_repository' 是一个文件位置，它必须指向 Elasticsearch 的 'config' 目录的子目录。

`xpack.ml.persist_results_max_retries`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The maximum number of times to retry bulk indexing requests that fail while processing machine learning results. If the limit is reached, the machine learning job stops processing data and its status is `failed`. When the operator privileges feature is enabled, this setting can be updated only by operator users. The minimum value is `0`; the maximum value is `50`. Defaults to `20`. 
`xpack.ml.process_connect_timeout`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The connection timeout for machine learning processes that run separately from the Elasticsearch JVM. When such processes are started they must connect to the Elasticsearch JVM. If the process does not connect within the time period specified by this setting then the process is assumed to have failed. When the operator privileges feature is enabled, this setting can be updated only by operator users. The minimum value is `5s`. Defaults to `10s`. 
`xpack.ml.use_auto_machine_memory_percent`

    

(动态)如果此设置为"true"，则忽略"xpack.ml.max_machine_memory_percent"设置。相反，可以自动计算可用于运行机器学习分析进程的机器内存的最大百分比，并考虑节点上的总节点大小和 JVM 的大小。启用操作员权限功能后，此设置只能由操作员用户更新。默认值为"false"。

* 如果您没有专用的机器学习节点(即节点具有多个角色)，请不要启用此设置。它的计算假设机器学习分析是节点的主要目的。  * 计算假设专用机器学习节点在 JVM 外部至少保留了"256MB"内存。如果群集中有小型机器学习节点，则不应使用此设置。

如果此设置为"true"，则也会影响"xpack.ml.max_model_memory_limit"的默认值。在这种情况下，'xpack.ml.max_model_memory_limit' 默认为当前集群中可以分配的最大大小。

#### 机器学习断路器设置

相关的断路器设置可以在断路器页面中找到。

[« Logging](logging.md) [Monitoring settings in Elasticsearch »](monitoring-
settings.md)
