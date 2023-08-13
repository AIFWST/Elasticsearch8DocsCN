

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Verify snapshot repository API](verify-snapshot-repo-api.md) [Get
snapshot repository API »](get-snapshot-repo-api.md)

## 存储库分析API

分析存储库，报告其性能特征和发现的任何不正确行为。

    
    
    response = client.snapshot.repository_analyze(
      repository: 'my_repository',
      blob_count: 10,
      max_blob_size: '1mb',
      timeout: '120s'
    )
    puts response
    
    
    POST /_snapshot/my_repository/_analyze?blob_count=10&max_blob_size=1mb&timeout=120s

###Request

"发布/_snapshot/<repository>/_analyze"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。有关详细信息，请参阅安全权限。  * 如果启用了操作员权限功能，则只有操作员用户才能使用此 API。

###Description

有大量的第三方存储系统可用，并非所有存储系统都适合由 Elasticsearch 用作快照存储库。某些存储系统的行为不正确或性能不佳，尤其是当多个客户端同时访问时，就像 Elasticsearchcluster 的节点一样。

存储库分析 API 对存储库执行一系列读取和写入操作，这些操作旨在检测不正确的行为并测量存储系统的性能特征。

此 API 的参数的默认值故意偏低，以减少无意中运行分析的影响。实际实验应将"blob_count"设置为至少"2000"，"max_blob_size"设置为至少"2gb"，将"max_total_data_size"设置为至少"1tb"，并且几乎肯定需要增加"超时"以留出时间成功完成该过程。您应该在与生产集群大小相似的多节点集群上运行分析，以便它可以检测仅在多个节点同时访问存储库时才出现的任何问题。

如果分析失败，则 Elasticsearch 检测到您的存储库行为异常。这通常意味着您正在使用第三方存储系统，其声称支持的 API 实现不正确或不兼容。如果是这样，则此存储系统不适合用作快照存储库。您需要与存储系统的供应商合作，以解决 Elasticsearch 检测到的不兼容性问题。有关更多信息，请参阅自我管理的存储库类型。

如果分析成功，此 API 将返回测试过程的详细信息，可以选择包括每个操作所花费的时间。可以使用此信息来确定存储系统的性能。如果任何操作失败或返回不正确的结果，此 API 将返回错误。如果 API 返回错误，则它可能没有删除它写入存储库的所有数据。该错误将指示任何剩余数据的位置，并且此路径也记录在 Elasticsearch 日志中。您应该验证自己是否已正确清理此位置。如果在指定位置仍有剩余数据，则应手动将其删除。

如果在客户端等待分析结果时关闭了从客户端到 Elasticsearch 的连接，则测试将被取消。某些客户端配置为在特定超时内未收到响应时关闭其连接。分析需要很长时间才能完成，因此您可能需要放宽任何此类客户端超时。取消时，分析会尝试清理它正在写入的数据，但它可能无法全部删除。剩余数据的路径记录在 Elasticsearch 日志中。您应该验证自己是否已正确清理此位置。如果在指定位置仍有剩余数据，则应手动将其删除。

如果分析成功，则没有检测到不正确的行为，但这并不意味着保证正确的行为。该分析试图检测常见错误，但它肯定不提供 100% 的覆盖率。此外，它不测试以下内容：

* 您的存储库必须执行持久写入。写入 blob 后，它必须保留在原位，直到删除它，即使在断电或类似灾难之后也是如此。  * 您的存储库不得遭受静默数据损坏。写入 Blob 后，其内容必须保持不变，直到有意修改或删除它。  * 即使来自集群的连接中断，您的存储库也必须正常运行。在这种情况下，读取和写入可能会失败，但它们不得返回不正确的结果。

分析会将大量数据写入存储库，然后再次读回。这会消耗群集和存储库之间的网络上的带宽，以及存储库本身的存储空间和 IO 带宽。必须确保此负载不会影响这些系统的其他用户。分析遵循存储库设置"max_snapshot_bytes_per_sec"和"max_restore_bytes_per_sec"(如果可用)，以及集群设置"index.recovery.max_bytes_per_sec"，您可以使用该设置来限制它们消耗的带宽。

此 API 旨在供人类探索性使用。您应该期望请求参数和响应格式在未来版本中有所不同。

此 API 可能无法在混合版本群集中正常工作。

### 实现详细信息

文档的这一部分描述了存储库分析 API 在此版本的 Elasticsearch 中的工作方式，但您应该期望实现因版本而异。请求参数和响应格式取决于实现的细节，因此在较新版本中也可能有所不同。

分析包括许多 Blob 级任务，由"blob_count"参数设置。Blob 级任务分布在群集中符合数据和主节点条件的节点上，以便执行。

对于大多数 Blob 级任务，执行节点首先将 Blob 写入存储库，然后指示群集中的其他一些节点尝试读取它刚刚写入的数据。斑点的大小是根据"max_blob_size"和"max_total_data_size"参数随机选择的。如果这些读取中的任何一个失败，那么存储库就不会实现 Elasticsearch 所需的必要的写后读语义。

对于某些 Blob 级任务，执行节点将指示其某些对等方在写入过程完成之前尝试读取数据。允许这些读取失败，但不得返回部分数据。如果任何读取返回部分数据，则存储库不会实现 Elasticsearch 所需的必要原子性语义。

对于某些 Blob 级别任务，执行节点将在其对等方读取 Blob 时覆盖该 Blob。在这种情况下，读取的数据可能来自原始 Blob 或覆盖的 Blob，但读取操作不得返回部分数据或来自两个 Blob 的数据混合。如果这些读取中的任何一个返回部分数据或两个 blob 的混合，则存储库不会实现 Elasticsearch 需要覆盖的必要原子性语义。

执行节点将使用各种不同的方法来写入 Blob。例如，在适用的情况下，它将同时使用单部分和多部分上传。同样，读取节点将使用各种不同的方法来再次读取数据。例如，它们可能从头到尾读取整个 Blob，或者可能只读取数据的子集。

对于某些 Blob 级别的任务，执行节点将在写入完成之前中止写入。在这种情况下，它仍会指示群集中的其他一些节点尝试读取 Blob，但所有这些读取都必须无法找到 Blob。

### 路径参数

`<repository>`

     (Required, string) Name of the snapshot repository to test. 

### 查询参数

`blob_count`

     (Optional, integer) The total number of blobs to write to the repository during the test. Defaults to `100`. For realistic experiments you should set this to at least `2000`. 
`max_blob_size`

     (Optional, [size units](api-conventions.html#size-units "Unit-less quantities")) The maximum size of a blob to be written during the test. Defaults to `10mb`. For realistic experiments you should set this to at least `2gb`. 
`max_total_data_size`

     (Optional, [size units](api-conventions.html#size-units "Unit-less quantities")) An upper limit on the total size of all the blobs written during the test. Defaults to `1gb`. For realistic experiments you should set this to at least `1tb`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for the test to complete. If no response is received before the timeout expires, the test is cancelled and returns an error. Defaults to `30s`. 

#### 高级查询参数

以下参数允许对分析进行额外的控制，但通常不需要对其进行调整。

`concurrency`

     (Optional, integer) The number of write operations to perform concurrently. Defaults to `10`. 
`read_node_count`

     (Optional, integer) The number of nodes on which to perform a read operation after writing each blob. Defaults to `10`. 
`early_read_node_count`

     (Optional, integer) The number of nodes on which to perform an early read operation while writing each blob. Defaults to `2`. Early read operations are only rarely performed. 
`rare_action_probability`

     (Optional, double) The probability of performing a rare action (an early read, an overwrite, or an aborted write) on each blob. Defaults to `0.02`. 
`seed`

     (Optional, integer) The seed for the pseudo-random number generator used to generate the list of operations performed during the test. To repeat the same set of operations in multiple experiments, use the same seed in each experiment. Note that the operations are performed concurrently so may not always happen in the same order on each run. 
`detailed`

     (Optional, boolean) Whether to return detailed results, including timing information for every operation performed during the analysis. Defaults to `false`, meaning to return only a summary of the analysis. 
`rarely_abort_writes`

     (Optional, boolean) Whether to rarely abort some write requests. Defaults to `true`. 

### 响应正文

响应公开分析的实现详细信息，这些详细信息可能因版本而异。因此，响应正文格式不被认为是稳定的，并且在较新版本中可能会有所不同。

`coordinating_node`

    

(对象)标识协调分析并执行最终清理的节点。

"coordinating_node"的属性

`id`

     (string) The id of the coordinating node. 
`name`

     (string) The name of the coordinating node 

`repository`

     (string) The name of the repository that was the subject of the analysis. 
`blob_count`

     (integer) The number of blobs written to the repository during the test, equal to the `?blob_count` request parameter. 
`concurrency`

     (integer) The number of write operations performed concurrently during the test, equal to the `?concurrency` request parameter. 
`read_node_count`

     (integer) The limit on the number of nodes on which read operations were performed after writing each blob, equal to the `?read_node_count` request parameter. 
`early_read_node_count`

     (integer) The limit on the number of nodes on which early read operations were performed after writing each blob, equal to the `?early_read_node_count` request parameter. 
`max_blob_size`

     (string) The limit on the size of a blob written during the test, equal to the `?max_blob_size` parameter. 
`max_blob_size_bytes`

     (long) The limit, in bytes, on the size of a blob written during the test, equal to the `?max_blob_size` parameter. 
`max_total_data_size`

     (string) The limit on the total size of all blob written during the test, equal to the `?max_total_data_size` parameter. 
`max_total_data_size_bytes`

     (long) The limit, in bytes, on the total size of all blob written during the test, equal to the `?max_total_data_size` parameter. 
`seed`

     (long) The seed for the pseudo-random number generator used to generate the operations used during the test. Equal to the `?seed` request parameter if set. 
`rare_action_probability`

     (double) The probability of performing rare actions during the test. Equal to the `?rare_action_probability` request parameter. 
`blob_path`

     (string) The path in the repository under which all the blobs were written during the test. 
`issues_detected`

     (list) A list of correctness issues detected, which will be empty if the API succeeded. Included to emphasize that a successful response does not guarantee correct behaviour in future. 
`summary`

    

(对象)汇总测试结果的统计信息集合。

"摘要"的属性

`write`

    

(对象)汇总测试中写入操作结果的统计信息集合。

"写入"的属性

`count`

     (integer) The number of write operations performed in the test. 
`total_size`

     (string) The total size of all the blobs written in the test. 
`total_size_bytes`

     (long) The total size of all the blobs written in the test, in bytes. 
`total_throttled`

     (string) The total time spent waiting due to the `max_snapshot_bytes_per_sec` throttle. 
`total_throttled_nanos`

     (long) The total time spent waiting due to the `max_snapshot_bytes_per_sec` throttle, in nanoseconds. 
`total_elapsed`

     (string) The total elapsed time spent on writing blobs in the test. 
`total_elapsed_nanos`

     (long) The total elapsed time spent on writing blobs in the test, in nanoseconds. 

`read`

    

(对象)汇总测试中读取操作结果的统计信息集合。

"读取"的属性

`count`

     (integer) The number of read operations performed in the test. 
`total_size`

     (string) The total size of all the blobs or partial blobs read in the test. 
`total_size_bytes`

     (long) The total size of all the blobs or partial blobs read in the test, in bytes. 
`total_wait`

     (string) The total time spent waiting for the first byte of each read request to be received. 
`total_wait_nanos`

     (long) The total time spent waiting for the first byte of each read request to be received, in nanoseconds. 
`max_wait`

     (string) The maximum time spent waiting for the first byte of any read request to be received. 
`max_wait_nanos`

     (long) The maximum time spent waiting for the first byte of any read request to be received, in nanoseconds. 
`total_throttled`

     (string) The total time spent waiting due to the `max_restore_bytes_per_sec` or `indices.recovery.max_bytes_per_sec` throttles. 
`total_throttled_nanos`

     (long) The total time spent waiting due to the `max_restore_bytes_per_sec` or `indices.recovery.max_bytes_per_sec` throttles, in nanoseconds. 
`total_elapsed`

     (string) The total elapsed time spent on reading blobs in the test. 
`total_elapsed_nanos`

     (long) The total elapsed time spent on reading blobs in the test, in nanoseconds. 

`details`

    

(阵列)对测试期间执行的每个读取和写入操作的描述。仅当"？详细"请求参数设置为"true"时，才会返回此参数。

"详细信息"中项目的属性

`blob`

    

(对象)已写入和读取的 Blob 的说明。

"斑点"的属性

`name`

     (string) The name of the blob. 
`size`

     (string) The size of the blob. 
`size_bytes`

     (long) The size of the blob in bytes. 
`read_start`

     (long) The position, in bytes, at which read operations started. 
`read_end`

     (long) The position, in bytes, at which read operations completed. 
`read_early`

     (boolean) Whether any read operations were started before the write operation completed. 
`overwritten`

     (boolean) Whether the blob was overwritten while the read operations were ongoing. 

`writer_node`

    

(对象)标识写入此 Blob 并协调读取操作的节点。

"writer_node"的属性

`id`

     (string) The id of the writer node. 
`name`

     (string) The name of the writer node 

`write_elapsed`

     (string) The elapsed time spent writing this blob. 
`write_elapsed_nanos`

     (long) The elapsed time spent writing this blob, in nanoseconds. 
`overwrite_elapsed`

     (string) The elapsed time spent overwriting this blob. Omitted if the blob was not overwritten. 
`overwrite_elapsed_nanos`

     (long) The elapsed time spent overwriting this blob, in nanoseconds. Omitted if the blob was not overwritten. 
`write_throttled`

     (string) The length of time spent waiting for the `max_snapshot_bytes_per_sec` (or `indices.recovery.max_bytes_per_sec` if the [recovery settings for managed services](recovery.html#recovery-settings-for-managed-services "Recovery settings for managed services") are set) throttle while writing this blob. 
`write_throttled_nanos`

     (long) The length of time spent waiting for the `max_snapshot_bytes_per_sec` (or `indices.recovery.max_bytes_per_sec` if the [recovery settings for managed services](recovery.html#recovery-settings-for-managed-services "Recovery settings for managed services") are set) throttle while writing this blob, in nanoseconds. 
`reads`

    

(阵列)对此 Blob 执行的每个读取操作的说明。

"读取"中项目的属性

`node`

    

(对象)标识执行读取操作的节点。

"节点"的属性

`id`

     (string) The id of the reader node. 
`name`

     (string) The name of the reader node 

`before_write_complete`

     (boolean) Whether the read operation may have started before the write operation was complete. Omitted if `false`. 
`found`

     (boolean) Whether the blob was found by this read operation or not. May be `false` if the read was started before the write completed, or the write was aborted before completion. 
`first_byte_time`

     (string) The length of time waiting for the first byte of the read operation to be received. Omitted if the blob was not found. 
`first_byte_time_nanos`

     (long) The length of time waiting for the first byte of the read operation to be received, in nanoseconds. Omitted if the blob was not found. 
`elapsed`

     (string) The length of time spent reading this blob. Omitted if the blob was not found. 
`elapsed_nanos`

     (long) The length of time spent reading this blob, in nanoseconds. Omitted if the blob was not found. 
`throttled`

     (string) The length of time spent waiting due to the `max_restore_bytes_per_sec` or `indices.recovery.max_bytes_per_sec` throttles during the read of this blob. Omitted if the blob was not found. 
`throttled_nanos`

     (long) The length of time spent waiting due to the `max_restore_bytes_per_sec` or `indices.recovery.max_bytes_per_sec` throttles during the read of this blob, in nanoseconds. Omitted if the blob was not found. 

`listing_elapsed`

     (string) The time it took to retrieve a list of all the blobs in the container. 
`listing_elapsed_nanos`

     (long) The time it took to retrieve a list of all the blobs in the container, in nanoseconds. 
`delete_elapsed`

     (string) The time it took to delete all the blobs in the container. 
`delete_elapsed_nanos`

     (long) The time it took to delete all the blobs in the container, in nanoseconds. 

[« Verify snapshot repository API](verify-snapshot-repo-api.md) [Get
snapshot repository API »](get-snapshot-repo-api.md)
